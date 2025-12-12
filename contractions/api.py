import json

from .core import _get_ts_basic, _get_ts_leftovers, _get_ts_leftovers_slang, _get_ts_slang, _get_ts_view_window


def add(contraction: str, expansion: str):
    all_matchers = [_get_ts_basic, _get_ts_leftovers, _get_ts_slang, _get_ts_leftovers_slang]
    for matcher_getter in all_matchers:
        text_search = matcher_getter()
        text_search.add(contraction, expansion)
    _get_ts_view_window().add([contraction])


def add_dict(contractions_dict: dict[str, str]):
    all_matchers = [_get_ts_basic, _get_ts_leftovers, _get_ts_slang, _get_ts_leftovers_slang]
    for matcher_getter in all_matchers:
        text_search = matcher_getter()
        text_search.add(contractions_dict)
    _get_ts_view_window().add(list(contractions_dict))


def load_json(filepath: str):
    with open(filepath, encoding="utf-8") as json_file:
        contractions_data = json.load(json_file)
    add_dict(contractions_data)


def preview(text: str, flank: int):
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

