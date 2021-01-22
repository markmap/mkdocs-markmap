import os
from urllib.request import Request, urlopen


def is_lib_uri(uri: str, lib_name: str) -> str:
    "Check that uri contains library name"
    return lib_name.lower() in uri.lower()
