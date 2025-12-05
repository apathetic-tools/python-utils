# tests/90_integration/test_zipapp_import_semantics.py
"""Integration tests for zipapp import semantics.

These tests verify that when the project is built using zipbundler (zipapp),
the import semantics work correctly:
- Can import and use the module from zipapp format
- Exported constants and classes are accessible

These are project-specific tests that verify our code works correctly
when built with zipbundler (not testing zipbundler itself).
"""

import subprocess
import sys
import zipfile

import pytest

import apathetic_utils
from tests.utils.constants import PROJ_ROOT


# Runtime mode marker: only run this test file in zipapp mode
__runtime_mode__ = "zipapp"


def test_zipapp_import_semantics() -> None:
    """Test that zipapp builds maintain correct import semantics.

    This test verifies our project code works correctly when built with zipbundler:
    1. Builds apathetic_utils as a zipapp using zipbundler (from project root)
    2. Imports from the zipapp and verifies import semantics work correctly:
       - Can import and use the module from zipapp format
       - Exported constants and classes are accessible

    This verifies our project configuration and code work correctly with zipbundler.
    """
    # --- setup ---
    # Build the project's zipapp
    zipapp_file = PROJ_ROOT / "dist" / "apathetic_utils.pyz"

    # Ensure dist directory exists
    zipapp_file.parent.mkdir(parents=True, exist_ok=True)

    # --- execute: build zipapp ---
    zipbundler_cmd = apathetic_utils.find_zipbundler()
    result = subprocess.run(  # noqa: S603
        [
            *zipbundler_cmd,
            "-m",
            "apathetic_utils",
            "-o",
            str(zipapp_file),
            "-q",
            ".",
        ],
        cwd=PROJ_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        pytest.fail(
            f"zipbundler failed with return code {result.returncode}.\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    if not zipapp_file.exists():
        pytest.fail(f"Zipapp file not created at {zipapp_file}")

    # Verify it's a valid zip file
    assert zipfile.is_zipfile(zipapp_file), "Zipapp should be a valid zip file"

    # --- execute: import from zipapp ---
    # Add zipapp to sys.path and import
    sys.path.insert(0, str(zipapp_file))

    try:
        # Import apathetic_utils from the zipapp
        import apathetic_utils as zipapp_apathetic_utils  # noqa: PLC0415

        # --- verify: import semantics ---
        # Verify apathetic_utils namespace is available
        assert hasattr(zipapp_apathetic_utils, "apathetic_utils"), (
            "apathetic_utils.apathetic_utils should be available"
        )

        apathetic_utils_ns = zipapp_apathetic_utils.apathetic_utils
        # Verify it's a class (the namespace class)
        assert isinstance(apathetic_utils_ns, type), (
            "apathetic_utils should be a class (namespace)"
        )

    finally:
        # Clean up sys.path
        if str(zipapp_file) in sys.path:
            sys.path.remove(str(zipapp_file))
        # Clean up imported modules
        if "apathetic_utils" in sys.modules:
            del sys.modules["apathetic_utils"]
