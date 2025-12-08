"""Tests for detect_module_runtime_mode function."""

from __future__ import annotations

from types import ModuleType

import pytest

import apathetic_utils as mod_apathetic_utils


def test_detect_module_runtime_mode_returns_package() -> None:
    """detect_module_runtime_mode should return 'package' for regular modules."""
    regular_module = ModuleType("regular_module")
    regular_module.__file__ = "/path/to/regular_module.py"

    result = mod_apathetic_utils.detect_module_runtime_mode(regular_module)
    assert result == "package", "Regular modules should be detected as 'package'"


def test_detect_module_runtime_mode_returns_stitched() -> None:
    """detect_module_runtime_mode should return 'stitched' for stitched modules."""
    stitched_module = ModuleType("stitched_module")
    stitched_module.__STITCHED__ = True  # type: ignore[attr-defined]

    result = mod_apathetic_utils.detect_module_runtime_mode(stitched_module)
    assert result == "stitched", "Modules with __STITCHED__ should be 'stitched'"


def test_detect_module_runtime_mode_returns_stitched_for_standalone() -> None:
    """detect_module_runtime_mode should return 'stitched' for __STANDALONE__."""
    standalone_module = ModuleType("standalone_module")
    standalone_module.__STANDALONE__ = True  # type: ignore[attr-defined]

    result = mod_apathetic_utils.detect_module_runtime_mode(standalone_module)
    assert result == "stitched", "Modules with __STANDALONE__ should be 'stitched'"


def test_detect_module_runtime_mode_returns_zipapp() -> None:
    """detect_module_runtime_mode should return 'zipapp' for zipapp modules."""
    zipapp_module = ModuleType("zipapp_module")
    zipapp_module.__file__ = "/path/to/archive.pyz/module.py"

    result = mod_apathetic_utils.detect_module_runtime_mode(zipapp_module)
    assert result == "zipapp", "Modules in .pyz should be detected as 'zipapp'"


def test_detect_module_runtime_mode_zipapp_ending_with_pyz() -> None:
    """detect_module_runtime_mode should detect .pyz files."""
    zipapp_module = ModuleType("zipapp_module")
    zipapp_module.__file__ = "/path/to/archive.pyz"

    result = mod_apathetic_utils.detect_module_runtime_mode(zipapp_module)
    assert result == "zipapp", "Files ending with .pyz should be 'zipapp'"


def test_detect_module_runtime_mode_prefers_marker_over_path() -> None:
    """detect_module_runtime_mode should prefer markers over path heuristics."""
    # Module with .pyz in path but __STITCHED__ marker
    conflicting_module = ModuleType("conflicting_module")
    conflicting_module.__file__ = "/path/to/archive.pyz/module.py"
    conflicting_module.__STITCHED__ = True  # type: ignore[attr-defined]

    result = mod_apathetic_utils.detect_module_runtime_mode(conflicting_module)
    assert result == "stitched", "Markers should take precedence over path heuristics"


def test_detect_module_runtime_mode_raises_on_non_module() -> None:
    """detect_module_runtime_mode should raise TypeError for non-modules."""
    with pytest.raises(TypeError, match="Expected ModuleType"):
        mod_apathetic_utils.detect_module_runtime_mode("not a module")  # type: ignore[arg-type]
