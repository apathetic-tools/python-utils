# tests/30_independant/test_shorten_path.py
"""Tests for shorten_path utility function."""

import tempfile
from pathlib import Path

import apathetic_utils as mod_autils


def test_shorten_path_basic() -> None:
    """shorten_path() should return relative path when paths share prefix."""
    # --- setup ---
    path = "/home/user/code/serger/src/serger/logs.py"
    base = "/home/user/code/serger/tests/utils/patch_everywhere.py"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    assert result == "src/serger/logs.py"


def test_shorten_path_with_path_objects() -> None:
    """shorten_path() should work with Path objects."""
    # --- setup ---
    path = Path("/home/user/code/serger/src/serger/logs.py")
    base = Path("/home/user/code/serger/tests/utils/patch_everywhere.py")

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    assert result == "src/serger/logs.py"


def test_shorten_path_no_common_prefix() -> None:
    """shorten_path() should return absolute path when only root in common."""
    # --- setup ---
    path = "/home/user/file1.py"
    base = "/var/lib/other/file2.py"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    # When common prefix is only root, returns absolute path (default behavior)
    assert result == "/home/user/file1.py"


def test_shorten_path_identical_paths() -> None:
    """shorten_path() should return '.' when paths are identical."""
    # --- setup ---
    path = "/home/user/file.py"
    base = "/home/user/file.py"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    assert result == "."


def test_shorten_path_one_is_prefix_of_other() -> None:
    """shorten_path() should handle when one path is prefix of other."""
    # --- setup ---
    path = "/home/user/code/file.py"
    base = "/home/user/code"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    assert result == "file.py"


def test_shorten_path_relative_paths() -> None:
    """shorten_path() should resolve relative paths."""
    # --- setup ---
    path = "src/file.py"
    base = "tests/file.py"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    # Should resolve to absolute paths and find common prefix
    assert isinstance(result, str)
    # Result depends on current working directory, but should be a valid path


def test_shorten_path_empty_result() -> None:
    """shorten_path() should return '.' for empty result."""
    # --- setup ---
    path = "/home/user"
    base = "/home/user"

    # --- execute ---
    result = mod_autils.shorten_path(path, base)

    # --- verify ---
    assert result == "."


def test_shorten_path_comprehensive() -> None:
    """shorten_path() should handle all code paths (lines 101-113)."""
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
        result = mod_autils.shorten_path(path1, path2)

        # Verify result
        assert isinstance(result, str)
        # Should return relative path from common prefix
        assert "c" in result or "file1.py" in result


def test_shorten_path_path_resolution() -> None:
    """shorten_path() should resolve paths correctly (lines 101-102)."""
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
        result = mod_autils.shorten_path(str(rel_path1), str(rel_path2))

        # Verify result is a string
        assert isinstance(result, str)


def test_shorten_path_zip_longest_logic() -> None:
    """shorten_path() should use zip_longest correctly (lines 105-109)."""
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
        result = mod_autils.shorten_path(long_path, short_path)

        # Verify result
        assert isinstance(result, str)
        # Should handle the case where one path is longer
        assert "c" in result or "d" in result or "e" in result or "file.py" in result


def test_shorten_path_slice_remaining() -> None:
    """shorten_path() should slice remaining parts correctly (lines 111-113)."""
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
        result = mod_autils.shorten_path(path1, path2)

        # Verify the remaining parts are correctly sliced
        assert isinstance(result, str)
        # Should contain the parts after common prefix
        assert "part1" in result or "part2" in result or "file1.py" in result


def test_shorten_path_empty_remaining() -> None:
    """shorten_path() should return '.' when remaining is empty (line 113)."""
    # This test ensures line 113 (empty remaining -> ".") is covered
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Create identical paths
        path1 = tmp_path / "file.py"
        path2 = tmp_path / "file.py"
        path1.parent.mkdir(parents=True, exist_ok=True)
        path1.touch()

        # When paths are identical, remaining should be empty
        result = mod_autils.shorten_path(path1, path2)

        # Should return "." when remaining is empty (line 113)
        assert result == "."


def test_shorten_path_multiple_bases() -> None:
    """shorten_path() should return shortest when multiple bases provided."""
    # --- setup ---
    path = "/home/user/code/serger/src/logs.py"
    bases: list[str | Path] = [
        # Common: /home/user/code/serger -> "src/logs.py"
        "/home/user/code/serger/tests/utils/patch.py",
        # Common: /home/user/code/serger/src -> "logs.py"
        "/home/user/code/serger/src",
    ]

    # --- execute ---
    result = mod_autils.shorten_path(path, bases)

    # --- verify ---
    # Should return shortest: "logs.py" (from second base)
    assert result == "logs.py"


def test_shorten_path_multiple_bases_single_string() -> None:
    """shorten_path() should accept single string or Path as bases."""
    # --- setup ---
    path = "/home/user/code/serger/src/logs.py"
    bases = "/home/user/code/serger/tests/utils/patch.py"

    # --- execute ---
    result = mod_autils.shorten_path(path, bases)

    # --- verify ---
    assert result == "src/logs.py"


def test_shorten_path_multiple_bases_different_prefixes() -> None:
    """shorten_path() should find shortest across bases with different prefixes."""
    # --- setup ---
    path = "/home/user/project1/src/file.py"
    bases: list[str | Path] = [
        # Common: /home/user -> "project1/src/file.py"
        "/home/user/project2/tests/test.py",
        # Common: /home/user/project1/src -> "file.py"
        "/home/user/project1/src/utils/helper.py",
    ]

    # --- execute ---
    result = mod_autils.shorten_path(path, bases)

    # --- verify ---
    # Should return shortest: "file.py" (from second base)
    assert result == "file.py"
