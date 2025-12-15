from __future__ import annotations

from typing import Any

try:
    import emoji  # type: ignore[import-not-found]
    EMOJI_AVAILABLE = True  # pragma: no cover
except ImportError:  # pragma: no cover
    EMOJI_AVAILABLE = False


def _contains_unicode_characters(text: str) -> bool:
    return any(ord(c) > 127 for c in text)


def _extract_emoji_data(text: str) -> list[dict[str, Any]]:
    return emoji.emoji_list(text)  # type: ignore[no-any-return]


def _convert_shortcode_to_text(shortcode: str) -> str:
    return shortcode.strip(":").replace("_", " ").replace("-", " ")


def _build_replacement_text(emoji_char: str) -> str:
    shortcode = emoji.demojize(emoji_char)
    text_version = _convert_shortcode_to_text(shortcode)
    return f" {text_version} "


def _replace_emoji_at_position(text: str, start: int, end: int, replacement: str) -> str:
    return text[:start] + replacement + text[end:]


def replace_emojis_with_text(text: str) -> str:
    if not EMOJI_AVAILABLE:  # pragma: no cover
        return text
    
    if not _contains_unicode_characters(text):
        return text
    
    emoji_data = _extract_emoji_data(text)
    
    if not emoji_data:
        return text
    
    result = text
    offset = 0
    
    for item in emoji_data:
        emoji_char = item["emoji"]
        start = item["match_start"] + offset
        end = item["match_end"] + offset
        
        replacement = _build_replacement_text(emoji_char)
        result = _replace_emoji_at_position(result, start, end, replacement)
        
        offset += len(replacement) - (end - start)
    
    return result
