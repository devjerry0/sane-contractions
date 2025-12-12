import json

from .core import _get_ts_basic, _get_ts_leftovers, _get_ts_leftovers_slang, _get_ts_slang, _get_ts_view_window


def add(key, value):
    for getter in [_get_ts_basic, _get_ts_leftovers, _get_ts_slang, _get_ts_leftovers_slang]:
        ts = getter()
        ts.add(key, value)
    _get_ts_view_window().add([key])


def add_dict(dictionary):
    for getter in [_get_ts_basic, _get_ts_leftovers, _get_ts_slang, _get_ts_leftovers_slang]:
        ts = getter()
        ts.add(dictionary)
    _get_ts_view_window().add(list(dictionary))


def load_json(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    add_dict(data)


def preview(text, flank):
    """
    Return all contractions and their location before fix for manual check. Also provide a viewing window to quickly
    preview the contractions in the text.
    :param text: texture.
    :param flank: int number, control the size of the preview window. The window would be "flank-contraction-flank".
    :return: preview_items, a list includes all matched contractions and their locations.
    """
    if not isinstance(flank, int):
        raise TypeError("Argument flank must be integer!")

    results = _get_ts_view_window().findall(text)
    text_len = len(text)

    return [
        {
            "match": result.match,
            "start": result.start,
            "end": result.end,
            "viewing_window": text[max(0, result.start - flank):min(text_len, result.end + flank)]
        }
        for result in results
    ]

