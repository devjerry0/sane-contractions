from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest

from contractions.emoji_support import EMOJI_AVAILABLE, replace_emojis_with_text


def test_emoji_library_detection() -> None:
    assert isinstance(EMOJI_AVAILABLE, bool)


def test_replace_emojis_without_library() -> None:
    if EMOJI_AVAILABLE:
        pytest.skip("Emoji library is installed, testing with-library path instead")
    
    text = "hello 🔥 world"
    result = replace_emojis_with_text(text)
    assert result == text


def test_replace_emojis_with_library() -> None:
    if not EMOJI_AVAILABLE:
        pytest.skip("Emoji library not installed, testing without-library path instead")
    
    result = replace_emojis_with_text("🔥")
    assert "fire" in result.lower() or "awesome" in result.lower()
    
    result = replace_emojis_with_text("💯")
    assert "hundred" in result.lower()


def test_emoji_integration_without_library() -> None:
    import contractions
    
    if EMOJI_AVAILABLE:
        pytest.skip("Emoji library is installed")
    
    result = contractions.expand("hello 🔥 world", emojis=True)
    assert "🔥" in result


def test_emoji_integration_with_library() -> None:
    import contractions
    
    if not EMOJI_AVAILABLE:
        pytest.skip("Emoji library not installed")
    
    result = contractions.expand("hello 🔥 world", emojis=True)
    assert "🔥" not in result
    assert "fire" in result.lower() or "awesome" in result.lower()
