from __future__ import annotations

from .file_loader import load_dict_from_file, load_dict_from_folder
from .matcher import (
    _get_basic_matcher,
    _get_leftovers_matcher,
    _get_leftovers_slang_matcher,
    _get_preview_matcher,
    _get_slang_matcher,
)
from .validation import validate_dict_param, validate_non_empty_string

_ALL_MATCHERS = (_get_basic_matcher, _get_leftovers_matcher, _get_slang_matcher, _get_leftovers_slang_matcher)


def add_custom_contraction(contraction: str, expansion: str) -> None:
    validate_non_empty_string(contraction, "contraction")
    validate_non_empty_string(expansion, "expansion")

    for get_matcher in _ALL_MATCHERS:
        get_matcher().add(contraction, expansion)
    _get_preview_matcher().add([contraction])


def add_custom_dict(contractions_dict: dict[str, str]) -> None:
    validate_dict_param(contractions_dict, "contractions_dict")
    if not contractions_dict:
        return

    for get_matcher in _ALL_MATCHERS:
        get_matcher().add(contractions_dict)
    _get_preview_matcher().add(list(contractions_dict.keys()))


def load_custom_from_file(filepath: str) -> None:
    add_custom_dict(load_dict_from_file(filepath))


def load_custom_from_folder(folderpath: str) -> None:
    add_custom_dict(load_dict_from_folder(folderpath))

