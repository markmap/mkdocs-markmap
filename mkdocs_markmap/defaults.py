from typing import Dict

import attr


@attr.attrs
class JsModuleConfig(object):
    version: str = attr.attrib()
    uri: str = attr.attrib()

D3_LIB: JsModuleConfig = JsModuleConfig(
    version="7",
    uri="https://unpkg.com/d3@{}",
)

MARKMAP_LIB: JsModuleConfig = JsModuleConfig(
    version="0.15.4",
    uri="https://unpkg.com/markmap-lib@{}",
)

MARKMAP_VIEW: JsModuleConfig = JsModuleConfig(
    version="0.15.4",
    uri="https://unpkg.com/markmap-view@{}",
)


MARKMAP: Dict[str, JsModuleConfig] = {
    "d3": D3_LIB,
    "lib": MARKMAP_LIB,
    "view": MARKMAP_VIEW,
}
