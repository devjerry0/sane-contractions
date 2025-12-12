import json
import pkgutil
from itertools import product

from textsearch import TextSearch

_contractions_dict: dict[str, str] | None = None
_leftovers_dict: dict[str, str] | None = None
_slang_dict: dict[str, str] | None = None
_unsafe_dict: dict[str, str] | None = None

_ts_leftovers: TextSearch | None = None
_ts_leftovers_slang: TextSearch | None = None
_ts_slang: TextSearch | None = None
_ts_basic: TextSearch | None = None
_ts_view_window: TextSearch | None = None


def _load_dicts():
    global _contractions_dict, _leftovers_dict, _slang_dict, _unsafe_dict  # noqa: PLW0603

    if _contractions_dict is not None:
        return

    json_data = pkgutil.get_data("contractions", "data/contractions_dict.json")
    assert json_data is not None
    _contractions_dict = json.loads(json_data.decode("utf-8"))

    json_data = pkgutil.get_data("contractions", "data/leftovers_dict.json")
    assert json_data is not None
    _leftovers_dict = json.loads(json_data.decode("utf-8"))

    json_data = pkgutil.get_data("contractions", "data/slang_dict.json")
    assert json_data is not None
    _slang_dict = json.loads(json_data.decode("utf-8"))

    for month in [
        "january", "february", "march", "april", "june", "july",
        "august", "september", "october", "november", "december",
    ]:
        _contractions_dict[month[:3] + "."] = month

    _contractions_dict |= {k.replace("'", "'"): v for k, v in _contractions_dict.items()}
    _leftovers_dict |= {k.replace("'", "'"): v for k, v in _leftovers_dict.items()}

    safety_keys = frozenset(
        ("he's", "he'll", "we'll", "we'd", "it's", "i'd", "we'd", "we're", "i'll", "who're", "o'")
    )

    _unsafe_dict = {}
    for k, v in _contractions_dict.items():
        k_lower = k.lower()
        if k_lower not in safety_keys and "'" in k:
            for comb in _get_combinations(k.split("'"), ["", "'"]):
                _unsafe_dict[comb] = v

    _slang_dict.update(_unsafe_dict)


def _get_combinations(tokens, joiners):
    option = [[x] for x in tokens]
    option = _intersperse(option, joiners)
    return ["".join(c) for c in product(*option)]


def _intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def _get_ts_basic():
    global _ts_basic  # noqa: PLW0603
    if _ts_basic is None:
        _load_dicts()
        _ts_basic = TextSearch("insensitive", "norm")
        _ts_basic.add(_contractions_dict)
    return _ts_basic


def _get_ts_leftovers():
    global _ts_leftovers  # noqa: PLW0603
    if _ts_leftovers is None:
        _load_dicts()
        _ts_leftovers = TextSearch("insensitive", "norm")
        _ts_leftovers.add(_contractions_dict)
        _ts_leftovers.add(_leftovers_dict)
    return _ts_leftovers


def _get_ts_slang():
    global _ts_slang  # noqa: PLW0603
    if _ts_slang is None:
        _load_dicts()
        _ts_slang = TextSearch("insensitive", "norm")
        _ts_slang.add(_contractions_dict)
        _ts_slang.add(_slang_dict)
    return _ts_slang


def _get_ts_leftovers_slang():
    global _ts_leftovers_slang  # noqa: PLW0603
    if _ts_leftovers_slang is None:
        _load_dicts()
        _ts_leftovers_slang = TextSearch("insensitive", "norm")
        _ts_leftovers_slang.add(_contractions_dict)
        _ts_leftovers_slang.add(_leftovers_dict)
        _ts_leftovers_slang.add(_slang_dict)
    return _ts_leftovers_slang


def _get_ts_view_window():
    global _ts_view_window  # noqa: PLW0603
    if _ts_view_window is None:
        _load_dicts()
        _ts_view_window = TextSearch("insensitive", "object")
        _ts_view_window.add([*_contractions_dict.keys(), *_leftovers_dict.keys(), *_slang_dict.keys()])
    return _ts_view_window


def fix(s: str, leftovers: bool = True, slang: bool = True) -> str:
    if leftovers and slang:
        return _get_ts_leftovers_slang().replace(s)

    if leftovers:
        return _get_ts_leftovers().replace(s)

    if slang:
        return _get_ts_slang().replace(s)

    return _get_ts_basic().replace(s)

