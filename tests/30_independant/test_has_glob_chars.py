# tests/30_independant/test_has_glob_chars.py
"""Tests for has_glob_chars utility function."""

import apathetic_utils as mod_autils


def test_has_glob_chars_with_star() -> None:
    """has_glob_chars() should return True for patterns with '*'."""
    # --- execute and verify ---
    assert mod_autils.has_glob_chars("*.py")
    assert mod_autils.has_glob_chars("file*.txt")
    assert mod_autils.has_glob_chars("**/*.py")


def test_has_glob_chars_with_question_mark() -> None:
    """has_glob_chars() should return True for patterns with '?'."""
    # --- execute and verify ---
    assert mod_autils.has_glob_chars("file?.txt")
    assert mod_autils.has_glob_chars("test_?.py")


def test_has_glob_chars_with_brackets() -> None:
    """has_glob_chars() should return True for patterns with '[]'."""
    # --- execute and verify ---
    assert mod_autils.has_glob_chars("file[0-9].txt")
    assert mod_autils.has_glob_chars("test_[abc].py")


def test_has_glob_chars_without_glob_chars() -> None:
    """has_glob_chars() should return False for patterns without glob characters."""
    # --- execute and verify ---
    assert not mod_autils.has_glob_chars("file.txt")
    assert not mod_autils.has_glob_chars("path/to/file")
    assert not mod_autils.has_glob_chars("")
    assert not mod_autils.has_glob_chars("normal_string")


def test_has_glob_chars_mixed() -> None:
    """has_glob_chars() should detect any glob character."""
    # --- execute and verify ---
    assert mod_autils.has_glob_chars("file*.txt")
    assert mod_autils.has_glob_chars("file?.txt")
    assert mod_autils.has_glob_chars("file[0-9].txt")
    assert mod_autils.has_glob_chars("**/*.py")


def test_has_glob_chars_false_return_path() -> None:
    """has_glob_chars() should return False when no glob chars found (line 62)."""
    # This test ensures line 62 (False return path) is covered
    # --- execute and verify ---
    result = mod_autils.has_glob_chars("plain_text_no_glob")
    assert result is False
    # Test with various strings that don't contain glob chars
    assert not mod_autils.has_glob_chars("path/to/file.txt")
    assert not mod_autils.has_glob_chars("normal_directory_name")
    assert not mod_autils.has_glob_chars("123456")
    assert not mod_autils.has_glob_chars("")
