# tests/0_independant/test_pytest__runtime_mode_swap.py
"""Verify runtime mode swap functionality in conftest.py.

This test verifies that our unique runtime_mode swap functionality works
correctly. Our conftest.py uses runtime_swap() to allow tests to run against
either the installed package (src/apathetic_utils) or the standalone single-file script
(dist/apathetic_utils.py) based on the RUNTIME_MODE environment variable.

Verifies:
  - When RUNTIME_MODE=singlefile: All modules resolve to dist/apathetic_utils.py
  - When RUNTIME_MODE is unset (installed): All modules resolve to src/apathetic_utils/
  - Python's import cache (sys.modules) points to the correct sources
  - All submodules load from the expected location

This ensures our dual-runtime testing infrastructure functions correctly.
"""

import importlib
import inspect
import os
import pkgutil
import sys
from pathlib import Path

import apathetic_logging as mod_logging
import pytest

import apathetic_utils.runtime as amod_utils_runtime
from tests.utils import PROGRAM_PACKAGE, PROGRAM_SCRIPT, PROJ_ROOT


# --- convenience -----------------------------------------------------------

_runtime = amod_utils_runtime.ApatheticUtils_Internal_Runtime

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

safe_trace = mod_logging.makeSafeTrace("🪞")

# Debug: show which apathetic_logging module we're using in the test
mod_logging_source = getattr(mod_logging, "__file__", "unknown")
safe_trace(f"🔍 test: Using apathetic_logging from: {mod_logging_source}")

SRC_ROOT = PROJ_ROOT / "src"
DIST_ROOT = PROJ_ROOT / "dist"


def list_important_modules() -> list[str]:
    """Return all importable submodules under the package, if available."""
    important: list[str] = []
    if not hasattr(amod_utils_runtime, "__path__"):
        safe_trace("pkgutil.walk_packages skipped — standalone runtime (no __path__)")
        important.append(amod_utils_runtime.__name__)
    else:
        for _, name, _ in pkgutil.walk_packages(
            amod_utils_runtime.__path__,
            amod_utils_runtime.__name__ + ".",
        ):
            important.append(name)

    return important


def dump_snapshot(*, include_full: bool = False) -> None:
    """Prints a summary of key modules and (optionally) a full sys.modules dump."""
    mode: str = os.getenv("RUNTIME_MODE", "installed")

    safe_trace("========== SNAPSHOT ===========")
    safe_trace(f"RUNTIME_MODE={mode}")

    important_modules = list_important_modules()

    # Summary: the modules we care about most
    safe_trace("======= IMPORTANT MODULES =====")
    for name in important_modules:
        mod = sys.modules.get(name)
        if not mod:
            continue
        origin = getattr(mod, "__file__", None)
        safe_trace(f"  {name:<25} {origin}")

    if include_full:
        # Full origin dump
        safe_trace("======== OTHER MODULES ========")
        for name, mod in sorted(sys.modules.items()):
            if name in important_modules:
                continue
            origin = getattr(mod, "__file__", None)
            safe_trace(f"  {name:<38} {origin}")

    safe_trace("===============================")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_pytest_runtime_cache_integrity() -> None:  # noqa: PLR0912, PLR0915
    """Verify runtime mode swap correctly loads modules from expected locations.

    Ensures that modules imported at the top of test files resolve to the
    correct source based on RUNTIME_MODE:
    - singlefile mode: All modules must load from dist/apathetic_utils.py
    - installed mode: All modules must load from src/apathetic_utils/

    Also verifies that Python's import cache (sys.modules) doesn't have stale
    references pointing to the wrong runtime.
    """
    # --- setup ---
    mode = os.getenv("RUNTIME_MODE", "unknown")
    expected_script = DIST_ROOT / f"{PROGRAM_SCRIPT}.py"

    # In singlefile/zipapp mode, get the module from sys.modules to ensure we're
    # using the version from the standalone script/zipapp (which was loaded by
    # runtime_swap) rather than the one imported at the top of this file (which
    # might be from the installed package if it was imported before runtime_swap ran)
    if mode in ("singlefile", "zipapp") and f"{PROGRAM_PACKAGE}.runtime" in sys.modules:
        # Use the module from sys.modules, which should be from the standalone
        # script/zipapp
        amod_utils_runtime_actual = sys.modules[f"{PROGRAM_PACKAGE}.runtime"]
        # Check __file__ directly - for stitched modules, should point to
        # dist/apathetic_utils.py or dist/apathetic_utils.pyz
        utils_file_path = getattr(amod_utils_runtime_actual, "__file__", None)
        if utils_file_path:
            utils_file = str(utils_file_path)
        else:
            # Fall back to inspect.getsourcefile if __file__ is not available
            utils_file = str(inspect.getsourcefile(amod_utils_runtime_actual) or "")
    else:
        # Otherwise, use the module imported at the top of the file
        amod_utils_runtime_actual = amod_utils_runtime
        utils_file = str(inspect.getsourcefile(amod_utils_runtime_actual) or "")
    # --- execute ---
    safe_trace(f"RUNTIME_MODE={mode}")
    safe_trace(f"{PROGRAM_PACKAGE}.runtime  → {utils_file}")

    if os.getenv("TRACE"):
        dump_snapshot()
    # Access via main module to get the function from the namespace class
    runtime_mode = _runtime.detect_runtime_mode(PROGRAM_PACKAGE)

    if mode == "singlefile":
        # --- verify singlefile ---
        # what does the module itself think?
        assert runtime_mode == "standalone", (
            f"Expected runtime_mode='standalone' but got '{runtime_mode}'"
        )

        # exists
        assert expected_script.exists(), (
            f"Expected standalone script at {expected_script}"
        )

        # path peeks - in singlefile mode, apathetic_utils modules might be
        # imported from the installed package, but they should still detect
        # standalone mode correctly via sys.modules.get("apathetic_utils")
        # So we only check the path if the module is actually from dist/
        if utils_file.startswith(str(DIST_ROOT)):
            # Module is from standalone script, verify it's the right file
            assert Path(utils_file).samefile(expected_script), (
                f"{utils_file} should be same file as {expected_script}"
            )
        else:
            # Module is from installed package, but that's OK as long as
            # detect_runtime_mode() correctly returns "standalone"
            safe_trace(
                f"Note: apathetic_utils.version loaded from installed package "
                f"({utils_file}), but runtime_mode correctly detected as 'standalone'"
            )

        # troubleshooting info
        safe_trace(
            f"sys.modules['{PROGRAM_PACKAGE}'] = {sys.modules.get(PROGRAM_PACKAGE)}",
        )
        safe_trace(
            f"sys.modules['{PROGRAM_PACKAGE}.runtime']"
            f" = {sys.modules.get(f'{PROGRAM_PACKAGE}.runtime')}",
        )

    else:
        # --- verify module ---
        # what does the module itself think?
        assert runtime_mode != "standalone"

        # path peeks
        if mode == "zipapp":
            # In zipapp mode, module should be from the zipapp
            expected_zipapp = DIST_ROOT / f"{PROGRAM_SCRIPT}.pyz"
            assert utils_file is not None, (
                "utils_file should not be None in zipapp mode"
            )
            assert str(expected_zipapp) in str(utils_file), (
                f"{utils_file} not from zipapp {expected_zipapp}"
            )
        else:
            # In installed mode, module should be from src/
            assert utils_file is not None, (
                "utils_file should not be None in installed mode"
            )
            assert utils_file.startswith(str(SRC_ROOT)), f"{utils_file} not in src/"

    # --- verify both ---
    important_modules = list_important_modules()
    for submodule in important_modules:
        mod = importlib.import_module(f"{submodule}")
        # For zipapp modules, inspect.getsourcefile() may not work,
        # so use __file__ directly
        if mode == "zipapp":
            mod_file = getattr(mod, "__file__", None)
            if mod_file:
                path = Path(mod_file)
            else:
                path = Path(inspect.getsourcefile(mod) or "")
        else:
            path = Path(inspect.getsourcefile(mod) or "")
        if mode == "singlefile":
            assert path.samefile(expected_script), f"{submodule} loaded from {path}"
        elif mode == "zipapp":
            # In zipapp mode, modules should be from the zipapp
            expected_zipapp = DIST_ROOT / f"{PROGRAM_SCRIPT}.pyz"
            assert str(expected_zipapp) in str(path), (
                f"{submodule} not from zipapp: {path}"
            )
        else:
            assert path.is_relative_to(SRC_ROOT), f"{submodule} not in src/: {path}"


@pytest.mark.debug
def test_debug_dump_all_module_origins() -> None:
    """Debug helper: Dump all loaded module origins for forensic analysis.

    Useful when debugging import leakage, stale sys.modules cache, or runtime
    mode swap issues. Always fails intentionally to force pytest to show TRACE
    output.

    Usage:
        TRACE=1 poetry run pytest -k debug -s
        RUNTIME_MODE=singlefile TRACE=1 poetry run pytest -k debug -s
    """
    # --- verify ---

    # dump everything we know
    dump_snapshot(include_full=True)

    # show total module count for quick glance
    count = sum(1 for name in sys.modules if name.startswith(PROGRAM_PACKAGE))
    safe_trace(f"Loaded {count} {PROGRAM_PACKAGE} modules total")

    # force visible failure for debugging runs
    xmsg = f"Intentional fail — {count} {PROGRAM_PACKAGE} modules listed above."
    raise AssertionError(xmsg)
