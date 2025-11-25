# src/apathetic_utils/namespace.py
"""Shared Apathetic Utils namespace implementation.

This namespace class provides a structure to minimize global namespace pollution
when the library is embedded in a stitched script.
"""

from __future__ import annotations

from .constants import (
    ApatheticUtils_Internal_Constants,
)


# --- Apathetic Utils Namespace -------------------------------------------


class apathetic_utils(  # noqa: N801
    ApatheticUtils_Internal_Constants,
):
    """Namespace for apathetic utils functionality.

    All utility functionality is accessed via this namespace class to minimize
    global namespace pollution when the library is embedded in a stitched script.
    """


# Note: All exports are handled in __init__.py
# - For library builds (installed/singlefile): __init__.py is included, exports happen
# - For embedded builds: __init__.py is excluded, no exports (only class available)
