#!/usr/bin/env python3
"""Official texture acquisition CLI; authoring-time only, never called by the game."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

from net import Client, PipelineError, digest, write_json
from providers import search, lookup, ph_files, acg_archive, safe_id, LICENSES
from processing import extract_maps, image_info, convert_maps, PROCESSOR_VERSION
from integration import publish, publish_catalog

ROOT = Path(__file__).resolve().parents[2]


def now():
    return datetime.now(timezone.utc).isoformat()


def serial(value, root):
    if isinstance(value, Path):
        return value.relative_to(root).as_posix()
    if isinstance(value, dict):
        return {k: serial(v, root) for k, v in value.items()}
    if isinstance(value, list):
        return [serial(v, root) for v in value]
    return value


def load_manifest(base):
    path = base / 'manifest.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
        'schema_version': 1, 'pipeline_version': 1, 'assets': {}, 'runs': []}


@contextmanager
def locked(base):
    base.mkdir(parents=True, exist_ok=True)
    path = base / '.pipeline.lock'
    try:
        stream = path.open('x', encoding='utf-8')
    except FileExistsError as exc:
        raise PipelineError('Another pipeline run is active; inspect .pipeline.lock before removing a stale lock') from exc
    try:
        stream.write(now())
        stream.close()
        yield
    finally:
        path.unlink(missing_ok=True)


def get_brief(args, config):
    brief = dict(config['briefs'][args.brief])
    if args.brief_json:
        brief.update(json.loads(Path(args.brief_json).read_text(encoding='utf-8')))
    if args.query:
        brief['query'] = args.query
        brief['ambientcg_query'] = args.query
    if not 1 <= len(brief['query'].strip()) <= 100:
        raise PipelineError('Search query must contain 1..100 characters')
    return brief


def verify_asset(root, entry):
    problems = []
    files = list(entry['source_files'].values()) + list(entry['optimized_maps'].values())
    files += list(entry['godot']['maps'].values())
    files.append({'path': entry['godot']['material'], 'sha256': entry['godot']['sha256']})
    files += entry.get('download_receipts', [])
    for item in files:
        path = root / item['path']
        if not path.is_file() or digest(path) != item['sha256']:
            problems.append(item['path'])
    return problems


def acquire(root, args, config, client, base, manifest, report):
    brief = report['brief']
    profile = config['profiles'][args.profile]
    signature = hashlib.sha256(json.dumps({'brief': brief, 'profile': profile, 'profile_name': args.profile,
        'side': args.size, 'provider': args.provider, 'id': args.id, 'tile_m': args.tile_m,
        'surface_m': args.surface_m, 'ao': not args.no_ao, 'source_k': args.source_k,
        'processor': PROCESSOR_VERSION}, sort_keys=True).encode()).hexdigest()
    if not args.refresh:
        for key, entry in manifest['assets'].items():
            if entry['request_signature'] == signature and not verify_asset(root, entry):
                report.update(status='reused', key=key, material=entry['godot']['material'],
                              note='Manifest + source/runtime hashes verified; no network needed')
                return
    candidates, errors = search(client, brief, args.limit)
    report.update(search_errors=errors, candidates=[{k: v for k, v in c.items() if k != 'raw_metadata'} for c in candidates])
    if args.id:
        if args.provider == 'auto' or not args.reason:
            raise PipelineError('Explicit ID requires --provider and --reason; search still runs on both sources')
        candidates = [lookup(client, args.provider, args.id)]
        report['selection_reason'] = args.reason
    elif args.provider != 'auto':
        candidates = [c for c in candidates if c['provider'] == args.provider]
    if not candidates:
        raise PipelineError('No appropriate candidate; sources/errors: ' + json.dumps(errors))
    selected = None
    preflight_errors = []
    for candidate in candidates:
        try:
            plan = ph_files(client, candidate['id'], args.source_k, not args.no_ao) if candidate['provider'] == 'polyhaven' else {'archive': acg_archive(candidate, args.source_k)}
            sizes = [i.get('size') or 0 for i in plan.get('maps', {}).values()]
            if 'archive' in plan:
                sizes.append(plan['archive'].get('size') or 0)
            if sum(sizes) > config['max_acquisition_mb'] * 1024 * 1024:
                raise PipelineError('Acquisition exceeds total download budget')
            tile = args.tile_m or candidate['tile_m']
            if not tile:
                raise PipelineError('Physical tile size unknown: supply --tile-m WIDTH HEIGHT in meters')
            if any(v <= 0 for v in tile):
                raise PipelineError('Physical tile dimensions must be positive')
            selected = candidate
            break
        except (PipelineError, KeyError, TypeError, ValueError) as exc:
            preflight_errors.append({'id': candidate['id'], 'provider': candidate['provider'], 'error': str(exc)})
    report['preflight_errors'] = preflight_errors
    if selected is None:
        raise PipelineError('No downloadable candidate with suitable PBR maps and scale: ' + json.dumps(preflight_errors))
    provider, asset_id = selected['provider'], safe_id(selected['id'])
    key = f'{provider}/{asset_id}/{args.profile}_{args.size}_{signature[:8]}'
    source_dir = base / 'sources' / provider / asset_id
    sources, receipts = {}, []
    if 'archive' in plan:
        item = plan['archive']
        target = source_dir / item['filename']
        receipt = client.file(item['url'], target, item.get('size'))
        receipts.append({'path': target, **receipt})
        sources = extract_maps(target, source_dir / 'maps', not args.no_ao)
        for source in sources.values():
            source['url'] = item['url']
    else:
        for role, item in plan['maps'].items():
            target = source_dir / item['filename']
            receipt = client.file(item['url'], target, item.get('size'), item.get('md5'))
            image_info(target)
            receipts.append({'path': target, **receipt})
            sources[role] = {'path': target, 'sha256': digest(target), 'url': item['url'],
                             'normal_convention': item.get('normal_convention')}
    converted, seams = convert_maps(sources, base / 'optimized' / key, profile, args.size)
    surface = args.surface_m or tile
    godot = publish(root, key, converted, tile, surface, profile)
    entry = {'provider': provider, 'id': asset_id, 'name': selected['name'], 'created_at': now(),
        'status': 'downloaded_optimized_pending_visual_review', 'request_signature': signature,
        'brief': brief, 'selection': report.get('selection_reason') or selected.get('ranking'),
        'source_page': selected['source_page'], 'metadata_url': selected['metadata_url'],
        'files_metadata_url': plan.get('metadata_url', selected['metadata_url']),
        'license': {'spdx': 'CC0-1.0', 'url': 'https://creativecommons.org/publicdomain/zero/1.0/',
                    'source_policy_url': LICENSES[provider]},
        'tile_m': tile, 'tile_basis': 'explicit authoring override' if args.tile_m else selected['dimension_basis'],
        'seamless': {'api_evidence': selected['seamless'], 'measurements': seams, 'approved': False},
        'source_files': sources, 'download_receipts': receipts, 'optimized_maps': converted,
        'transformation': {'processor_version': PROCESSOR_VERSION, 'profile_name': args.profile,
                           'profile': profile, 'max_side': args.size}, 'godot': godot,
        'visual_reviews': []}
    manifest['assets'][key] = serial(entry, root)
    report.update(status='downloaded_optimized', key=key, material=godot['material'],
                  selected={'provider': provider, 'id': asset_id}, visual_review_required=True)


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['search', 'acquire', 'verify', 'review'])
    p.add_argument('--brief', default='wood_floor')
    p.add_argument('--brief-json', help='Merge a JSON brief with query, prefer, avoid, require_any')
    p.add_argument('--query')
    p.add_argument('--profile', default='retro_realistic')
    p.add_argument('--size', type=int, choices=[64, 128, 256, 512, 1024], default=256)
    p.add_argument('--source-k', type=int, choices=[1, 2], default=1)
    p.add_argument('--limit', type=int, choices=range(1, 13), default=6)
    p.add_argument('--provider', choices=['auto', 'polyhaven', 'ambientcg'], default='auto')
    p.add_argument('--id')
    p.add_argument('--reason')
    p.add_argument('--tile-m', type=float, nargs=2)
    p.add_argument('--surface-m', type=float, nargs=2)
    p.add_argument('--no-ao', action='store_true')
    p.add_argument('--offline', action='store_true')
    p.add_argument('--refresh', action='store_true')
    p.add_argument('--report', help='JSON report path relative to project root')
    p.add_argument('--key', help='Manifest key for visual review')
    p.add_argument('--capture', help='Actual engine screenshot path relative to project root')
    p.add_argument('--notes')
    return p


def run(args, root=ROOT):
    base = root / 'assets/textures'
    config = json.loads((base / 'config.json').read_text(encoding='utf-8'))
    report = {'at': now(), 'command': args.command, 'status': 'started'}
    with locked(base):
        manifest = load_manifest(base)
        client = Client(base / 'cache/api', args.offline, args.refresh, config['max_file_mb'])
        client.transfer_budget = config['max_acquisition_mb'] * 1024 * 1024
        try:
            if args.command in ('search', 'acquire'):
                if args.brief not in config['briefs'] or args.profile not in config['profiles']:
                    raise PipelineError('Unknown brief or profile; see assets/textures/config.json')
                if args.surface_m and any(v <= 0 for v in args.surface_m):
                    raise PipelineError('Surface dimensions must be positive')
                report['brief'] = get_brief(args, config)
                if args.command == 'search':
                    candidates, errors = search(client, report['brief'], args.limit)
                    report.update(status='searched', candidates=[{k: v for k, v in c.items() if k != 'raw_metadata'} for c in candidates], search_errors=errors)
                    if not candidates:
                        raise PipelineError('No candidates; see search_errors')
                else:
                    acquire(root, args, config, client, base, manifest, report)
            elif args.command == 'verify':
                failures = {key: errors for key, value in manifest['assets'].items() if (errors := verify_asset(root, value))}
                report.update(status='verified' if not failures else 'failed', assets=len(manifest['assets']), failures=failures)
                if failures:
                    raise PipelineError('Manifest verification failed')
            else:
                if not args.key or not args.capture or not args.notes or args.key not in manifest['assets']:
                    raise PipelineError('Review requires existing --key, --capture and --notes')
                capture = (root / args.capture).resolve()
                if not capture.is_relative_to(root.resolve()) or not capture.is_file():
                    raise PipelineError('Capture must exist inside this project')
                image_info(capture)
                entry = manifest['assets'][args.key]
                if verify_asset(root, entry):
                    raise PipelineError('Cannot review asset with invalid hashes')
                entry['visual_reviews'].append({'at': now(), 'capture': capture.relative_to(root).as_posix(),
                    'sha256': digest(capture), 'notes': args.notes, 'kind': 'engine review; not user artistic approval'})
                entry['status'] = 'visually_checked_in_engine'
                report.update(status='review_recorded', key=args.key)
        except (PipelineError, OSError, ValueError, KeyError, TypeError) as exc:
            report.update(status='failed', error=str(exc))
        report['network'] = {'requests': client.requests, 'downloaded_bytes': client.downloaded_bytes, 'cache_hits': client.cache_hits,
                             'offline': args.offline}
        manifest['runs'].append(report)
        publish_catalog(root, manifest['assets'])
        write_json(base / 'manifest.json', manifest)
        if args.report:
            path = (root / args.report).resolve()
            if not path.is_relative_to(root.resolve()):
                raise PipelineError('Report must stay inside project root')
            write_json(path, report)
    print(json.dumps({k: v for k, v in report.items() if k != 'candidates'}, ensure_ascii=True, indent=2))
    if 'candidates' in report:
        print(json.dumps([{'provider': c['provider'], 'id': c['id'], 'score': c.get('ranking', {}).get('score'),
                           'tags': c['tags'], 'tile_m': c['tile_m']} for c in report['candidates'][:12]], ensure_ascii=True, indent=2))
    return 1 if report['status'] == 'failed' else 0


if __name__ == '__main__':
    try:
        sys.exit(run(parser().parse_args()))
    except (PipelineError, OSError, ValueError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=True), file=sys.stderr)
        sys.exit(1)
