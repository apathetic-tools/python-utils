# src/apathetic_utils/testing.py
"""Test utilities mixin for reusable test helpers."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from contextlib import suppress
from types import ModuleType
from typing import Any
from unittest.mock import MagicMock

import pytest


class ApatheticUtils_Internal_Testing:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing reusable test utilities.

    Inherit from this mixin in your test classes to access shared test utilities
    that can be used across multiple projects.
    """

    @staticmethod
    def is_running_under_pytest() -> bool:
        """Detect if code is running under pytest.

        Checks multiple indicators:
        - Environment variables set by pytest
        - Command-line arguments containing 'pytest'

        Returns:
            True if running under pytest, False otherwise
        """
        return (
            "pytest" in os.environ.get("_", "")
            or "PYTEST_CURRENT_TEST" in os.environ
            or any(
                "pytest" in arg
                for arg in sys.argv
                if isinstance(arg, str)  # pyright: ignore[reportUnnecessaryIsInstance]
            )
        )

    @staticmethod
    def create_mock_superclass_test(
        mixin_class: type,
        parent_class: type,
        method_name: str,
        camel_case_method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that a mixin's snake_case method calls parent's camelCase via super().

        Creates a test class with controlled MRO:
        - TestClass inherits from mixin_class, then MockBaseClass
        - MockBaseClass provides the camelCase method that super() resolves to
        - Mocks the camelCase method and verifies it's called

        Args:
            mixin_class: The mixin class containing the snake_case method
            parent_class: The parent class with the camelCase method
                (e.g., logging.Logger)
            method_name: Name of the snake_case method to test (e.g., "add_filter")
            camel_case_method_name: Name of the camelCase method to mock
                (e.g., "addFilter")
            args: Arguments to pass to the snake_case method
            kwargs: Keyword arguments to pass to the snake_case method
            monkeypatch: pytest.MonkeyPatch fixture for patching

        Raises:
            AssertionError: If the camelCase method was not called as expected
        """
        # Get the real camelCase method from parent class to use as the base
        # implementation. Check if the method exists first.
        if not hasattr(parent_class, camel_case_method_name):
            py_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
            pytest.skip(
                f"{camel_case_method_name} does not exist on {parent_class.__name__} "
                f"(Python {py_version})"
            )
        camel_method_unbound = getattr(parent_class, camel_case_method_name)

        # Create a base class with the camelCase method (what super() resolves to)
        # We define it dynamically so we can use any method name
        # The method needs to exist on the class for patching to work
        def create_method(camel_method: Any) -> Any:
            """Create a method that wraps the parent class method."""

            def method(self: Any, *a: Any, **kw: Any) -> Any:
                return camel_method(self, *a, **kw)

            return method

        MockBaseClass = type(
            "MockBaseClass",
            (),
            {camel_case_method_name: create_method(camel_method_unbound)},
        )

        # Create test class: mixin first, then base class
        # MRO: TestLogger -> Mixin -> MockBaseClass -> object
        # When super() is called from Mixin, it resolves to MockBaseClass
        class TestClass(mixin_class, MockBaseClass):  # type: ignore[misc, valid-type]
            """Test class with controlled MRO for super() resolution."""

            def __init__(self) -> None:
                MockBaseClass.__init__(self)  # type: ignore[misc]

        # Create an instance of our test class
        test_instance = TestClass()

        # Get the snake_case method from the test instance
        snake_method = getattr(test_instance, method_name)
        if snake_method is None:
            msg = f"Method {method_name} not found on {mixin_class.__name__}"
            raise AttributeError(msg)

        # Mock the base class method (what super() resolves to)
        mock_method = MagicMock(wraps=camel_method_unbound)
        monkeypatch.setattr(MockBaseClass, camel_case_method_name, mock_method)
        # Call the snake_case method on our test instance
        # Some methods may raise (e.g., invalid arguments)
        # That's okay - we just want to verify the mock was called
        with suppress(Exception):
            snake_method(*args, **kwargs)

        # Verify the underlying method was called
        # For super() calls, this verifies the parent method was invoked
        # When called via super(), the method is bound, so self is implicit
        # The mock receives just the args (self is already bound)
        # This is a "happy path" test - we just verify the method was called
        # (exact argument matching is less important than verifying the call happened)
        if not mock_method.called:
            msg = f"{camel_case_method_name} was not called by {method_name}"
            raise AssertionError(msg)
        # If we have simple args/kwargs, try to verify them more precisely
        # But don't fail if the method has defaults that fill in extra args
        if args and not kwargs:
            # For positional-only calls, check the first few args match
            call_args = mock_method.call_args
            if call_args:
                call_args_pos, _ = call_args
                # Verify at least the first arg matches (if we have args)
                if (
                    call_args_pos
                    and len(call_args_pos) >= len(args)
                    and call_args_pos[: len(args)] != args
                ):
                    msg = (
                        f"Args don't match: expected {args}, "
                        f"got {call_args_pos[: len(args)]}"
                    )
                    raise AssertionError(msg)

    @staticmethod
    def patch_everywhere(  # noqa: C901, PLR0912
        mp: pytest.MonkeyPatch,
        mod_env: ModuleType | Any,
        func_name: str,
        replacement_func: Callable[..., object],
        package_prefix: str,
        stitch_hints: set[str] | None = None,
        create_if_missing: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Replace a function everywhere it was imported.

        Works in both package and stitched single-file runtimes.
        Walks sys.modules once and handles:
          • the defining module
          • any other module that imported the same function object
          • any freshly reloaded stitched modules (heuristic: path matches hints)

        Args:
            mp: pytest.MonkeyPatch instance to use for patching
            mod_env: Module or object containing the function to patch
            func_name: Name of the function to patch
            replacement_func: Function to replace the original with
            package_prefix: Package name prefix to filter modules
                (e.g., "apathetic_utils")
            stitch_hints: Set of path hints to identify stitched modules.
                Defaults to {"/dist/", "standalone"}.
            create_if_missing: If True, create the attribute if it doesn't exist.
                If False (default), raise TypeError if the function doesn't exist.
        """
        from apathetic_logging import safeTrace  # noqa: PLC0415

        if stitch_hints is None:
            stitch_hints = {"/dist/", "standalone"}

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
            safeTrace(f"Patched {mod_name}.{func_name}")
        else:
            safeTrace(f"Created and patched {mod_name}.{func_name}")

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
                safeTrace(f"  also patched {name} (path={path})")
                patched_ids.add(id(m))
