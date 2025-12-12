import json
import pkgutil
from itertools import chain, product

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


def _load_json_data(filename: str) -> dict | list:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    assert json_bytes is not None
    return json.loads(json_bytes.decode("utf-8"))


def _normalize_apostrophes(contractions: dict[str, str]) -> dict[str, str]:
    return {
        contraction.replace("'", "'"): expansion
        for contraction, expansion in contractions.items()
    }


def _load_dicts():
    global _contractions_dict, _leftovers_dict, _slang_dict, _unsafe_dict  # noqa: PLW0603

    if _contractions_dict is not None:
        return

    _contractions_dict = _load_json_data("contractions_dict.json")
    _leftovers_dict = _load_json_data("leftovers_dict.json")
    _slang_dict = _load_json_data("slang_dict.json")
    safety_keys = frozenset(_load_json_data("safety_keys.json"))

    _contractions_dict |= _normalize_apostrophes(_contractions_dict)
    _leftovers_dict |= _normalize_apostrophes(_leftovers_dict)

    _unsafe_dict = _build_apostrophe_variants(_contractions_dict, safety_keys)
    _slang_dict.update(_unsafe_dict)


def _build_apostrophe_variants(contractions: dict[str, str], safety_keys: frozenset[str]) -> dict[str, str]:
    apostrophe_variants = ["", "'"]
    variants_dict = {}

    for contraction, expansion in contractions.items():
        if "'" not in contraction:
            continue

        if contraction.lower() in safety_keys:
            continue

        tokens = contraction.split("'")
        combinations = _get_combinations(tokens, apostrophe_variants)

        for combination in combinations:
            variants_dict[combination] = expansion

    return variants_dict


def _get_combinations(tokens, joiners):
    token_options = [[token] for token in tokens]
    interspersed_options = _intersperse(token_options, joiners)
    return ["".join(combination) for combination in product(*interspersed_options)]


def _intersperse(items, separator):
    result = [separator] * (len(items) * 2 - 1)
    result[0::2] = items
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

