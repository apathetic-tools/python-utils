# src/apathetic_utils/namespace.py
"""Shared Apathetic Utils namespace implementation.

This namespace class provides a structure to minimize global namespace pollution
when the library is embedded in a stitched script.
"""

from __future__ import annotations

from .ci import (
    ApatheticUtils_Internal_CI,
)
from .constants import (
    ApatheticUtils_Internal_Constants,
)
from .files import (
    ApatheticUtils_Internal_Files,
)
from .matching import (
    ApatheticUtils_Internal_Matching,
)
from .paths import (
    ApatheticUtils_Internal_Paths,
)
from .system import (
    ApatheticUtils_Internal_System,
)
from .text import (
    ApatheticUtils_Internal_Text,
)
from .types import (
    ApatheticUtils_Internal_Types,
)


# --- Apathetic Utils Namespace -------------------------------------------


class apathetic_utils(  # noqa: N801
    ApatheticUtils_Internal_Constants,
    ApatheticUtils_Internal_CI,
    ApatheticUtils_Internal_Files,
    ApatheticUtils_Internal_Matching,
    ApatheticUtils_Internal_Paths,
    ApatheticUtils_Internal_System,
    ApatheticUtils_Internal_Text,
    ApatheticUtils_Internal_Types,
):
    """Namespace for apathetic utils functionality.

    All utility functionality is accessed via this namespace class to minimize
    global namespace pollution when the library is embedded in a stitched script.
    """


# Note: All exports are handled in __init__.py
# - For library builds (installed/singlefile): __init__.py is included, exports happen
# - For embedded builds: __init__.py is excluded, no exports (only class available)
