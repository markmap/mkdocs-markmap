import logging
import os
from pathlib import Path

from urllib.parse import unquote
from requests.adapters import HTTPAdapter
from requests import Response
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.util.url import Url, parse_url
from requests.sessions import Session


log = logging.getLogger('mkdocs.markmap')


def download(base_path: Path, url: str, flat: bool = False, force_reload: bool = False) -> str:
    parsed_url: Url = parse_url(url)
    path: str = unquote(parsed_url.request_uri.split('?')[0])
    sub_path: str = os.path.basename(path) if flat else f'{parsed_url.hostname}{path}'
    file_path: Path = base_path / sub_path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    if force_reload or not file_path.exists():
        retries: Retry = Retry(connect=5, read=2, redirect=5)
        adapter: HTTPAdapter = HTTPAdapter(max_retries=retries)
        http: Session = Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        response: Response = http.get(url, allow_redirects=True, timeout=3.0)
        with open(file_path, 'wb') as fp:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:
                    fp.write(chunk)

    log.info(f'script downloaded: {url}')

    return str(sub_path)
