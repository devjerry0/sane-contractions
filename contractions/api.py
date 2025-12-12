import json

from .core import replacers, ts_view_window


def add(key, value):
    for ts in replacers.values():
        ts.add(key, value)
    ts_view_window.add([key])


def add_dict(dictionary):
    for ts in replacers.values():
        ts.add(dictionary)
    ts_view_window.add(list(dictionary.keys()))


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

    results = ts_view_window.findall(text)
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

