import base64
import logging
from pathlib import Path
import re
from typing import Dict, Tuple

from bs4 import BeautifulSoup, ResultSet, Tag
from mkdocs.config.base import Config, load_config
from mkdocs.config.config_options import Type as PluginType
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from mkdocs_markmap.extension import MarkmapExtension

from .defaults import MARKMAP
from .utils import download


log = logging.getLogger("mkdocs.markmap")


STATICS_PATH: Path = Path(__file__).parent / "static_files"
STYLE_PATH: Path = STATICS_PATH / "mkdocs-markmap.css"
SCRIPT_PATH: Path = STATICS_PATH / "mkdocs-markmap.js"

VERSION_KEY = "{name}_version"


class MarkmapPlugin(BasePlugin):
    """
    Plugin for markmap support
    """
    config_scheme: Tuple[Tuple[str, PluginType]] = (
        *(
            (VERSION_KEY.format(name=name), PluginType(str, default=module.version))
            for name, module in MARKMAP.items()
        ),
        ("base_path", PluginType(str, default="docs")),
        ("encoding", PluginType(str, default="utf-8")),
        ("file_extension", PluginType(str, default=".mm.md")),
    )

    def __init__(self):
        self._markmap: Dict[str, str] = None

    @property
    def markmap(self) -> Dict[str, str]:
        """
        Provides all markmap libraries defined in mkdocs.yml (if any)
        """
        if self._markmap is None:
            self._markmap: Dict[str, str] = {}
            for name, module in MARKMAP.items():
                if self.config[VERSION_KEY.format(name=name)]:
                    self._markmap[name] = module.uri.format(self.config[VERSION_KEY.format(name=name)])

        return self._markmap

    def _load_scripts(self, soup: BeautifulSoup, script_base_url: str, js_path: Path) -> None:
        for script_url in self.markmap.values():
            if script_url.lower().startswith("http"):
                try:
                    src: str = script_base_url + download(js_path, script_url, extname=".js")
                except Exception as e:
                    log.error(f"unable to download script: {script_url}")
                    src = script_url

            else:
                log.info(f"static script detected: {script_url}")
                src = script_url

            script: Tag = soup.new_tag("script", src=src, type="text/javascript")
            soup.head.append(script)

    @staticmethod
    def _add_statics(soup: BeautifulSoup):
        statics = (
            (STYLE_PATH, "style", "text/css", "head"),
            (SCRIPT_PATH, "script", "text/javascript", "body"),
        )

        for path, tag_name, text_type, attribute in statics:
            tag: Tag = soup.new_tag(tag_name, type=text_type)
            with open(path, "r") as fp:
                tag.string = fp.read()
            getattr(soup, attribute).append(tag)

    def on_config(self, config: Config) -> Config:
        config["markdown_extensions"].append("markmap")
        config["mdx_configs"]["markmap"] = {
            key: value
            for key, value in config["plugins"].get("markmap").config.items()
            if key in MarkmapExtension.config_defaults
        }
        self.config["extra_javascript"] = config.get("extra_javascript", [])

        return config

    def on_post_page(self, html: str, page: Page, config: Config, **kwargs) -> str:
        if not getattr(page, "_found_markmap", False):
            log.debug(f"no markmap found: {page.file.name}")
            return html

        log.info(f"markmap found: {page.file.name}")
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        script_base_url: str = re.sub(r"/[^/]*$", "/", re.sub(r"[^/]+?/", "../", re.sub(r"/+?", "/", page.url))) + "js/"
        js_path: Path = Path(config["site_dir"]) / "js"
        self._load_scripts(soup, script_base_url, js_path)
        self._add_statics(soup)

        return str(soup)

    def on_page_content(self, html: str, page: Page, **kwargs) -> str:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        markmaps: ResultSet = soup.find_all(class_="language-markmap")
        setattr(page, "_found_markmap", any(markmaps))

        for index, markmap in enumerate(markmaps):
            markmap: Tag
            pre: Tag
            code: Tag
            if markmap.name == "pre":
                pre = markmap
                code = markmap.findChild("code")
            else:
                pre = markmap.parent
                code = markmap
            pre.name = "div"
            pre["class"] = pre.get("class", []) + ["mkdocs-markmap"]
            code.name = "markmap-data"
            code.attrs["hidden"] = "true"
            if not code.attrs.get("encoding"):
                # Encode content as base64 to avoid being handled by other plugins like KaTeX
                code.attrs["encoding"] = "base64"
                code.string = base64.b64encode(code.get_text().strip().encode()).decode()

        return str(soup)
