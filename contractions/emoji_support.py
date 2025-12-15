from __future__ import annotations

try:
    import emoji  # type: ignore[import-not-found]
    EMOJI_AVAILABLE = True
except ImportError:
    EMOJI_AVAILABLE = False


def replace_emojis_with_text(text: str) -> str:
    if not EMOJI_AVAILABLE:
        return text
    
    def emoji_to_text(chars: str, data_dict: dict) -> str:
        shortcode = data_dict["en"]
        text_version = shortcode.strip(":").replace("_", " ").replace("-", " ")
        return f" {text_version} "
    
    return emoji.replace_emoji(text, replace=emoji_to_text)  # type: ignore[no-any-return]
