# tests/utils/runtime_detection.py
"""Runtime mode detection utilities for tests."""

import sys

from .constants import PROGRAM_PACKAGE


def detect_runtime_mode() -> str:
    """Detect the current runtime mode.

    Returns:
        - "frozen" if running as a frozen executable
        - "zipapp" if running as a .pyz zipapp
        - "standalone" if running as a standalone single-file script
        - "installed" if running from installed package
    """
    if getattr(sys, "frozen", False):
        return "frozen"
    if "__main__" in sys.modules and getattr(
        sys.modules["__main__"],
        "__file__",
        "",
    ).endswith(".pyz"):
        return "zipapp"
    # Check for standalone mode in multiple locations
    # 1. Check package module's globals (when loaded via importlib)
    # The standalone script is loaded as the package
    pkg_mod = sys.modules.get(PROGRAM_PACKAGE)
    if pkg_mod is not None and hasattr(pkg_mod, "__STANDALONE__"):
        return "standalone"
    # 2. Check __main__ module's globals (for script execution)
    if "__main__" in sys.modules:
        main_mod = sys.modules["__main__"]
        if hasattr(main_mod, "__STANDALONE__"):
            return "standalone"
    return "installed"
