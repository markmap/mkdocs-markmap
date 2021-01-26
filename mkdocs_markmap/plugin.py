import logging
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


# todo: move this to template
SCRIPT_CONTENT = """
const markdown{index} = '{content}';
const svg{index} = document.querySelector('#{tag_id}');
const root{index} = markmap_transformer.transform(markdown{index}).root;
var m{index} = markmap.Markmap.create(svg{index}, null, root{index});

m{index}.rescale(1).then(function() {{
    svg{index}.parentElement.style.height = (svg{index}.getBBox().height + 10) + "px";
    setTimeout(function() {{
        // todo: this is a dirty workaround to center the mindmap within svg
        while (svg{index}.firstChild) {{
            svg{index}.removeChild(svg{index}.lastChild);
        }}
        m{index} = markmap.Markmap.create(svg{index}, null, root{index});
    }}, 500);
}});
"""

# todo: move this to static file
STYLE_CONTENT = """
div.markmap {
    width: 100%;
    min-height: 1em;
    border: 1px solid grey;
}
.markmap > svg {
    width: 100%;
    height: 100%;
}
"""


class MarkmapPlugin(BasePlugin):
    """
    Plugin for markmap support
    """
    config_scheme: Tuple[Tuple[str, PluginType]] = (
        *(
            (f'{name}_version', PluginType(str, default=module.version))
            for name, module in MARKMAP.items()
        ),
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

    def on_post_page(self, output_content: str, config: Config, **kwargs) -> str:
        soup: BeautifulSoup = BeautifulSoup(output_content, 'html.parser')
        page: Page = kwargs.get('page')

        script_base_url: str = re.sub(r'[^/]+?/', '../', re.sub(r'/+?', '/', page.url)) + 'js/'
        js_path: Path = Path(config['site_dir']) / 'js'
        markmaps: ResultSet = soup.find_all('code', class_='language-markmap')
        if any(markmaps):
            for script_url in self.markmap.values():
                try:
                    src: str = script_base_url + download(js_path, script_url)
                except Exception as e:
                    log.error(f'unable to download script: {script_url}')
                    src = script_url
                script: Tag = soup.new_tag('script', src=src, type='text/javascript')
                soup.head.append(script)
            
            style: Tag = soup.new_tag('style', type='text/css')
            style.string = STYLE_CONTENT
            soup.head.append(style)

            script: Tag = soup.new_tag('script')
            script.string = 'const markmap_transformer = new markmap.Transformer();'
            soup.head.append(script)

        for index, markmap in enumerate(markmaps):
            tag_id: str = f'markmap-{index}'
            markmap.parent.name = 'div'
            markmap.parent['class'] = markmap.parent.get('class', []) + ['markmap']
            markmap.replaceWith(soup.new_tag(
                'svg', 
                id=tag_id, 
                attrs={'class': 'markmap'},
            ))
            script: Tag = soup.new_tag('script')
            script.string = SCRIPT_CONTENT.format(
                index=index,
                tag_id=tag_id,
                content=markmap.text.replace('\n', '\\n'),
            )
            soup.body.append(script)

        return str(soup)
