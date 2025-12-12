from itertools import chain

from textsearch import TextSearch

from .loaders import load_all_contractions

_contractions_dict: dict[str, str] | None = None
_leftovers_dict: dict[str, str] | None = None
_slang_dict: dict[str, str] | None = None

_ts_leftovers: TextSearch | None = None
_ts_leftovers_slang: TextSearch | None = None
_ts_slang: TextSearch | None = None
_ts_basic: TextSearch | None = None
_ts_view_window: TextSearch | None = None


def _load_dicts():
    global _contractions_dict, _leftovers_dict, _slang_dict  # noqa: PLW0603

    if _contractions_dict is not None:
        return

    _contractions_dict, _leftovers_dict, _slang_dict = load_all_contractions()


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
        all_contraction_keys = list(chain(
            _contractions_dict.keys(),
            _leftovers_dict.keys(),
            _slang_dict.keys()
        ))
        _ts_view_window.add(all_contraction_keys)
    return _ts_view_window


def fix(text: str, leftovers: bool = True, slang: bool = True) -> str:
    if leftovers and slang:
        return _get_ts_leftovers_slang().replace(text)

    if leftovers:
        return _get_ts_leftovers().replace(text)

    if slang:
        return _get_ts_slang().replace(text)

    return _get_ts_basic().replace(text)

