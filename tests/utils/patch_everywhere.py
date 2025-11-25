# tests/utils/patch_everywhere.py

import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from .constants import PROGRAM_PACKAGE, PROGRAM_SCRIPT
from .safe_trace import safe_trace
from .strip_common_prefix import strip_common_prefix


_PATCH_PATH = Path(__file__).resolve()


def _short_path(path: str | None) -> str:
    if not path:
        return "n/a"
    return strip_common_prefix(path, _PATCH_PATH)


def patch_everywhere(  # noqa: PLR0912
    mp: pytest.MonkeyPatch,
    mod_env: ModuleType | Any,
    func_name: str,
    replacement_func: Callable[..., object],
    create_if_missing: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """Replace a function everywhere it was imported.

    Works in both package and stitched single-file runtimes.
    Walks sys.modules once and handles:
      • the defining module
      • any other module that imported the same function object
      • any freshly reloaded stitched modules (heuristic: path under /bin/)

    Args:
        mp: pytest.MonkeyPatch instance to use for patching
        mod_env: Module or object containing the function to patch
        func_name: Name of the function to patch
        replacement_func: Function to replace the original with
        create_if_missing: If True, create the attribute if it doesn't exist.
            If False (default), raise TypeError if the function doesn't exist.
    """
    # --- Sanity checks ---
    func = getattr(mod_env, func_name, None)
    func_existed = func is not None
    if func is None:
        if create_if_missing:
            # Will create the function below, but don't set func to replacement_func
            # since we need to track that it didn't exist for search logic
            pass
        else:
            xmsg = f"Could not find {func_name!r} on {mod_env!r}"
            raise TypeError(xmsg)

    mod_name = getattr(mod_env, "__name__", type(mod_env).__name__)

    # Patch in the defining module
    # For modules, if the attribute doesn't exist and create_if_missing=True,
    # we need to create it manually first, then use monkeypatch to track it
    if not func_existed and isinstance(mod_env, ModuleType):
        # Manually create the attribute on the module's __dict__
        # This is necessary because monkeypatch.setattr may fail if the attribute
        # doesn't exist on a module
        mod_env.__dict__[func_name] = replacement_func
        # Now register with monkeypatch for cleanup on undo
        # Since the attribute now exists, setattr should work
        mp.setattr(mod_env, func_name, replacement_func)
    else:
        try:
            mp.setattr(mod_env, func_name, replacement_func)
        except AttributeError:
            # If setattr fails because attribute doesn't exist on a module,
            # create it manually and try again
            if isinstance(mod_env, ModuleType) and create_if_missing:
                mod_env.__dict__[func_name] = replacement_func
                mp.setattr(mod_env, func_name, replacement_func)
            else:
                raise
    if func_existed:
        safe_trace(f"Patched {mod_name}.{func_name}")
    else:
        safe_trace(f"Created and patched {mod_name}.{func_name}")

    stitch_hints = {"/dist/", "standalone", f"{PROGRAM_SCRIPT}.py"}
    package_prefix = PROGRAM_PACKAGE
    patched_ids: set[int] = set()

    for m in list(sys.modules.values()):
        if (
            m is mod_env
            or not isinstance(m, ModuleType)  # pyright: ignore[reportUnnecessaryIsInstance]
            or not hasattr(m, "__dict__")
        ):
            continue

        # skip irrelevant stdlib or third-party modules for performance
        name = getattr(m, "__name__", "")
        if not name.startswith(package_prefix):
            continue

        did_patch = False

        # 1) Normal case: module imported the same object
        # Only search if the function actually existed (not created)
        if func_existed:
            for k, v in list(m.__dict__.items()):
                if v is func:
                    mp.setattr(m, k, replacement_func)
                    did_patch = True

        # 2) Single-file case: reloaded stitched modules
        #    whose __file__ path matches heuristic
        path = getattr(m, "__file__", "") or ""
        if any(h in path for h in stitch_hints) and hasattr(m, func_name):
            mp.setattr(m, func_name, replacement_func)
            did_patch = True

        if did_patch and id(m) not in patched_ids:
            safe_trace(f"  also patched {name} (path={_short_path(path)})")
            patched_ids.add(id(m))
