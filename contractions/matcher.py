from __future__ import annotations

from itertools import chain

from textsearch import TextSearch

from .bootstrap import load_all_contractions
from .state import _State

_MODE_NORM = "norm"
_MODE_OBJECT = "object"
_CASE_INSENSITIVE = "insensitive"


def _load_dicts() -> None:
    if _State.contractions_dict is not None:
        return

    _State.contractions_dict, _State.leftovers_dict, _State.slang_dict = load_all_contractions()


def _create_matcher(mode: str, *dicts: dict[str, str]) -> TextSearch:
    matcher = TextSearch(_CASE_INSENSITIVE, mode)
    for dictionary in dicts:
        matcher.add(dictionary)
    return matcher


def _get_basic_matcher() -> TextSearch:
    if _State.basic_matcher is None:
        _load_dicts()
        assert _State.contractions_dict is not None
        _State.basic_matcher = _create_matcher(_MODE_NORM, _State.contractions_dict)
    return _State.basic_matcher


def _get_leftovers_matcher() -> TextSearch:
    if _State.leftovers_matcher is None:
        _load_dicts()
        assert _State.contractions_dict is not None
        assert _State.leftovers_dict is not None
        _State.leftovers_matcher = _create_matcher(
            _MODE_NORM,
            _State.contractions_dict,
            _State.leftovers_dict
        )
    return _State.leftovers_matcher


def _get_slang_matcher() -> TextSearch:
    if _State.slang_matcher is None:
        _load_dicts()
        assert _State.contractions_dict is not None
        assert _State.slang_dict is not None
        _State.slang_matcher = _create_matcher(
            _MODE_NORM,
            _State.contractions_dict,
            _State.slang_dict
        )
    return _State.slang_matcher


def _get_leftovers_slang_matcher() -> TextSearch:
    if _State.leftovers_slang_matcher is None:
        _load_dicts()
        assert _State.contractions_dict is not None
        assert _State.leftovers_dict is not None
        assert _State.slang_dict is not None
        _State.leftovers_slang_matcher = _create_matcher(
            _MODE_NORM,
            _State.contractions_dict,
            _State.leftovers_dict,
            _State.slang_dict
        )
    return _State.leftovers_slang_matcher


def _get_preview_matcher() -> TextSearch:
    if _State.preview_matcher is None:
        _load_dicts()
        assert _State.contractions_dict is not None
        assert _State.leftovers_dict is not None
        assert _State.slang_dict is not None
        all_keys = list(chain(
            _State.contractions_dict.keys(),
            _State.leftovers_dict.keys(),
            _State.slang_dict.keys()
        ))
        _State.preview_matcher = TextSearch(_CASE_INSENSITIVE, _MODE_OBJECT)
        _State.preview_matcher.add(all_keys)
    return _State.preview_matcher



