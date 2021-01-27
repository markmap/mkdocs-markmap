import logging
from mkdocs_markmap.extension import MarkmapExtension
import re
from pathlib import Path
from typing import Dict, Tuple

from bs4 import BeautifulSoup, ResultSet, Tag
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type as PluginType

from .defaults import MARKMAP
from .utils import download


log = logging.getLogger('mkdocs.markmap')


STATICS_PATH: Path = Path(__file__).parent / 'static_files'
STYLE_PATH: Path = STATICS_PATH / 'mkdocs-markmap.css'
SCRIPT_PATH: Path = STATICS_PATH / 'mkdocs-markmap.js'

class MarkmapPlugin(BasePlugin):
    """
    Plugin for markmap support
    """
    config_scheme: Tuple[Tuple[str, PluginType]] = (
        *(
            (f'{name}_version', PluginType(str, default=module.version))
            for name, module in MARKMAP.items()
        ),
        ('base_path', PluginType(str, default='docs')),
        ('encoding', PluginType(str, default='utf-8')),
        ('file_extension', PluginType(str, default='.mm.md')),
    )

    def __init__(self):
        self._markmap: Dict[str, str] = None

    @property
    def markmap(self) -> Dict[str, str]:
        """
        Provides all markmap libraries defined in mkdocs.yml (if any)
        """
        if self._markmap is None:            
            extra_javascript = self.config.get('extra_javascript', [])
            self._markmap: Dict[str, str] = {}
            for uri in extra_javascript:
                for name in MARKMAP.keys():
                    if f'markmap-{name}' in uri.lower():
                        self._markmap[name] = uri

            for name, module in MARKMAP.items():
                if name not in self._markmap:
                    self._markmap[name] = module.uri.format(self.config[f'{name}_version'])

        return self._markmap

    def _load_scripts(self, soup: BeautifulSoup, script_base_url: str, js_path: Path) -> None:
        for script_url in self.markmap.values():
            try:
                src: str = script_base_url + download(js_path, script_url)
            except Exception as e:
                log.error(f'unable to download script: {script_url}')
                src = script_url
            
            script: Tag = soup.new_tag('script', src=src, type='text/javascript')
            soup.head.append(script)

    @staticmethod
    def _add_statics(soup: BeautifulSoup):
        statics = (
            (STYLE_PATH, 'style', 'text/css', 'head'),
            (SCRIPT_PATH, 'script', 'text/javascript', 'body'),
        )

        for path, tag_name, text_type, attribute in statics:
            tag: Tag = soup.new_tag(tag_name, type=text_type)
            with open(path, 'r') as fp:
                tag.string = fp.read()
            getattr(soup, attribute).append(tag)    

    def on_config(self, config: Config) -> Config:
        config['markdown_extensions'].append('markmap')
        config['mdx_configs']['markmap'] = {
            key: value
            for key, value in config['plugins'].get('markmap').config.items()
            if key in MarkmapExtension.config_defaults
        }

        return config

    def on_post_page(self, output_content: str, config: Config, **kwargs) -> str:
        soup: BeautifulSoup = BeautifulSoup(output_content, 'html.parser')
        page: Page = kwargs.get('page')

        markmaps: ResultSet = soup.find_all('code', class_='language-markmap')
        if not any(markmaps):
            return output_content

        script_base_url: str = re.sub(r'[^/]+?/', '../', re.sub(r'/+?', '/', page.url)) + 'js/'
        js_path: Path = Path(config['site_dir']) / 'js'
        self._load_scripts(soup, script_base_url, js_path)
        self._add_statics(soup)

        for index, markmap in enumerate(markmaps):
            tag_id: str = f'markmap-{index}'
            markmap.parent.name = 'div'
            markmap.parent['class'] = markmap.parent.get('class', []) + ['mkdocs-markmap']
            markmap.parent['data-markdown']=markmap.text.replace('\n', '&#10;')
            markmap.replaceWith(soup.new_tag(
                'svg', 
                id=tag_id, 
                attrs={'class': 'markmap'},
            ))

        return str(soup)
