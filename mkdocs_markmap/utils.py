import logging
import os
from pathlib import Path

from urllib.parse import unquote
from urllib3 import PoolManager
from urllib3.response import HTTPResponse
from urllib3.util.retry import Retry
from urllib3.util.url import Url, parse_url


log = logging.getLogger('mkdocs.markmap')


def download(base_path: Path, url: str, flat: bool = False, force_reload: bool = False) -> str:
    parsed_url: Url = parse_url(url)
    path: str = unquote(parsed_url.request_uri.split('?')[0])
    sub_path: str = os.path.basename(path) if flat else f'{parsed_url.hostname}{path}'
    file_path: Path = base_path / sub_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    retries = Retry(connect=5, read=2, redirect=5)
    http = PoolManager(retries=retries)
    if force_reload or not file_path.exists():
        response: HTTPResponse = http.request('GET', url)
        with open(file_path, 'wb') as fp:
            fp.write(response.data)

    log.info(f'script downloaded: {url}')

    return str(sub_path)
