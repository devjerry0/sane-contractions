from __future__ import annotations

from .matcher import (
    _get_basic_matcher,
    _get_leftovers_matcher,
    _get_leftovers_slang_matcher,
    _get_preview_matcher,
    _get_slang_matcher,
)
from .validation import validate_int_param, validate_string_param


def expand(text: str, leftovers: bool = True, slang: bool = True) -> str:
    validate_string_param(text, "text")

    if leftovers and slang:
        return _get_leftovers_slang_matcher().replace(text)

    if leftovers:
        return _get_leftovers_matcher().replace(text)

    if slang:
        return _get_slang_matcher().replace(text)

    return _get_basic_matcher().replace(text)

def _extract_viewing_window(text: str, match_start: int, match_end: int, context_chars: int) -> str:
    text_length = len(text)
    window_start = max(0, match_start - context_chars)
    window_end = min(text_length, match_end + context_chars)
    
    return text[window_start:window_end]

def preview(text: str, context_chars: int) -> list[dict[str, str | int]]:
    validate_int_param(context_chars, "context_chars")

    matched_contractions = _get_preview_matcher().findall(text)

    return [
        {
            "match": match.match,
            "start": match.start,
            "end": match.end,
            "viewing_window": _extract_viewing_window(text, match.start, match.end, context_chars)
        }
        for match in matched_contractions
    ]

