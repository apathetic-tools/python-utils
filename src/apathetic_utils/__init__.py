# src/apathetic_utils/__init__.py
"""Apathetic Utils implementation."""

from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:
    from .namespace import apathetic_utils as _apathetic_utils_class

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
#
# Note: In embedded builds, __init__.py is excluded from the stitch,
# so this code never runs and no exports happen (only the class is available).
# In singlefile/installed builds, __init__.py is included, so exports happen.

# Exports will be added here as utilities are implemented

__all__ = [
    "apathetic_utils",
]
