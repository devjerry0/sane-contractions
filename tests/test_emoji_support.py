from __future__ import annotations

from contractions.emoji_support import EMOJI_AVAILABLE, replace_emojis_with_text


def test_emoji_library_detection() -> None:
    assert isinstance(EMOJI_AVAILABLE, bool)


def test_replace_emojis_without_library() -> None:
    if EMOJI_AVAILABLE:
        return
    
    text = "hello 🔥 world"
    result = replace_emojis_with_text(text)
    assert result == text


def test_replace_emojis_with_library() -> None:
    if not EMOJI_AVAILABLE:
        return
    
    result = replace_emojis_with_text("🔥")
    assert "fire" in result.lower() or "awesome" in result.lower()
    
    result = replace_emojis_with_text("💯")
    assert "hundred" in result.lower()
