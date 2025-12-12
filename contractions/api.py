import json
import os

from .core import _get_ts_basic, _get_ts_leftovers, _get_ts_leftovers_slang, _get_ts_slang, _get_ts_view_window

_MATCHER_GETTERS = (_get_ts_basic, _get_ts_leftovers, _get_ts_slang, _get_ts_leftovers_slang)


def add(contraction: str, expansion: str) -> None:
    for matcher_getter in _MATCHER_GETTERS:
        matcher_getter().add(contraction, expansion)
    _get_ts_view_window().add([contraction])


def add_dict(contractions_dict: dict[str, str]) -> None:
    if not contractions_dict:
        return

    for matcher_getter in _MATCHER_GETTERS:
        matcher_getter().add(contractions_dict)
    _get_ts_view_window().add(list(contractions_dict.keys()))


def load_json(filepath: str) -> None:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON file not found at: {filepath}")

    with open(filepath, encoding="utf-8") as json_file:
        contractions_data = json.load(json_file)

    if not isinstance(contractions_data, dict):
        raise ValueError(f"JSON file must contain a dictionary, got {type(contractions_data).__name__}")

    add_dict(contractions_data)


def preview(text: str, flank: int) -> list[dict[str, str | int]]:
    if not isinstance(flank, int):
        raise TypeError("Argument flank must be integer!")

    matched_contractions = _get_ts_view_window().findall(text)
    text_length = len(text)

    return [
        {
            "match": match.match,
            "start": match.start,
            "end": match.end,
            "viewing_window": text[max(0, match.start - flank):min(text_length, match.end + flank)]
        }
        for match in matched_contractions
    ]

