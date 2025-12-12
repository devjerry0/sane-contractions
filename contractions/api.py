import json
import os

from .core import (
    _get_basic_matcher,
    _get_leftovers_matcher,
    _get_leftovers_slang_matcher,
    _get_preview_matcher,
    _get_slang_matcher,
)
from .validation import validate_dict_param, validate_int_param, validate_non_empty_string

_ALL_MATCHERS = (
    _get_basic_matcher,
    _get_leftovers_matcher,
    _get_slang_matcher,
    _get_leftovers_slang_matcher,
)


def add(contraction: str, expansion: str) -> None:
    validate_non_empty_string(contraction, "contraction")
    validate_non_empty_string(expansion, "expansion")

    for get_matcher in _ALL_MATCHERS:
        get_matcher().add(contraction, expansion)
    _get_preview_matcher().add([contraction])


def add_dict(contractions_dict: dict[str, str]) -> None:
    validate_dict_param(contractions_dict, "contractions_dict")
    if not contractions_dict:
        return

    for get_matcher in _ALL_MATCHERS:
        get_matcher().add(contractions_dict)
    _get_preview_matcher().add(list(contractions_dict.keys()))


def load_json(filepath: str) -> None:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON file not found at: {filepath}")

    with open(filepath, encoding="utf-8") as json_file:
        contractions_data = json.load(json_file)

    if not isinstance(contractions_data, dict):
        raise ValueError(f"JSON file must contain a dictionary, got {type(contractions_data).__name__}")

    add_dict(contractions_data)


def preview(text: str, context_chars: int) -> list[dict[str, str | int]]:
    validate_int_param(context_chars, "context_chars")

    matched_contractions = _get_preview_matcher().findall(text)
    text_length = len(text)

    return [
        {
            "match": match.match,
            "start": match.start,
            "end": match.end,
            "viewing_window": text[max(0, match.start - context_chars):min(text_length, match.end + context_chars)]
        }
        for match in matched_contractions
    ]

