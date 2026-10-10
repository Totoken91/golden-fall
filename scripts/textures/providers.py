"""Official API adapters. Download URLs are read exclusively from file metadata."""
import re
from urllib.parse import urlencode, quote
from net import PipelineError

PH = 'https://api.polyhaven.com'
ACG = 'https://ambientcg.com/api/v2/full_json'
LICENSES = {
    'polyhaven': 'https://polyhaven.com/license',
    'ambientcg': 'https://docs.ambientcg.com/license/',
}


def safe_id(value):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', value):
        raise PipelineError('Invalid asset ID')
    return value


def tokens(value):
    return set(re.findall(r'[a-z]+', value.lower().replace('_', ' ')))


def rank(candidate, brief):
    text = ' '.join([candidate['id'], candidate['name'], *candidate['tags'], candidate.get('description', '')])
    words = tokens(text)
    required = set(brief.get('require_any', []))
    if required and not required.intersection(words):
        return None
    positive = set(brief.get('prefer', [])) & words
    negative = set(brief.get('avoid', [])) & words
    query_match = tokens(brief['query']) & words
    score = 3 * len(positive) - 4 * len(negative) + len(query_match)
    # API rank is used, not Poly Haven's vector score (different ranking signals).
    score += 2 / (1 + candidate['api_rank'])
    return {'score': round(score, 4), 'preferred_matches': sorted(positive),
            'avoided_matches': sorted(negative), 'query_matches': sorted(query_match),
            'method': 'metadata heuristic; visual review still required'}


def ph_info(client, asset_id, index=0):
    asset_id = safe_id(asset_id)
    url = PH + '/info/' + quote(asset_id)
    info = client.json(url)
    if info.get('type') != 1:
        raise PipelineError('Poly Haven asset is not a texture')
    dims = info.get('dimensions') or []
    tile = [round(float(x) / 1000, 6) for x in dims[:2]] if len(dims) >= 2 and all(float(x) > 0 for x in dims[:2]) else None
    return {'provider': 'polyhaven', 'id': asset_id, 'name': info.get('name', asset_id),
            'tags': info.get('tags', []), 'description': info.get('description', ''),
            'tile_m': tile, 'dimension_basis': 'API dimensions in millimeters' if tile else 'unknown',
            'api_rank': index, 'source_page': 'https://polyhaven.com/a/' + asset_id,
            'metadata_url': url, 'authors': info.get('authors', {}),
            'seamless': {'status': 'candidate', 'basis': 'PBR texture category; verify edge continuity and 2x2 tiling'},
            'raw_metadata': info}


def acg_info(info, index=0):
    asset_id = safe_id(info['assetId'])
    if info.get('dataType', '').lower() != 'material':
        raise PipelineError('ambientCG asset is not a Material')
    x, y = info.get('dimensionX', 0), info.get('dimensionY', 0)
    # ambientCG v2 dimensions are centimeters. Zero means unknown, not zero meters.
    tile = [float(x) / 100, float(y) / 100] if x and y and x > 0 and y > 0 else None
    return {'provider': 'ambientcg', 'id': asset_id, 'name': info.get('displayName', asset_id),
            'tags': info.get('tags', []), 'description': info.get('description', ''),
            'tile_m': tile, 'dimension_basis': 'API dimensions in centimeters' if tile else 'unknown',
            'api_rank': index, 'source_page': 'https://ambientcg.com/a/' + asset_id,
            'metadata_url': ACG + '?' + urlencode({'id': asset_id, 'include': 'downloadData,tagData,dimensionsData'}),
            'authors': {'ambientCG': info.get('creationMethod', '')},
            'seamless': {'status': 'candidate', 'basis': 'Material category; verify edge continuity and 2x2 tiling'},
            'raw_metadata': info}


def lookup(client, provider, asset_id):
    safe_id(asset_id)
    if provider == 'polyhaven':
        return ph_info(client, asset_id)
    url = ACG + '?' + urlencode({'id': asset_id, 'include': 'downloadData,tagData,dimensionsData'})
    matches = client.json(url).get('foundAssets', [])
    exact = [a for a in matches if a.get('assetId') == asset_id]
    if not exact:
        raise PipelineError('ambientCG ID not returned by API: ' + asset_id)
    return acg_info(exact[0])


def search(client, brief, limit=6):
    results, errors = [], {}
    # Both sources are always queried. One failure is reported explicitly.
    for provider in ('polyhaven', 'ambientcg'):
        try:
            if provider == 'polyhaven':
                url = PH + '/search?' + urlencode({'q': brief['query'].strip().lower(), 't': 'textures', 'limit': limit, 'future': 'false'})
                matches = client.json(url).get('results', [])
                candidates = [ph_info(client, m['slug'], i) for i, m in enumerate(matches[:limit])]
            else:
                url = ACG + '?' + urlencode({'q': brief.get('ambientcg_query', brief['query']), 'type': 'Material',
                        'limit': limit, 'sort': 'Popular', 'include': 'downloadData,tagData,dimensionsData'})
                candidates = [acg_info(m, i) for i, m in enumerate(client.json(url).get('foundAssets', []))]
            for item in candidates:
                ranking = rank(item, brief)
                if ranking is not None:
                    item['ranking'] = ranking
                    results.append(item)
        except (PipelineError, KeyError, TypeError, ValueError) as exc:
            errors[provider] = str(exc)
    results.sort(key=lambda x: (-x['ranking']['score'], x['provider'], x['id']))
    return results, errors


def resolution_choice(available, target_k):
    choices = []
    for label in available:
        if re.fullmatch(r'\d+[kK]', label):
            k = int(label[:-1])
            choices.append((0 if k >= target_k else 1, abs(k - target_k), k, label))
    if not choices:
        raise PipelineError('No supported resolution in API metadata')
    return min(choices)[3]


def ph_files(client, asset_id, source_k=1, ao=True):
    url = PH + '/files/' + quote(safe_id(asset_id))
    files = client.json(url)
    maps = {}
    for role, name in [('albedo', 'Diffuse'), ('normal', 'nor_gl'), ('roughness', 'Rough'), ('ao', 'AO')]:
        if role == 'ao' and not ao:
            continue
        if name not in files:
            if role == 'ao':
                continue
            raise PipelineError('Missing required Poly Haven map: ' + name)
        label = resolution_choice(files[name], source_k)
        variants = files[name][label]
        preferred = ('png', 'jpg') if role == 'normal' else ('jpg', 'png')
        fmt = next((f for f in preferred if f in variants), None)
        if fmt is None:
            raise PipelineError('No PNG/JPG for ' + name)
        entry = variants[fmt]
        maps[role] = {'url': entry['url'], 'size': entry.get('size'), 'md5': entry.get('md5'),
                      'filename': role + '_' + label + '.' + fmt, 'normal_convention': 'OpenGL' if role == 'normal' else None}
    return {'metadata_url': url, 'maps': maps}


def acg_archive(candidate, source_k=1):
    downloads = []
    for folder in candidate['raw_metadata'].get('downloadFolders', {}).values():
        for category in folder.get('downloadFiletypeCategories', {}).values():
            downloads.extend(category.get('downloads', []))
    choices = []
    for entry in downloads:
        label = entry.get('attribute', '')
        match = re.fullmatch(r'(\d+)K-(JPG|PNG)', label, flags=re.I)
        if match and entry.get('filetype', '').lower() == 'zip':
            k = int(match[1])
            choices.append(((0 if k >= source_k else 1, abs(k - source_k), 0 if match[2].upper() == 'JPG' else 1), entry))
    if not choices:
        raise PipelineError('No supported ambientCG ZIP in metadata')
    entry = min(choices, key=lambda x: x[0])[1]
    # Never construct a download URL from an ID or use previewImage/previewLinks.
    return {'url': entry.get('downloadLink') or entry['fullDownloadPath'], 'size': entry.get('size'),
            'filename': safe_id(candidate['id']) + '_' + entry['attribute'] + '.zip'}
