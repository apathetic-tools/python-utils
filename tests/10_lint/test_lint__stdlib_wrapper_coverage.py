# tests/10_lint/test_lint__stdlib_wrapper_coverage.py
"""Custom lint rule: Check that all stdlib logging functions are wrapped.

This test acts as a "poor person's linter" to ensure we have wrapper coverage
for all standard library logging functions and Logger methods. It uses AST to:

1. Extract all module-level functions from stdlib `logging` module
2. Extract all methods from stdlib `logging.Logger` class
3. Extract all wrapped functions from our `logging_std_camel.py` (module-level wrappers)
4. Extract all wrapped methods from our `logger.py` (Logger method wrappers)
5. Compare and report any missing wrappers

This helps ensure we don't miss new stdlib functions when Python versions are
updated, and helps maintain complete wrapper coverage.
"""

import ast
import inspect
import logging
from pathlib import Path

from tests.utils.constants import PROJ_ROOT


def _is_special_method(name: str) -> bool:
    """Check if a name is a special method (starts and ends with double underscore)."""
    return name.startswith("__") and name.endswith("__")


def _should_include_function(name: str) -> bool:
    """Determine if a function should be included in coverage check.

    We exclude:
    - Special methods (starting and ending with `__`)
    - Private functions (starting with `_`)

    Args:
        name: The function or method name

    Returns:
        True if the function should be checked for coverage, False otherwise
    """
    if _is_special_method(name):
        return False
    return not name.startswith("_")


def _get_stdlib_logging_functions() -> set[str]:
    """Extract all module-level functions from stdlib logging module.

    Returns:
        Set of function names from logging module (excluding private/special)
    """
    logging_functions: set[str] = set()

    # Get all attributes from logging module
    for name in dir(logging):
        obj = getattr(logging, name)
        # Check if it's a function (not a class, constant, etc.)
        if inspect.isfunction(obj) and _should_include_function(name):
            logging_functions.add(name)

    return logging_functions


def _get_stdlib_logger_methods() -> set[str]:
    """Extract all methods from stdlib logging.Logger class.

    Returns:
        Set of method names from logging.Logger (excluding private/special)
    """
    logger_methods: set[str] = set()

    # Get all methods from logging.Logger class
    for name in dir(logging.Logger):
        obj = getattr(logging.Logger, name)
        # Check if it's a method/function
        is_method = inspect.isfunction(obj) or inspect.ismethod(obj)
        if is_method and _should_include_function(name):
            logger_methods.add(name)

    return logger_methods


def _extract_wrapped_functions_from_ast(file_path: Path) -> set[str]:
    """Extract wrapped function names from a Python file using AST.

    Looks for static methods in classes (for logging_std_camel.py).

    Args:
        file_path: Path to the Python file to parse

    Returns:
        Set of function names that are wrapped
    """
    wrapped_functions: set[str] = set()

    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return wrapped_functions

    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError:
        return wrapped_functions

    class FunctionExtractor(ast.NodeVisitor):
        """AST visitor to extract static method names."""

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            """Visit a function definition."""
            # Check if this is a static method (has @staticmethod decorator)
            is_static = any(
                isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
                for decorator in node.decorator_list
            )
            if is_static and _should_include_function(node.name):
                wrapped_functions.add(node.name)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            """Visit an async function definition."""
            # Check if this is a static method
            is_static = any(
                isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
                for decorator in node.decorator_list
            )
            if is_static and _should_include_function(node.name):
                wrapped_functions.add(node.name)
            self.generic_visit(node)

    extractor = FunctionExtractor()
    extractor.visit(tree)
    return wrapped_functions


def _extract_wrapped_logger_methods_from_ast(file_path: Path) -> set[str]:
    """Extract wrapped Logger method names from a Python file using AST.

    Looks for instance methods in classes that inherit from logging.Logger.

    Args:
        file_path: Path to the Python file to parse

    Returns:
        Set of method names that are wrapped/overridden
    """
    wrapped_methods: set[str] = set()

    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return wrapped_methods

    try:
        tree = ast.parse(content, filename=str(file_path))
    except SyntaxError:
        return wrapped_methods

    class LoggerMethodExtractor(ast.NodeVisitor):
        """AST visitor to extract methods from Logger subclasses."""

        def __init__(self, methods_set: set[str]) -> None:
            """Initialize the extractor.

            Args:
                methods_set: Set to collect method names into
            """
            self.in_logger_subclass = False
            self.methods_set = methods_set

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            """Visit a class definition."""
            # Check if this class inherits from logging.Logger
            old_state = self.in_logger_subclass
            for base in node.bases:
                if isinstance(base, ast.Attribute):
                    if (
                        isinstance(base.value, ast.Name)
                        and base.value.id == "logging"
                        and base.attr == "Logger"
                    ):
                        self.in_logger_subclass = True
                        break
                elif isinstance(base, ast.Name):
                    # Could be an alias, but we'll check if it's Logger
                    # For now, we'll be conservative and check all methods
                    # in classes that might be Logger subclasses
                    pass

            self.generic_visit(node)
            self.in_logger_subclass = old_state

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            """Visit a function definition."""
            # If we're in a Logger subclass, collect instance methods
            # (not static methods or class methods)
            if self.in_logger_subclass:
                is_static = any(
                    isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
                    for decorator in node.decorator_list
                )
                is_classmethod = any(
                    isinstance(decorator, ast.Name) and decorator.id == "classmethod"
                    for decorator in node.decorator_list
                )
                # Include instance methods (not static/class methods)
                # and exclude __init__ (we override it but it's special)
                if (
                    not is_static
                    and not is_classmethod
                    and _should_include_function(node.name)
                    and node.name != "__init__"
                ):
                    self.methods_set.add(node.name)
            self.generic_visit(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            """Visit an async function definition."""
            if self.in_logger_subclass:
                is_static = any(
                    isinstance(decorator, ast.Name) and decorator.id == "staticmethod"
                    for decorator in node.decorator_list
                )
                is_classmethod = any(
                    isinstance(decorator, ast.Name) and decorator.id == "classmethod"
                    for decorator in node.decorator_list
                )
                if (
                    not is_static
                    and not is_classmethod
                    and _should_include_function(node.name)
                ):
                    self.methods_set.add(node.name)
            self.generic_visit(node)

    extractor = LoggerMethodExtractor(wrapped_methods)
    extractor.visit(tree)
    return wrapped_methods


def test_stdlib_logging_module_coverage() -> None:
    """Check that all stdlib logging.* functions have wrappers.

    This test ensures we have wrapper coverage for all standard library
    logging module-level functions. It compares the functions available in
    the stdlib `logging` module against the functions we've wrapped in
    `logging_std_camel.py`.

    Note: This test may report false positives for:
    - Functions that are not meant to be wrapped (internal/private stdlib functions)
    - Functions that are deprecated or removed in newer Python versions
    - Functions that are version-specific (Python 3.11+, 3.12+, etc.)

    These should be documented with explicit exclusions if they're intentional.
    """
    # Get stdlib functions
    stdlib_functions = _get_stdlib_logging_functions()

    # Get our wrapped functions from logging_std_camel.py
    logging_std_camel_path = (
        PROJ_ROOT / "src" / "apathetic_utils" / "logging_std_camel.py"
    )
    wrapped_functions = _extract_wrapped_functions_from_ast(logging_std_camel_path)

    # Functions we intentionally don't wrap (document exceptions)
    # Add to this set if there are stdlib functions we intentionally skip
    intentional_exclusions: set[str] = set()
    # Add function names here if they should not be wrapped

    # Find missing wrappers
    missing = stdlib_functions - wrapped_functions - intentional_exclusions

    if missing:
        print("\n❌ Missing wrappers for stdlib logging.* functions:")
        print(
            "\nThe following stdlib logging module functions are not wrapped"
            " in logging_std_camel.py:"
        )
        for func_name in sorted(missing):
            print(f"  - logging.{func_name}")
        print(
            "\nTo fix:"
            "\n  1. Add a wrapper function in"
            " src/apathetic_utils/logging_std_camel.py"
            "\n  2. Or add to intentional_exclusions if the function"
            " should not be wrapped"
        )
        xmsg = (
            f"{len(missing)} stdlib logging.* function(s) are not wrapped."
            " All standard library logging functions should have wrappers"
            " in logging_std_camel.py (unless explicitly excluded)."
        )
        raise AssertionError(xmsg)


def test_stdlib_logger_method_coverage() -> None:
    """Check that all stdlib logging.Logger.* methods have wrappers.

    This test ensures we have wrapper/override coverage for all standard library
    logging.Logger methods. It compares the methods available in the stdlib
    `logging.Logger` class against the methods we've overridden/extended in
    `logger.py`.

    Note: This test may report false positives for:
    - Methods that are not meant to be wrapped (internal/private stdlib methods)
    - Methods that are deprecated or removed in newer Python versions
    - Methods that are version-specific (Python 3.11+, 3.12+, etc.)
    - Methods that we intentionally don't override (inherit as-is)

    These should be documented with explicit exclusions if they're intentional.
    """
    # Get stdlib Logger methods
    stdlib_methods = _get_stdlib_logger_methods()

    # Get our wrapped methods from logger.py
    logger_path = PROJ_ROOT / "src" / "apathetic_utils" / "logger.py"
    wrapped_methods = _extract_wrapped_logger_methods_from_ast(logger_path)

    # Methods we intentionally don't wrap (document exceptions)
    # Add to this set if there are stdlib Logger methods we intentionally skip
    # Common ones we might not override:
    # - Methods that work fine as-is from the base class
    # - Internal methods that shouldn't be overridden
    intentional_exclusions: set[str] = {
        # Logging methods that work fine as-is because we override _log():
        "critical",
        "debug",
        "error",
        "exception",
        "fatal",
        "info",
        "log",
        "warn",
        "warning",
        # Handler/filter methods that work fine as-is:
        "addFilter",
        "addHandler",
        "callHandlers",
        "filter",
        "handle",
        "removeFilter",
        "removeHandler",
        # Utility methods that work fine as-is:
        "findCaller",
        "getChild",
        "getChildren",
        "getEffectiveLevel",
        "hasHandlers",
        "isEnabledFor",
        "makeRecord",
    }

    # Find missing wrappers
    missing = stdlib_methods - wrapped_methods - intentional_exclusions

    if missing:
        print("\n❌ Missing wrappers for stdlib logging.Logger.* methods:")
        print(
            "\nThe following stdlib logging.Logger methods are not wrapped"
            " in logger.py:"
        )
        for method_name in sorted(missing):
            print(f"  - logging.Logger.{method_name}")
        print(
            "\nTo fix:"
            "\n  1. Add a method override in src/apathetic_utils/logger.py"
            "\n  2. Or add to intentional_exclusions if the method"
            " should not be wrapped"
        )
        print(
            "\nNote: Some methods may work fine as-is from the base class."
            " Only add wrappers if you need to extend or modify behavior."
        )
        xmsg = (
            f"{len(missing)} stdlib logging.Logger.* method(s) are not wrapped."
            " All standard library Logger methods should be reviewed and either"
            " wrapped in logger.py or explicitly excluded."
        )
        raise AssertionError(xmsg)
