import json

from pathlib import Path

from .matcher import (
    _get_basic_matcher,
    _get_leftovers_matcher,
    _get_leftovers_slang_matcher,
    _get_preview_matcher,
    _get_slang_matcher,
)
from .validation import validate_dict_param, validate_file_contains_dict, validate_non_empty_string

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
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found at: {filepath}")

    contractions_data = json.loads(path.read_text(encoding="utf-8"))
    validate_file_contains_dict(contractions_data, filepath)
    add_custom_dict(contractions_data)


def load_custom_from_folder(folderpath: str) -> None:
    folder = Path(folderpath)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found at: {folderpath}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folderpath}")
    
    json_files = sorted(folder.glob("*.json"))
    
    if not json_files:
        raise ValueError(f"No JSON files found in folder: {folderpath}")
    
    for json_file in json_files:
        contractions_data = json.loads(json_file.read_text(encoding="utf-8"))
        validate_file_contains_dict(contractions_data, str(json_file))
        add_custom_dict(contractions_data)

