# src/apathetic_utils/__init__.py
"""Apathetic utilities package."""

from typing import TYPE_CHECKING, TypeAlias, cast


if TYPE_CHECKING:
    from .namespace import apathetic_utils as _apathetic_utils_class
    from .system import ApatheticUtils_Internal_System

# Get reference to the namespace class
# In stitched mode: class is already defined in namespace.py (executed before this)
# In installed mode: import from namespace module
_is_standalone = globals().get("__STANDALONE__", False)

if _is_standalone:
    # Stitched mode: class already defined in namespace.py
    # Get reference to the class (it's already in globals from namespace.py)
    _apathetic_utils_raw = globals().get("apathetic_utils")
    if _apathetic_utils_raw is None:
        # Fallback: should not happen, but handle gracefully
        msg = "apathetic_utils class not found in standalone mode"
        raise RuntimeError(msg)
    # Type cast to help mypy understand this is the apathetic_utils class
    # The import gives us type[apathetic_utils], so cast to
    # type[_apathetic_utils_class]
    apathetic_utils = cast("type[_apathetic_utils_class]", _apathetic_utils_raw)
else:
    # Installed mode: import from namespace module
    # This block is only executed in installed mode, not in standalone builds
    from .namespace import apathetic_utils

    # Ensure the else block is not empty (build script may remove import)
    _ = apathetic_utils

# Export all namespace items for convenience
# These are aliases to apathetic_utils.*

# Note: In embedded builds, __init__.py is excluded from the stitch,
# so this code never runs and no exports happen (only the class is available).
# In singlefile/installed builds, __init__.py is included, so exports happen.

# CI
CI_ENV_VARS = apathetic_utils.CI_ENV_VARS
is_ci = apathetic_utils.is_ci

# Files
load_jsonc = apathetic_utils.load_jsonc
load_toml = apathetic_utils.load_toml

# Matching
fnmatchcase_portable = apathetic_utils.fnmatchcase_portable
is_excluded_raw = apathetic_utils.is_excluded_raw

# Paths
get_glob_root = apathetic_utils.get_glob_root
has_glob_chars = apathetic_utils.has_glob_chars
normalize_path_string = apathetic_utils.normalize_path_string

# System
# CapturedOutput is a nested class in ApatheticUtils_Internal_System that
# is accessed via the namespace class.
# Use TypeAlias to help mypy understand this is a class type.
if TYPE_CHECKING:
    CapturedOutput: TypeAlias = ApatheticUtils_Internal_System.CapturedOutput
else:
    CapturedOutput = apathetic_utils.CapturedOutput

capture_output = apathetic_utils.capture_output
detect_runtime_mode = apathetic_utils.detect_runtime_mode
get_sys_version_info = apathetic_utils.get_sys_version_info
is_running_under_pytest = apathetic_utils.is_running_under_pytest

# Text
plural = apathetic_utils.plural
remove_path_in_error_message = apathetic_utils.remove_path_in_error_message

# Types
cast_hint = apathetic_utils.cast_hint
literal_to_set = apathetic_utils.literal_to_set
safe_isinstance = apathetic_utils.safe_isinstance
schema_from_typeddict = apathetic_utils.schema_from_typeddict


__all__ = [  # noqa: RUF022
    "apathetic_utils",
    # ci
    "CI_ENV_VARS",
    "is_ci",
    # files
    "load_jsonc",
    "load_toml",
    # matching
    "fnmatchcase_portable",
    "is_excluded_raw",
    # paths
    "get_glob_root",
    "has_glob_chars",
    "normalize_path_string",
    # system
    "CapturedOutput",
    "capture_output",
    "detect_runtime_mode",
    "get_sys_version_info",
    "is_running_under_pytest",
    # text
    "plural",
    "remove_path_in_error_message",
    # types
    "cast_hint",
    "literal_to_set",
    "safe_isinstance",
    "schema_from_typeddict",
]
