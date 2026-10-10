"""Small persistent HTTP cache. A failed request never creates a successful receipt."""
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = 'LesHeuresCreuses-TexturePipeline/1.0 (offline game asset authoring; Poly Haven + ambientCG)'


class PipelineError(RuntimeError):
    pass


def digest(path, algorithm='sha256'):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, algorithm).hexdigest()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)


def secure_url(url):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password:
        raise PipelineError('Expected an HTTPS URL without credentials: ' + url)
    return url


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        secure_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Client:
    def __init__(self, cache, offline=False, refresh=False, max_mb=48, ttl_hours=168):
        self.cache = Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.offline, self.refresh = offline, refresh
        self.max_bytes = int(max_mb * 1024 * 1024)
        self.transfer_budget = self.max_bytes
        self.ttl = ttl_hours * 3600
        self.requests = self.downloaded_bytes = self.cache_hits = 0
        self.opener = urllib.request.build_opener(HTTPSRedirect())

    def _open(self, url):
        if self.offline:
            raise PipelineError('Offline: no cached response for ' + url)
        secure_url(url)
        for attempt in range(3):
            try:
                self.requests += 1
                return self.opener.open(urllib.request.Request(url, headers={
                    'User-Agent': USER_AGENT, 'Accept': '*/*'}), timeout=25)
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise PipelineError(f'HTTP {exc.code}: {url}') from exc
                wait = exc.headers.get('Retry-After', '')
                # Never hammer the API or wait silently for minutes.
                if wait.isdigit() and int(wait) > 10:
                    raise PipelineError(f'Rate limit: retry after {wait}s: {url}') from exc
                time.sleep(int(wait) if wait.isdigit() else 1 + attempt * 2)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                raise PipelineError(f'Network unavailable: {url}: {exc}') from exc

    def json(self, url):
        secure_url(url)
        key = hashlib.sha256(url.encode()).hexdigest()
        path = self.cache / (key + '.json')
        if path.exists():
            record = json.loads(path.read_text(encoding='utf-8'))
            if record['url'] != url:
                raise PipelineError('Metadata cache URL mismatch')
            if self.offline or (not self.refresh and time.time() - record['fetched_at'] < self.ttl):
                self.cache_hits += 1
                return record['data']
        with self._open(url) as response:
            raw = response.read(8 * 1024 * 1024 + 1)
            if len(raw) > 8 * 1024 * 1024:
                raise PipelineError('API JSON exceeds 8 MiB')
            try:
                data = json.loads(raw)
            except (ValueError, UnicodeDecodeError) as exc:
                raise PipelineError('Response is not JSON: ' + url) from exc
        write_json(path, {'url': url, 'fetched_at': time.time(), 'data': data})
        return data

    def file(self, url, target, expected_size=None, expected_md5=None):
        secure_url(url)
        target = Path(target)
        receipt = target.with_name(target.name + '.receipt.json')
        if target.exists() and receipt.exists():
            info = json.loads(receipt.read_text(encoding='utf-8'))
            if (info['url'] == url and digest(target) == info['sha256']
                    and (not expected_size or target.stat().st_size == expected_size)
                    and (not expected_md5 or digest(target, 'md5') == expected_md5)):
                self.cache_hits += 1
                return info
        if expected_size and expected_size > self.max_bytes:
            raise PipelineError('File exceeds the configured download limit')
        target.parent.mkdir(parents=True, exist_ok=True)
        partial = target.with_name(target.name + '.part')
        try:
            with self._open(url) as response, partial.open('wb') as out:
                declared = int(response.headers.get('Content-Length', 0))
                if declared > self.max_bytes or self.downloaded_bytes + declared > self.transfer_budget:
                    raise PipelineError('Content-Length exceeds download limit')
                total = 0
                while chunk := response.read(256 * 1024):
                    total += len(chunk)
                    if total > self.max_bytes or self.downloaded_bytes + total > self.transfer_budget:
                        raise PipelineError('Stream exceeds download limit')
                    out.write(chunk)
                final_url = response.geturl()
                content_type = response.headers.get('Content-Type', '')
            if total == 0 or (expected_size and total != expected_size):
                raise PipelineError(f'Incomplete file: received {total}, expected {expected_size}')
            if expected_md5 and digest(partial, 'md5') != expected_md5:
                raise PipelineError('Source MD5 mismatch')
            if 'text/html' in content_type:
                raise PipelineError('Downloaded HTML instead of a texture/archive')
            info = {'url': url, 'resolved_url': final_url, 'bytes': total,
                    'sha256': digest(partial), 'source_md5': expected_md5,
                    'content_type': content_type, 'downloaded_at': time.time()}
            os.replace(partial, target)
            write_json(receipt, info)
            self.downloaded_bytes += total
            return info
        finally:
            partial.unlink(missing_ok=True)
