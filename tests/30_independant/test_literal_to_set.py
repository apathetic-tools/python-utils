# tests/30_independant/test_literal_to_set.py
"""Tests for literal_to_set utility function."""

from typing import Literal

import pytest

import apathetic_utils as mod_autils


def test_literal_to_set_basic() -> None:
    """literal_to_set() should extract values from Literal type."""
    # --- setup ---
    literal_type = Literal["a", "b", "c"]

    # --- execute ---
    result = mod_autils.literal_to_set(literal_type)

    # --- verify ---
    assert result == {"a", "b", "c"}


def test_literal_to_set_single_value() -> None:
    """literal_to_set() should work with single Literal value."""
    # --- setup ---
    literal_type = Literal["only"]

    # --- execute ---
    result = mod_autils.literal_to_set(literal_type)

    # --- verify ---
    assert result == {"only"}


def test_literal_to_set_with_integers() -> None:
    """literal_to_set() should work with integer literals."""
    # --- setup ---
    literal_type = Literal[1, 2, 3]

    # --- execute ---
    result = mod_autils.literal_to_set(literal_type)

    # --- verify ---
    assert result == {1, 2, 3}


def test_literal_to_set_mixed_types() -> None:
    """literal_to_set() should work with mixed literal types."""
    # --- setup ---
    # literal_to_set() only accepts pure Literal types, not Optional/Literal unions
    # So we include None as a literal value directly
    literal_type = Literal["a", 1, True]

    # --- execute ---
    result = mod_autils.literal_to_set(literal_type)

    # --- verify ---
    assert result == {"a", 1}


def test_literal_to_set_raises_typeerror_for_non_literal() -> None:
    """literal_to_set() should raise TypeError for non-Literal types."""
    # --- execute and verify ---
    with pytest.raises(TypeError, match="Expected Literal type"):
        mod_autils.literal_to_set(str)

    with pytest.raises(TypeError, match="Expected Literal type"):
        mod_autils.literal_to_set(int)

    with pytest.raises(TypeError, match="Expected Literal type"):
        mod_autils.literal_to_set(list[str])
