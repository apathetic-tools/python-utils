---
layout: base
title: API Reference
permalink: /api/
---

# API Reference

Complete API documentation for Apathetic Python Utils.

## Quick Reference

| Category | Functions |
|----------|-----------|
| **File Loading** | [`load_jsonc()`](#load_jsonc), [`load_toml()`](#load_toml) |
| **Path Utilities** | [`normalize_path_string()`](#normalize_path_string), [`has_glob_chars()`](#has_glob_chars), [`get_glob_root()`](#get_glob_root) |
| **Pattern Matching** | [`fnmatchcase_portable()`](#fnmatchcase_portable), [`is_excluded_raw()`](#is_excluded_raw) |
| **System Detection** | [`is_ci()`](#is_ci), [`is_running_under_pytest()`](#is_running_under_pytest), [`detect_runtime_mode()`](#detect_runtime_mode), [`capture_output()`](#capture_output), [`get_sys_version_info()`](#get_sys_version_info) |
| **Text Processing** | [`plural()`](#plural), [`remove_path_in_error_message()`](#remove_path_in_error_message) |
| **Type Utilities** | [`safe_isinstance()`](#safe_isinstance), [`literal_to_set()`](#literal_to_set), [`cast_hint()`](#cast_hint), [`schema_from_typeddict()`](#schema_from_typeddict) |
| **Constants** | [`CI_ENV_VARS`](#ci_env_vars) |

## File Loading

### load_jsonc

```python
load_jsonc(path: Path) -> dict[str, Any] | list[Any] | None
```

Load and parse a JSONC (JSON with Comments) file.

Supports:
- Single-line comments (`//` and `#`)
- Block comments (`/* */`)
- Trailing commas
- Empty files or files with only comments (returns `None`)

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Path to the JSONC file |

**Returns:**
- `dict[str, Any] | list[Any]`: Parsed JSON data (dict or list)
- `None`: If the file is empty or contains only comments

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `ValueError`: If the file is not a file, has invalid JSONC syntax, or has a scalar root

**Example:**
```python
from apathetic_utils import load_jsonc
from pathlib import Path

config = load_jsonc(Path("config.jsonc"))
# {
#   "name": "my_app",
#   "version": "1.0.0"
# }
```

### load_toml

```python
load_toml(path: Path, *, required: bool = False) -> dict[str, Any] | None
```

Load and parse a TOML file, supporting Python 3.10 and 3.11+.

Uses:
- `tomllib` (Python 3.11+ standard library)
- `tomli` (required for Python 3.10 - must be installed separately)

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Path to the TOML file |
| `required` | `bool` | If `True`, raise `RuntimeError` when `tomli` is missing on Python 3.10. If `False`, return `None` when unavailable. Defaults to `False`. |

**Returns:**
- `dict[str, Any]`: Parsed TOML data as a dictionary
- `None`: If unavailable and `required=False`

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `RuntimeError`: If `required=True` and neither `tomllib` nor `tomli` is available
- `ValueError`: If the file cannot be parsed

**Example:**
```python
from apathetic_utils import load_toml
from pathlib import Path

pyproject = load_toml(Path("pyproject.toml"), required=True)
```

## Path Utilities

### normalize_path_string

```python
normalize_path_string(raw: str) -> str
```

Normalize a user-supplied path string for cross-platform use.

Industry-standard (Git/Node/Python) rules:
- Treat both `/` and `\` as valid separators and normalize all to `/`
- Replace escaped spaces (`\ `) with real spaces
- Collapse redundant slashes (preserve protocol prefixes like `file://`)
- Never resolve `.` or `..` or touch the filesystem
- Never raise for syntax; normalization is always possible

This is purely lexical — it normalizes syntax, not filesystem state.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `raw` | `str` | Raw path string to normalize |

**Returns:**
- `str`: Normalized path string

**Example:**
```python
from apathetic_utils import normalize_path_string

path = normalize_path_string("src\\utils\\file.py")
# Returns: "src/utils/file.py"

path = normalize_path_string("src//utils///file.py")
# Returns: "src/utils/file.py"
```

### has_glob_chars

```python
has_glob_chars(s: str) -> bool
```

Check if a string contains glob pattern characters (`*`, `?`, `[`).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `s` | `str` | String to check |

**Returns:**
- `bool`: `True` if the string contains glob characters, `False` otherwise

**Example:**
```python
from apathetic_utils import has_glob_chars

has_glob_chars("src/**/*.py")  # True
has_glob_chars("src/file.py")  # False
```

### get_glob_root

```python
get_glob_root(pattern: str) -> Path
```

Return the non-glob portion of a path pattern like `src/**/*.txt`.

Normalizes paths to cross-platform format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `pattern` | `str` | Glob pattern string |

**Returns:**
- `Path`: The non-glob portion of the path

**Example:**
```python
from apathetic_utils import get_glob_root

root = get_glob_root("src/**/*.txt")
# Returns: Path("src")

root = get_glob_root("tests/unit/**/*.py")
# Returns: Path("tests/unit")
```

## Pattern Matching

### fnmatchcase_portable

```python
fnmatchcase_portable(path: str, pattern: str) -> bool
```

Case-sensitive glob pattern matching with Python 3.10 `**` backport.

Uses `fnmatchcase` (case-sensitive) as the base, with backported support for recursive `**` patterns on Python 3.10.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `str` | The path to match against the pattern |
| `pattern` | `str` | The glob pattern to match |

**Returns:**
- `bool`: `True` if the path matches the pattern, `False` otherwise

**Example:**
```python
from apathetic_utils import fnmatchcase_portable

fnmatchcase_portable("src/utils/file.py", "src/**/*.py")  # True
fnmatchcase_portable("deep/nested/file.py", "**/*.py")    # True
fnmatchcase_portable("src/file.py", "src/*.py")            # True
```

### is_excluded_raw

```python
is_excluded_raw(
    path: Path | str,
    exclude_patterns: list[str],
    root: Path | str
) -> bool
```

Smart matcher for normalized inputs to check if a path matches exclusion patterns.

- Treats `path` as relative to `root` unless already absolute
- If `root` is a file, match directly
- Handles absolute or relative glob patterns
- Supports patterns with `../` to match files outside the exclude root
- Supports `**/` patterns for recursive matching

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Path \| str` | Path to check against exclusion patterns |
| `exclude_patterns` | `list[str]` | List of glob patterns to exclude |
| `root` | `Path \| str` | Root directory for relative path resolution |

**Returns:**
- `bool`: `True` if the path matches any exclusion pattern, `False` otherwise

**Example:**
```python
from apathetic_utils import is_excluded_raw
from pathlib import Path

patterns = ["**/__pycache__/**", "*.pyc", "tests/**"]
root = Path(".")

is_excluded_raw("src/__pycache__/file.pyc", patterns, root)  # True
is_excluded_raw("src/utils/file.py", patterns, root)         # False
```

## System Detection

### is_ci

```python
is_ci() -> bool
```

Check if running in a CI environment.

Returns `True` if any of the following environment variables are set:
- `CI`: Generic CI indicator (set by most CI systems)
- `GITHUB_ACTIONS`: GitHub Actions specific
- `GIT_TAG`: Indicates a tagged build
- `GITHUB_REF`: GitHub Actions ref (branch/tag)

**Returns:**
- `bool`: `True` if running in CI, `False` otherwise

**Example:**
```python
from apathetic_utils import is_ci

if is_ci():
    print("Running in CI environment")
    # Adjust behavior for CI
```

### is_running_under_pytest

```python
is_running_under_pytest() -> bool
```

Detect if code is running under pytest.

Checks multiple indicators:
- Environment variables set by pytest
- Command-line arguments containing 'pytest'

**Returns:**
- `bool`: `True` if running under pytest, `False` otherwise

**Example:**
```python
from apathetic_utils import is_running_under_pytest

if is_running_under_pytest():
    # Use test-specific configuration
    pass
```

### detect_runtime_mode

```python
detect_runtime_mode(package_name: str) -> str
```

Detect how the package is being executed.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `package_name` | `str` | Name of the package to check |

**Returns:**
- `str`: Runtime mode, one of:
  - `"installed"`: Package installed via pip/poetry
  - `"standalone"`: Single-file standalone script
  - `"zipapp"`: Python zipapp (`.pyz` file)
  - `"frozen"`: Frozen executable (PyInstaller, etc.)

**Example:**
```python
from apathetic_utils import detect_runtime_mode

mode = detect_runtime_mode("my_package")
print(f"Running in {mode} mode")
```

### capture_output

```python
capture_output() -> ContextManager[CapturedOutput]
```

Temporarily capture stdout and stderr.

Any exception raised inside the block is re-raised with the captured output attached as `exc.captured_output`.

**Returns:**
- `ContextManager[CapturedOutput]`: Context manager that yields a `CapturedOutput` object

**CapturedOutput Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `stdout` | `StringIO` | Captured stdout |
| `stderr` | `StringIO` | Captured stderr |
| `merged` | `StringIO` | Merged stdout and stderr |

**CapturedOutput Methods:**

| Method | Description |
|--------|-------------|
| `as_dict() -> dict[str, str]` | Return contents as plain strings for serialization |

**Example:**
```python
from apathetic_utils import capture_output
import sys

with capture_output() as cap:
    print("Hello, world!")
    print("Error message", file=sys.stderr)

print(f"stdout: {cap.stdout.getvalue()}")
print(f"stderr: {cap.stderr.getvalue()}")
print(f"merged: {cap.merged.getvalue()}")

# Or convert to dict
output = cap.as_dict()
```

### get_sys_version_info

```python
get_sys_version_info() -> tuple[int, int, int] | tuple[int, int, int, str, int]
```

Get Python version information.

Wrapper for `sys.version_info`.

**Returns:**
- `tuple[int, int, int]`: Version tuple `(major, minor, micro)`
- `tuple[int, int, int, str, int]`: Version tuple with releaselevel and serial (for release candidates)

**Example:**
```python
from apathetic_utils import get_sys_version_info

version = get_sys_version_info()
print(f"Python {version[0]}.{version[1]}.{version[2]}")
```

## Text Processing

### plural

```python
plural(obj: Any) -> str
```

Return `'s'` if `obj` represents a plural count.

Accepts ints, floats, and any object implementing `__len__()`. Returns `''` for singular or zero.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `obj` | `Any` | Object to check (int, float, or object with `__len__()`) |

**Returns:**
- `str`: `'s'` for plural, `''` for singular or zero

**Example:**
```python
from apathetic_utils import plural

count = 5
print(f"{count} file{plural(count)}")  # "5 files"

count = 1
print(f"{count} file{plural(count)}")  # "1 file"

items = [1, 2, 3]
print(f"{len(items)} item{plural(items)}")  # "3 items"
```

### remove_path_in_error_message

```python
remove_path_in_error_message(inner_msg: str, path: Path) -> str
```

Remove redundant file path mentions (and nearby filler) from error messages.

Useful when wrapping a lower-level exception that already embeds its own file reference, so the higher-level message can use its own path without duplication.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `inner_msg` | `str` | Error message that may contain path references |
| `path` | `Path` | Path to remove from the message |

**Returns:**
- `str`: Error message with path references removed

**Example:**
```python
from apathetic_utils import remove_path_in_error_message
from pathlib import Path

error_msg = "Invalid JSONC syntax in /path/to/config.jsonc: Expecting value"
path = Path("/path/to/config.jsonc")

clean_msg = remove_path_in_error_message(error_msg, path)
# Returns: "Invalid JSONC syntax: Expecting value"
```

## Type Utilities

### safe_isinstance

```python
safe_isinstance(value: Any, expected_type: Any) -> bool
```

Like `isinstance()`, but safe for TypedDicts and typing generics.

Handles:
- `typing.Union`, `Optional`, `Any`
- `typing.NotRequired`
- TypedDict subclasses
- `list[...]` with inner types
- `dict[...]` with key/value types
- `tuple[...]` with element types
- Defensive fallback for exotic typing constructs

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `Any` | Value to check |
| `expected_type` | `Any` | Type to check against |

**Returns:**
- `bool`: `True` if value matches the expected type, `False` otherwise

**Example:**
```python
from apathetic_utils import safe_isinstance
from typing import TypedDict, Optional

class Config(TypedDict):
    name: str
    value: int

data = {"name": "test", "value": 42}

# Works with TypedDict
safe_isinstance(data, Config)  # True

# Works with generics
safe_isinstance([1, 2, 3], list[int])  # True
safe_isinstance({"a": 1, "b": 2}, dict[str, int])  # True

# Works with Optional
safe_isinstance(None, Optional[str])  # True
safe_isinstance("test", Optional[str])  # True
```

### literal_to_set

```python
literal_to_set(literal_type: Any) -> set[Any]
```

Extract values from a `Literal` type as a set.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `literal_type` | `Any` | A `Literal` type (e.g., `Literal["a", "b"]`) |

**Returns:**
- `set[Any]`: A set containing all values from the `Literal` type

**Raises:**
- `TypeError`: If the input is not a `Literal` type

**Example:**
```python
from apathetic_utils import literal_to_set
from typing import Literal

Mode = Literal["dev", "prod", "test"]
valid_modes = literal_to_set(Mode)
# Returns: {"dev", "prod", "test"}

if "dev" in valid_modes:
    print("Valid mode")
```

### cast_hint

```python
cast_hint(typ: type[T], value: Any) -> T
```

Explicit cast that documents intent but is purely for type hinting.

A drop-in replacement for `typing.cast`, meant for places where:
- You want to silence mypy's redundant-cast warnings
- You want to signal "this narrowing is intentional"
- You need IDEs (like Pylance) to retain strong inference on a value

Does not handle `Union`, `Optional`, or nested generics: stick to `cast()` for those, because unions almost always represent a meaningful type narrowing.

This function performs **no runtime checks**.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `typ` | `type[T]` | Target type |
| `value` | `Any` | Value to cast |

**Returns:**
- `T`: The value (unchanged at runtime)

**Example:**
```python
from apathetic_utils import cast_hint

# Type narrowing for type checkers
value: Any = get_data()
typed_value = cast_hint(dict[str, int], value)
# typed_value is now inferred as dict[str, int]
```

### schema_from_typeddict

```python
schema_from_typeddict(td: type[Any]) -> dict[str, Any]
```

Extract field names and their annotated types from a TypedDict.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `td` | `type[Any]` | TypedDict class |

**Returns:**
- `dict[str, Any]`: Dictionary mapping field names to their types

**Example:**
```python
from apathetic_utils import schema_from_typeddict
from typing import TypedDict

class Config(TypedDict):
    name: str
    value: int

schema = schema_from_typeddict(Config)
# Returns: {"name": str, "value": int}
```

## Constants

### CI_ENV_VARS

```python
CI_ENV_VARS: tuple[str, ...]
```

Tuple of CI environment variable names that indicate a CI environment.

Default values:
- `"CI"`
- `"GITHUB_ACTIONS"`
- `"GIT_TAG"`
- `"GITHUB_REF"`

**Example:**
```python
from apathetic_utils import CI_ENV_VARS

print(CI_ENV_VARS)  # ("CI", "GITHUB_ACTIONS", "GIT_TAG", "GITHUB_REF")
```

## Namespace Class

All utilities are also available through the `apathetic_utils` namespace class:

```python
from apathetic_utils import apathetic_utils

# Use via namespace
config = apathetic_utils.load_jsonc(Path("config.jsonc"))
is_ci = apathetic_utils.is_ci()
mode = apathetic_utils.detect_runtime_mode("my_package")
```

This is useful when embedding the library as a single-file script to minimize global namespace pollution.
