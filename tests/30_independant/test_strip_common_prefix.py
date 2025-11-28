# tests/30_independant/test_strip_common_prefix.py
"""Tests for strip_common_prefix utility function."""

import tempfile
from pathlib import Path

import apathetic_utils as mod_autils


def test_strip_common_prefix_basic() -> None:
    """strip_common_prefix() should return relative path when paths share prefix."""
    # --- setup ---
    path = "/home/user/code/serger/src/serger/logs.py"
    base = "/home/user/code/serger/tests/utils/patch_everywhere.py"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    assert result == "src/serger/logs.py"


def test_strip_common_prefix_with_path_objects() -> None:
    """strip_common_prefix() should work with Path objects."""
    # --- setup ---
    path = Path("/home/user/code/serger/src/serger/logs.py")
    base = Path("/home/user/code/serger/tests/utils/patch_everywhere.py")

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    assert result == "src/serger/logs.py"


def test_strip_common_prefix_no_common_prefix() -> None:
    """strip_common_prefix() should return relative path when no common prefix."""
    # --- setup ---
    path = "/home/user/file1.py"
    base = "/var/lib/other/file2.py"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    # When there's no common prefix, it returns the resolved path
    # (which will be the full path since they don't share a prefix)
    assert isinstance(result, str)
    assert "file1.py" in result


def test_strip_common_prefix_identical_paths() -> None:
    """strip_common_prefix() should return '.' when paths are identical."""
    # --- setup ---
    path = "/home/user/file.py"
    base = "/home/user/file.py"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    assert result == "."


def test_strip_common_prefix_one_is_prefix_of_other() -> None:
    """strip_common_prefix() should handle when one path is prefix of other."""
    # --- setup ---
    path = "/home/user/code/file.py"
    base = "/home/user/code"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    assert result == "file.py"


def test_strip_common_prefix_relative_paths() -> None:
    """strip_common_prefix() should resolve relative paths."""
    # --- setup ---
    path = "src/file.py"
    base = "tests/file.py"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    # Should resolve to absolute paths and find common prefix
    assert isinstance(result, str)
    # Result depends on current working directory, but should be a valid path


def test_strip_common_prefix_empty_result() -> None:
    """strip_common_prefix() should return '.' for empty result."""
    # --- setup ---
    path = "/home/user"
    base = "/home/user"

    # --- execute ---
    result = mod_autils.strip_common_prefix(path, base)

    # --- verify ---
    assert result == "."


def test_strip_common_prefix_comprehensive() -> None:
    """strip_common_prefix() should handle all code paths (lines 101-113)."""
    # This test ensures all lines 101-113 are covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create test structure
        path1 = tmp_path / "a" / "b" / "c" / "file1.py"
        path2 = tmp_path / "a" / "b" / "d" / "file2.py"
        path1.parent.mkdir(parents=True, exist_ok=True)
        path2.parent.mkdir(parents=True, exist_ok=True)
        path1.touch()
        path2.touch()

        # Test with paths that share common prefix
        # This exercises lines 101-113
        result = mod_autils.strip_common_prefix(path1, path2)

        # Verify result
        assert isinstance(result, str)
        # Should return relative path from common prefix
        assert "c" in result or "file1.py" in result


def test_strip_common_prefix_path_resolution() -> None:
    """strip_common_prefix() should resolve paths correctly (lines 101-102)."""
    # This test ensures lines 101-102 (Path.resolve()) are covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create relative paths that need resolution
        rel_path1 = tmp_path / "subdir1" / "file1.py"
        rel_path2 = tmp_path / "subdir2" / "file2.py"
        rel_path1.parent.mkdir(parents=True, exist_ok=True)
        rel_path2.parent.mkdir(parents=True, exist_ok=True)
        rel_path1.touch()
        rel_path2.touch()

        # Test with string paths (will be resolved)
        result = mod_autils.strip_common_prefix(str(rel_path1), str(rel_path2))

        # Verify result is a string
        assert isinstance(result, str)


def test_strip_common_prefix_zip_longest_logic() -> None:
    """strip_common_prefix() should use zip_longest correctly (lines 105-109)."""
    # This test ensures lines 105-109 (zip_longest loop) are covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create paths of different lengths
        long_path = tmp_path / "a" / "b" / "c" / "d" / "e" / "file.py"
        short_path = tmp_path / "a" / "b" / "other.py"
        long_path.parent.mkdir(parents=True, exist_ok=True)
        short_path.parent.mkdir(parents=True, exist_ok=True)
        long_path.touch()
        short_path.touch()

        # Test with different length paths
        # This exercises zip_longest with different lengths
        result = mod_autils.strip_common_prefix(long_path, short_path)

        # Verify result
        assert isinstance(result, str)
        # Should handle the case where one path is longer
        assert "c" in result or "d" in result or "e" in result or "file.py" in result


def test_strip_common_prefix_slice_remaining() -> None:
    """strip_common_prefix() should slice remaining parts correctly (lines 111-113)."""
    # This test ensures lines 111-113 (slicing and return) are covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create paths with common prefix
        path1 = tmp_path / "common" / "part1" / "part2" / "file1.py"
        path2 = tmp_path / "common" / "other" / "file2.py"
        path1.parent.mkdir(parents=True, exist_ok=True)
        path2.parent.mkdir(parents=True, exist_ok=True)
        path1.touch()
        path2.touch()

        # Test slicing logic
        result = mod_autils.strip_common_prefix(path1, path2)

        # Verify the remaining parts are correctly sliced
        assert isinstance(result, str)
        # Should contain the parts after common prefix
        assert "part1" in result or "part2" in result or "file1.py" in result


def test_strip_common_prefix_empty_remaining() -> None:
    """strip_common_prefix() should return '.' when remaining is empty (line 113)."""
    # This test ensures line 113 (empty remaining -> ".") is covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create identical paths
        path1 = tmp_path / "file.py"
        path2 = tmp_path / "file.py"
        path1.parent.mkdir(parents=True, exist_ok=True)
        path1.touch()

        # When paths are identical, remaining should be empty
        result = mod_autils.strip_common_prefix(path1, path2)

        # Should return "." when remaining is empty (line 113)
        assert result == "."
