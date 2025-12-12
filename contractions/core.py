from itertools import chain

from textsearch import TextSearch

from .loaders import load_all_contractions


class _State:
    contractions_dict: dict[str, str] | None = None
    leftovers_dict: dict[str, str] | None = None
    slang_dict: dict[str, str] | None = None

    ts_leftovers: TextSearch | None = None
    ts_leftovers_slang: TextSearch | None = None
    ts_slang: TextSearch | None = None
    ts_basic: TextSearch | None = None
    ts_view_window: TextSearch | None = None


def _load_dicts():
    if _State.contractions_dict is not None:
        return

    _State.contractions_dict, _State.leftovers_dict, _State.slang_dict = load_all_contractions()


def _get_ts_basic():
    if _State.ts_basic is None:
        _load_dicts()
        _State.ts_basic = TextSearch("insensitive", "norm")
        _State.ts_basic.add(_State.contractions_dict)
    return _State.ts_basic


def _get_ts_leftovers():
    if _State.ts_leftovers is None:
        _load_dicts()
        _State.ts_leftovers = TextSearch("insensitive", "norm")
        _State.ts_leftovers.add(_State.contractions_dict)
        _State.ts_leftovers.add(_State.leftovers_dict)
    return _State.ts_leftovers


def _get_ts_slang():
    if _State.ts_slang is None:
        _load_dicts()
        _State.ts_slang = TextSearch("insensitive", "norm")
        _State.ts_slang.add(_State.contractions_dict)
        _State.ts_slang.add(_State.slang_dict)
    return _State.ts_slang


def _get_ts_leftovers_slang():
    if _State.ts_leftovers_slang is None:
        _load_dicts()
        _State.ts_leftovers_slang = TextSearch("insensitive", "norm")
        _State.ts_leftovers_slang.add(_State.contractions_dict)
        _State.ts_leftovers_slang.add(_State.leftovers_dict)
        _State.ts_leftovers_slang.add(_State.slang_dict)
    return _State.ts_leftovers_slang


def _get_ts_view_window():
    if _State.ts_view_window is None:
        _load_dicts()
        _State.ts_view_window = TextSearch("insensitive", "object")
        all_contraction_keys = list(chain(
            _State.contractions_dict.keys(),
            _State.leftovers_dict.keys(),
            _State.slang_dict.keys()
        ))
        _State.ts_view_window.add(all_contraction_keys)
    return _State.ts_view_window


def fix(text: str, leftovers: bool = True, slang: bool = True) -> str:
    if leftovers and slang:
        return _get_ts_leftovers_slang().replace(text)

    if leftovers:
        return _get_ts_leftovers().replace(text)

    if slang:
        return _get_ts_slang().replace(text)

    return _get_ts_basic().replace(text)

