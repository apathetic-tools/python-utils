# tests/30_independant/test_fnmatchcase_portable.py
"""Tests for fnmatchcase_portable utility function."""

from types import SimpleNamespace

import pytest

import apathetic_utils as mod_autils
from tests.utils.constants import PATCH_STITCH_HINTS, PROGRAM_PACKAGE


def test_fnmatchcase_portable_non_recursive_pattern() -> None:
    """fnmatchcase_portable() should use fnmatchcase for non-recursive patterns."""
    # This test ensures line 115 (early return for non-** patterns) is covered
    # --- execute and verify ---
    # Non-recursive patterns should use fnmatchcase directly
    assert mod_autils.fnmatchcase_portable("file.py", "*.py")
    assert mod_autils.fnmatchcase_portable("src/file.py", "src/*.py")
    assert not mod_autils.fnmatchcase_portable("file.txt", "*.py")
    assert mod_autils.fnmatchcase_portable("test_x.py", "test_?.py")


def test_fnmatchcase_portable_python_311_plus() -> None:
    """fnmatchcase_portable() should use backport for ** patterns."""
    # This test ensures ** patterns use the backport regex compiler
    # **/*.py should match files in subdirectories
    assert mod_autils.fnmatchcase_portable("src/utils/file.py", "src/**/*.py")
    assert mod_autils.fnmatchcase_portable("deep/nested/file.py", "**/*.py")
    # **/*.py requires at least one directory level, so src/file.py doesn't match
    assert not mod_autils.fnmatchcase_portable("src/file.py", "src/**/*.py")


def test_fnmatchcase_portable_recursive_pattern_py310(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """fnmatchcase_portable() should use backport for ** patterns on Python 3.10."""
    # --- setup ---
    # Force Python 3.10
    fake_sys = SimpleNamespace(version_info=(3, 10, 0))
    mod_autils.patch_everywhere(
        monkeypatch,
        mod_autils.apathetic_utils,
        "get_sys_version_info",
        lambda: fake_sys.version_info,
        PROGRAM_PACKAGE,
        PATCH_STITCH_HINTS,
    )

    # --- execute and verify ---
    # On Python 3.10, ** patterns should use backport
    # **/*.py should match files in subdirectories
    assert mod_autils.fnmatchcase_portable("src/utils/file.py", "src/**/*.py")
    assert mod_autils.fnmatchcase_portable("deep/nested/file.py", "**/*.py")
    # **/*.py requires at least one directory level
    assert not mod_autils.fnmatchcase_portable("src/file.py", "src/**/*.py")
    assert not mod_autils.fnmatchcase_portable("file.txt", "**/*.py")
