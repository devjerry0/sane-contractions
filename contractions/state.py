from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from textsearch import TextSearch


class _State:
    contractions_dict: dict[str, str] | None = None
    leftovers_dict: dict[str, str] | None = None
    slang_dict: dict[str, str] | None = None

    basic_matcher: TextSearch | None = None
    leftovers_matcher: TextSearch | None = None
    slang_matcher: TextSearch | None = None
    leftovers_slang_matcher: TextSearch | None = None
    preview_matcher: TextSearch | None = None

