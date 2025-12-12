from itertools import chain

from textsearch import TextSearch

from .loaders import load_all_contractions
from .state import _State

_TEXTSEARCH_MODE_NORM = "norm"
_TEXTSEARCH_MODE_OBJECT = "object"
_TEXTSEARCH_CASE_INSENSITIVE = "insensitive"


def _load_dicts():
    if _State.contractions_dict is not None:
        return

    _State.contractions_dict, _State.leftovers_dict, _State.slang_dict = load_all_contractions()


def _create_matcher(mode: str, *dicts: dict[str, str]) -> TextSearch:
    matcher = TextSearch(_TEXTSEARCH_CASE_INSENSITIVE, mode)
    for dictionary in dicts:
        matcher.add(dictionary)
    return matcher


def _get_basic_matcher():
    if _State.basic_matcher is None:
        _load_dicts()
        _State.basic_matcher = _create_matcher(_TEXTSEARCH_MODE_NORM, _State.contractions_dict)
    return _State.basic_matcher


def _get_leftovers_matcher():
    if _State.leftovers_matcher is None:
        _load_dicts()
        _State.leftovers_matcher = _create_matcher(
            _TEXTSEARCH_MODE_NORM,
            _State.contractions_dict,
            _State.leftovers_dict
        )
    return _State.leftovers_matcher


def _get_slang_matcher():
    if _State.slang_matcher is None:
        _load_dicts()
        _State.slang_matcher = _create_matcher(
            _TEXTSEARCH_MODE_NORM,
            _State.contractions_dict,
            _State.slang_dict
        )
    return _State.slang_matcher


def _get_leftovers_slang_matcher():
    if _State.leftovers_slang_matcher is None:
        _load_dicts()
        _State.leftovers_slang_matcher = _create_matcher(
            _TEXTSEARCH_MODE_NORM,
            _State.contractions_dict,
            _State.leftovers_dict,
            _State.slang_dict
        )
    return _State.leftovers_slang_matcher


def _get_preview_matcher():
    if _State.preview_matcher is None:
        _load_dicts()
        all_keys = list(chain(
            _State.contractions_dict.keys(),
            _State.leftovers_dict.keys(),
            _State.slang_dict.keys()
        ))
        _State.preview_matcher = TextSearch(_TEXTSEARCH_CASE_INSENSITIVE, _TEXTSEARCH_MODE_OBJECT)
        _State.preview_matcher.add(all_keys)
    return _State.preview_matcher


def fix(text: str, leftovers: bool = True, slang: bool = True) -> str:
    if leftovers and slang:
        return _get_leftovers_slang_matcher().replace(text)

    if leftovers:
        return _get_leftovers_matcher().replace(text)

    if slang:
        return _get_slang_matcher().replace(text)

    return _get_basic_matcher().replace(text)

