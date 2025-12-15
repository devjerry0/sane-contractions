from __future__ import annotations

try:
    import emoji  # type: ignore[import-not-found]
    EMOJI_AVAILABLE = True  # pragma: no cover
except ImportError:
    EMOJI_AVAILABLE = False


def replace_emojis_with_text(text: str) -> str:
    if not EMOJI_AVAILABLE:
        return text
    
    if not any(ord(c) > 127 for c in text):
        return text
    
    emoji_data = emoji.emoji_list(text)  # type: ignore[attr-defined] # pragma: no cover
    
    if not emoji_data:
        return text
    
    result = text
    offset = 0
    
    for item in emoji_data:  # pragma: no cover
        emoji_char = item["emoji"]
        start = item["match_start"] + offset
        end = item["match_end"] + offset
        
        shortcode = emoji.demojize(emoji_char)  # type: ignore[attr-defined]
        text_version = shortcode.strip(":").replace("_", " ").replace("-", " ")
        replacement = f" {text_version} "
        
        result = result[:start] + replacement + result[end:]
        offset += len(replacement) - (end - start)
    
    return result
