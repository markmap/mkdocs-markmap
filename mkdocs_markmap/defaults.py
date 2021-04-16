from typing import Dict

import attr


@attr.attrs
class JsModuleConfig(object):
    version: str = attr.attrib()
    uri: str = attr.attrib()

D3_LIB: JsModuleConfig = JsModuleConfig(
    version='6.7.0',
    uri='https://unpkg.com/d3@{}/dist/d3.min.js',
)

MARKMAP_LIB: JsModuleConfig = JsModuleConfig(
    version='0.11.5',
    uri='https://unpkg.com/markmap-lib@{}/dist/browser/index.min.js',
)

MARKMAP_VIEW: JsModuleConfig = JsModuleConfig(
    version='0.2.6',
    uri='https://unpkg.com/markmap-view@{}/dist/index.min.js',
)


MARKMAP: Dict[str, JsModuleConfig] = {
    'd3': D3_LIB,
    'lib': MARKMAP_LIB,
    'view': MARKMAP_VIEW,
}
