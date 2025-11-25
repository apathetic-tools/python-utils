# tests/conftest.py
"""Shared test setup for project.

Each pytest run now targets a single runtime mode:
- Normal mode (default): uses src/apathetic_utils
- Standalone mode: uses dist/apathetic_utils.py when RUNTIME_MODE=singlefile
- Zipapp mode: uses dist/apathetic_utils.pyz when RUNTIME_MODE=zipapp

Switch mode with: RUNTIME_MODE=singlefile pytest or RUNTIME_MODE=zipapp pytest
"""

import logging
import os
from collections.abc import Generator

import pytest

from tests.utils import make_safe_trace, runtime_swap
from tests.utils.log_fixtures import (
    direct_logger,
    module_logger,
)


# These fixtures are intentionally re-exported so pytest can discover them.
__all__ = [
    "direct_logger",
    "module_logger",
]

safe_trace = make_safe_trace("⚡️")

# early jank hook
runtime_swap()

# Import after runtime_swap to ensure we get the right module
import apathetic_utils as mod_alogs  # noqa: E402
import apathetic_utils.registry_data as mod_registry  # noqa: E402


@pytest.fixture(autouse=True)
def reset_logger_class_and_registry() -> Generator[None, None, None]:
    """Reset logger class and registry state before and after each test.

    This ensures that tests that set a custom logger class or modify registry
    state don't affect subsequent tests. This is the lowest common denominator
    needed by almost all tests.
    """
    # Save original state
    original_logger_class = logging.getLoggerClass()
    _registry = mod_registry.ApatheticLogging_Internal_RegistryData
    original_name = _registry.registered_internal_logger_name
    original_default = _registry.registered_internal_default_log_level
    original_env_vars = _registry.registered_internal_log_level_env_vars
    original_compatibility_mode = _registry.registered_internal_compatibility_mode

    # Clear any existing loggers from the registry
    _logging_utils = mod_alogs.apathetic_utils
    logger_names = list(logging.Logger.manager.loggerDict.keys())
    for logger_name in logger_names:
        _logging_utils.removeLogger(logger_name)

    # Reset to defaults before test
    logging.setLoggerClass(mod_alogs.Logger)
    mod_alogs.Logger.extendLoggingModule()
    # Explicitly restore standard level names to ensure they're registered
    # even if a previous test added conflicting custom level names
    _constants = mod_alogs.apathetic_utils
    mod_alogs.Logger.addLevelName(_constants.TEST_LEVEL, "TEST")
    mod_alogs.Logger.addLevelName(_constants.TRACE_LEVEL, "TRACE")
    mod_alogs.Logger.addLevelName(_constants.DETAIL_LEVEL, "DETAIL")
    mod_alogs.Logger.addLevelName(_constants.MINIMAL_LEVEL, "MINIMAL")
    mod_alogs.Logger.addLevelName(_constants.SILENT_LEVEL, "SILENT")
    _registry.registered_internal_logger_name = None
    _registry.registered_internal_default_log_level = None
    _registry.registered_internal_log_level_env_vars = None
    _registry.registered_internal_compatibility_mode = None

    yield

    # Clear loggers again after test
    logger_names = list(logging.Logger.manager.loggerDict.keys())
    for logger_name in logger_names:
        _logging_utils.removeLogger(logger_name)

    # Restore original state after test
    logging.setLoggerClass(original_logger_class)
    mod_alogs.Logger.extendLoggingModule()
    # Explicitly restore standard level names to ensure they're registered
    # even if the test added conflicting custom level names
    mod_alogs.Logger.addLevelName(_constants.TEST_LEVEL, "TEST")
    mod_alogs.Logger.addLevelName(_constants.TRACE_LEVEL, "TRACE")
    mod_alogs.Logger.addLevelName(_constants.DETAIL_LEVEL, "DETAIL")
    mod_alogs.Logger.addLevelName(_constants.MINIMAL_LEVEL, "MINIMAL")
    mod_alogs.Logger.addLevelName(_constants.SILENT_LEVEL, "SILENT")
    _registry.registered_internal_logger_name = original_name
    _registry.registered_internal_default_log_level = original_default
    _registry.registered_internal_log_level_env_vars = original_env_vars
    _registry.registered_internal_compatibility_mode = original_compatibility_mode


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _mode() -> str:
    return os.getenv("RUNTIME_MODE", "installed")


def _filter_debug_tests(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    # detect if the user is filtering for debug tests
    keywords = config.getoption("-k") or ""
    running_debug = "debug" in keywords.lower()

    if running_debug:
        return  # user explicitly requested them, don't skip

    for item in items:
        if "debug" in item.keywords:
            item.add_marker(
                pytest.mark.skip(reason="Skipped debug test (use -k debug to run)"),
            )


def _filter_runtime_mode_tests(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    mode = _mode()
    # Check if verbose mode is enabled (verbose > 0 means user wants verbose output)
    verbose = getattr(config.option, "verbose", 0)
    is_quiet = verbose <= 0

    # Only track included tests if not in quiet mode (for later reporting)
    included_map: dict[str, int] | None = {} if not is_quiet else None
    root = str(config.rootpath)
    testpaths: list[str] = config.getini("testpaths") or []

    # Identify mode-specific files by a custom variable defined at module scope
    for item in list(items):
        mod = item.getparent(pytest.Module)
        if mod is None or not hasattr(mod, "obj"):
            continue

        runtime_marker = getattr(mod.obj, "__runtime_mode__", None)

        if runtime_marker and runtime_marker != mode:
            items.remove(item)
            continue

        # Only track if not in quiet mode
        if runtime_marker and runtime_marker == mode and included_map is not None:
            file_path = str(item.fspath)
            # Make path relative to project root dir
            if file_path.startswith(root):
                file_path = os.path.relpath(file_path, root)
                for tp in testpaths:
                    if file_path.startswith(tp.rstrip("/") + os.sep):
                        file_path = file_path[len(tp.rstrip("/") + os.sep) :]
                        break

            included_map[file_path] = included_map.get(file_path, 0) + 1

    # Store results for later reporting (only if not in quiet mode)
    if included_map is not None:
        config._included_map = included_map  # type: ignore[attr-defined]  # noqa: SLF001
        config._runtime_mode = mode  # type: ignore[attr-defined]  # noqa: SLF001


# ----------------------------------------------------------------------
# Hooks
# ----------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest options based on verbosity."""
    verbose = getattr(config.option, "verbose", 0)
    if verbose <= 0:
        # In quiet mode, modify reportchars to exclude skipped tests ('s')
        # The -ra flag in pytest.ini shows all, but hide skipped in quiet mode
        reportchars = getattr(config.option, "reportchars", "")
        if reportchars == "a":
            # 'a' means "all except passed", change to exclude skipped and passed output
            # Use explicit chars: f (failed), E (error), x (xfailed), X (xpassed)
            config.option.reportchars = "fExX"
        elif "s" in reportchars or "P" in reportchars:
            # Remove 's' (skipped) and 'P' (passed with output) in quiet mode
            config.option.reportchars = reportchars.replace("s", "").replace("P", "")


def pytest_report_header(config: pytest.Config) -> str:  # noqa: ARG001 # pyright: ignore[reportUnknownParameterType]
    mode = _mode()
    return f"Runtime mode: {mode}"


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Filter and record runtime-specific tests for later reporting.

    also automatically skips debug tests unless asked for
    """
    _filter_debug_tests(config, items)
    _filter_runtime_mode_tests(config, items)


def pytest_unconfigure(config: pytest.Config) -> None:
    """Print summary of included runtime-specific tests at the end."""
    included_map: dict[str, int] = getattr(config, "_included_map", {})
    mode = getattr(config, "_runtime_mode", "installed")

    if not included_map:
        return

    # Only print if pytest is not in quiet mode (verbose > 0 means verbose mode)
    verbose = getattr(config.option, "verbose", 0)
    if verbose <= 0:
        return

    total_tests = sum(included_map.values())
    print(
        f"🧪 Included {total_tests} {mode}-specific tests"
        f" across {len(included_map)} files:",
    )
    for path, count in sorted(included_map.items()):
        print(f"   • ({count}) {path}")
