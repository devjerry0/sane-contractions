from __future__ import annotations

from .extension import add_custom_contraction, add_custom_dict, load_custom_from_file, load_custom_from_folder
from .processor import expand as _expand
from .processor import preview as _preview


def expand(text: str, leftovers: bool = True, slang: bool = True) -> str:
    return _expand(text, leftovers, slang)


def preview(text: str, context_chars: int) -> list[dict[str, str | int]]:
    return _preview(text, context_chars)


def add(contraction: str, expansion: str) -> None:
    return add_custom_contraction(contraction, expansion)


def add_dict(contractions_dict: dict[str, str]) -> None:
    return add_custom_dict(contractions_dict)


def load_file(filepath: str) -> None:
    return load_custom_from_file(filepath)


def load_folder(folderpath: str) -> None:
    return load_custom_from_folder(folderpath)


e = expand
p = preview

