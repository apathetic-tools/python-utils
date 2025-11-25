---
layout: base
title: API Reference
permalink: /api/
---

# API Reference

Complete API documentation for Apathetic Python Utils.

> **Note:** This library uses **camelCase** naming to match Python's standard library `logging` module conventions.
>
> By default, this library provides improved behavior with enhancements over the standard library. For stdlib-compatible behavior with no breaking changes, enable [Compatibility Mode](#compatibility-mode).

## Quick Reference: `apathetic_utils` Module Functions

### New Functions

| Function | Summary |
|-----------|---------|
| [`getLoggerOfType()`](#getloggeroftype) | Get a logger of the specified type, creating it if necessary |
| [`registerLogger()`](#registerlogger) | Register a logger for use by `getLogger()` |
| [`registerCompatibilityMode()`](#registercompatibilitymode) | Register the compatibility mode setting for stdlib drop-in replacement |
| [`getCompatibilityMode()`](#getcompatibilitymode) | Get the compatibility mode setting |
| [`registerLogLevelEnvVars()`](#registerloglevelenvvars) | Register environment variable names to check for log level |
| [`registerDefaultLogLevel()`](#registerdefaultloglevel) | Register the default log level to use when no other source is found |
| [`registerTargetPythonVersion()`](#registertargetpythonversion) | Register the target Python version for compatibility checking |
| [`registerPropagate()`](#registerpropagate) | Register the propagate setting for loggers |
| [`safeLog()`](#safelog) | Emergency logger that never fails |
| [`safeTrace()`](#safetrace) | Debug tracing function for test development |
| [`makeSafeTrace()`](#makesafetrace) | Create a test trace function with a custom icon |
| [`hasLogger()`](#haslogger) | Check if a logger exists in the logging manager's registry |
| [`removeLogger()`](#removelogger) | Remove a logger from the logging manager's registry |
| [`getDefaultLoggerName()`](#getdefaultloggername) | Get default logger name with optional inference from caller's frame |
| [`getLogLevelEnvVars()`](#getloglevelenvvars) | Get the environment variable names to check for log level |
| [`getDefaultLogLevel()`](#getdefaultloglevel) | Get the default log level |
| [`getRegisteredLoggerName()`](#getregisteredloggername) | Get the registered logger name |
| [`getTargetPythonVersion()`](#gettargetpythonversion) | Get the target Python version |
| [`getDefaultPropagate()`](#getdefaultpropagate) | Get the default propagate setting |
| [`getLevelNumber()`](#getlevelnumber) | Convert a log level name to its numeric value |
| [`getLevelNameStr()`](#getlevelnamestr) | Convert a log level to its string name (always returns string) |

### Changed Functions

| Function | Summary |
|-----------|---------|
| [`getLogger()`](#getlogger) | Return the registered logger instance (auto-infers name when None) |
| [`getLevelName()`](#getlevelname) | Get the level name for a numeric level (extended version that always returns string) |

### Unchanged Functions

| Function | Summary |
|-----------|---------|
| [`basicConfig()`](#basicconfig) | Configure logging system |
| [`addLevelName()`](#addlevelname) | Associate a level name with a numeric level |
| [`getLevelNamesMapping()`](#getlevelnamesmapping) | 3.11+: Get mapping of level names to numeric values |
| [`getLoggerClass()`](#getloggerclass) | Return the class to be used when instantiating a logger |
| [`setLoggerClass()`](#setloggerclass) | Set the class to be used when instantiating a logger |
| [`getLogRecordFactory()`](#getlogrecordfactory) | Return the factory function used to create LogRecords |
| [`setLogRecordFactory()`](#setlogrecordfactory) | Set the factory function used to create LogRecords |
| [`shutdown()`](#shutdown) | Perform an orderly shutdown of the logging system |
| [`disable()`](#disable) | Disable all logging calls of severity 'level' and below |
| [`captureWarnings()`](#capturewarnings) | Capture warnings issued by the warnings module |
| [`critical()`](#critical) | Log a message with severity CRITICAL |
| [`debug()`](#debug) | Log a message with severity DEBUG |
| [`detail()`](#detail) | Log a message with severity DETAIL |
| [`error()`](#error) | Log a message with severity ERROR |
| [`exception()`](#exception) | Log a message with severity ERROR with exception info |
| [`fatal()`](#fatal) | Log a message with severity CRITICAL |
| [`info()`](#info) | Log a message with severity INFO |
| [`log()`](#log) | Log a message with an explicit level |
| [`minimal()`](#minimal) | Log a message with severity MINIMAL |
| [`trace()`](#trace) | Log a message with severity TRACE |
| [`warn()`](#warn) | Log a message with severity WARNING |
| [`warning()`](#warning) | Log a message with severity WARNING |
| [`getHandlerByName()`](#gethandlerbyname) | 3.12+: Get a handler with the specified name |
| [`getHandlerNames()`](#gethandlernames) | 3.12+: Return all known handler names |
| [`makeLogRecord()`](#makelogrecord) | Create a LogRecord from the given parameters |
| [`currentframe()`](#currentframe) | Return the frame object for the caller's stack frame |

## Quick Reference: `apathetic_utils.Logger` Class Methods

### New Methods

| Method | Summary |
|--------|---------|
| [`determineLogLevel()`](#determineloglevel) | Resolve log level from CLI → env → root config → default |
| [`determineColorEnabled()`](#determinecolorenabled) | Return True if colored output should be enabled (classmethod) |
| [`extendLoggingModule()`](#extendloggingmodule) | Extend Python's logging module with TRACE and SILENT levels (classmethod) |
| [`trace()`](#trace) | Log a message at TRACE level |
| [`detail()`](#detail) | Log a message at DETAIL level |
| [`minimal()`](#minimal) | Log a message at MINIMAL level |
| [`test()`](#test) | Log a message at TEST level |
| [`errorIfNotDebug()`](#errorifnotdebug) | Log an error with full traceback only if debug/trace is enabled |
| [`criticalIfNotDebug()`](#criticalifnotdebug) | Log a critical error with full traceback only if debug/trace is enabled |
| [`colorize()`](#colorize) | Apply ANSI color codes to text |
| [`logDynamic()`](#logdynamic) | Log a message at a dynamically specified level |
| [`useLevel()`](#uselevel) | Context manager to temporarily change log level |
| [`levelName`](#levelname) | Return the explicit level name set on this logger (property) |
| [`effectiveLevel`](#effectivelevel) | Return the effective level (what's actually used) (property) |
| [`effectiveLevelName`](#effectivelevelname) | Return the effective level name (what's actually used) (property) |
| [`getLevel()`](#getlevel) | Return the explicit level set on this logger |
| [`getLevelName()`](#getlevelname) | Return the explicit level name set on this logger |
| [`getEffectiveLevelName()`](#geteffectivelevelname) | Return the effective level name (what's actually used) |
| [`ensureHandlers()`](#ensurehandlers) | Ensure handlers are attached to this logger |
| [`validateLevelPositive()`](#validatelevelpositive) | Validate that a level value is positive (> 0) (staticmethod) |

### Changed Methods

| Method | Summary |
|--------|---------|
| [`setLevel()`](#setlevel) | Set the logging level (accepts string names and has minimum parameter) |
| [`_log()`](#_log) | Log a message with the specified level (automatically ensures handlers) |
| [`addLevelName()`](#addlevelname) | Associate a level name with a numeric level (validates level > 0) (staticmethod) |

### Unchanged Methods

All other methods from `logging.Logger` are inherited unchanged. See the [Python logging.Logger documentation](https://docs.python.org/3/library/logging.html#logging.Logger) for the complete list.

**Version-specific methods:**
- [`getChildren()`](#getchildren) - 3.12+: Return a set of loggers that are immediate children of this logger

## `apathetic_utils` Function Reference

### getLogger

```python
getLogger(
    logger_name: str | None = None,
    *,
    level: str | int | None = None,
    minimum: bool | None = None
) -> Logger
```

Return the registered logger instance.

Uses Python's built-in logging registry (`logging.getLogger()`) to retrieve the logger. If no logger name is provided, uses the registered logger name or attempts to auto-infer the logger name from the calling module's top-level package.

> **Behavior:** When `logger_name` is `None`, the logger name is **auto-inferred** from the calling module (improved behavior). To get the root logger, use `getLogger("")` instead. In [Compatibility Mode](#compatibility-mode), `getLogger(None)` returns the root logger (stdlib behavior).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger_name` | str \| None | Optional logger name. If not provided, uses the registered logger name or auto-infers from the calling module. Use `""` to get the root logger. |
| `level` | str \| int \| None | Exact log level to set on the logger. Accepts both string names (case-insensitive) and numeric values. If provided, sets the logger's level to this value. Defaults to None (no change). |
| `minimum` | bool \| None | If True, only set the level if it's more verbose (lower numeric value) than the current level. This prevents downgrading from a more verbose level (e.g., TRACE) to a less verbose one (e.g., DEBUG). If None, defaults to False. Only used when `level` is provided. |

**Returns:**
- The logger instance from `logging.getLogger()` (as `apathetic_utils.Logger` type)

**Raises:**
- `RuntimeError`: If no logger name is provided and no logger name has been registered and auto-inference fails.
- `ValueError`: If an invalid log level is provided.

**Example:**
```python
from apathetic_utils import getLogger, registerLogger

# Using registered logger name
registerLogger("my_app")
logger = getLogger()  # Gets "my_app" logger

# Or specify logger name directly
logger = getLogger("my_app")  # Gets "my_app" logger

# Set exact log level
logger = getLogger("my_app", level="debug")  # Sets level to DEBUG

# Set minimum log level (only if current is less verbose)
logger = getLogger("my_app", level="info", minimum=True)  # At least INFO

# To get root logger (use "" instead of None)
logger = getLogger("")  # Returns root logger
```

### getLoggerOfType

```python
getLoggerOfType(
    name: str | None,
    class_type: type[Logger],
    skip_frames: int = 1,
    *args: Any,
    level: str | int | None = None,
    minimum: bool | None = None,
    **kwargs: Any
) -> Logger
```

Get a logger of the specified type, creating it if necessary.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str \| None | The name of the logger to get. If None, auto-infers from the calling module. Use `""` for root logger. |
| `class_type` | type[Logger] | The logger class type to use. |
| `skip_frames` | int | Number of frames to skip when inferring logger name (default: 1). |
| `*args` | Any | Additional positional arguments (for future-proofing) |
| `level` | str \| int \| None | Exact log level to set on the logger. Accepts both string names (case-insensitive) and numeric values. If provided, sets the logger's level to this value. Defaults to None (no change). |
| `minimum` | bool \| None | If True, only set the level if it's more verbose (lower numeric value) than the current level. This prevents downgrading from a more verbose level (e.g., TRACE) to a less verbose one (e.g., DEBUG). If None, defaults to False. Only used when `level` is provided. |
| `**kwargs` | Any | Additional keyword arguments (for future-proofing) |

**Returns:**
- A logger instance of the specified type

**Raises:**
- `ValueError`: If an invalid log level is provided.

**Example:**
```python
from apathetic_utils import Logger, getLoggerOfType

class AppLogger(Logger):
    pass

logger = getLoggerOfType("my_app", AppLogger)

# Set exact log level
logger = getLoggerOfType("my_app", AppLogger, level="debug")

# Set minimum log level
logger = getLoggerOfType("my_app", AppLogger, level="info", minimum=True)
```

### registerLogger

```python
registerLogger(
    logger_name: str | None = None,
    logger_class: type[Logger] | None = None,
    *,
    target_python_version: tuple[int, int] | None = None,
    log_level_env_vars: list[str] | None = None,
    default_log_level: str | None = None,
    propagate: bool | None = None,
    compat_mode: bool | None = None
) -> None
```

Register a logger for use by `getLogger()`. This registers the logger name and extends the logging module with custom levels if needed.

If `logger_name` is not provided, the top-level package is automatically extracted from the calling module's `__package__` attribute.

If `logger_class` is provided and has an `extendLoggingModule()` method, it will be called to extend the logging module with custom levels and set the logger class. If `logger_class` is not provided, the default `Logger` class will be used.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger_name` | str \| None | The logger name to register. If None, auto-infers from the calling module. |
| `logger_class` | type[Logger] \| None | Optional logger class to use. If provided and the class has an `extendLoggingModule()` method, it will be called. If None, defaults to the standard `Logger` class. |
| `target_python_version` | tuple[int, int] \| None | Optional target Python version (major, minor) tuple. If provided, sets the target Python version in the registry permanently. Defaults to None (no change). |
| `log_level_env_vars` | list[str] \| None | Optional list of environment variable names to check for log level. If provided, sets the log level environment variables in the registry permanently. Defaults to None (no change). |
| `default_log_level` | str \| None | Optional default log level name. If provided, sets the default log level in the registry permanently. Defaults to None (no change). |
| `propagate` | bool \| None | Optional propagate setting. If provided, sets the propagate value in the registry permanently. If None, uses registered propagate setting or falls back to DEFAULT_PROPAGATE from constants.py. Defaults to None (no change). |
| `compat_mode` | bool \| None | Optional compatibility mode setting. If provided, sets the compatibility mode in the registry permanently. When `True`, enables stdlib-compatible behavior with no breaking changes (e.g., `getLogger(None)` returns root logger). When `False` (default), uses improved behavior with enhancements. If `None`, uses registered compatibility mode setting or defaults to `False`. Defaults to `None` (no change). |

**Example:**
```python
from apathetic_utils import registerLogger

registerLogger("my_app")
# Or let it auto-infer:
registerLogger()  # Uses top-level package name

# Or with a custom logger class:
from apathetic_utils import Logger

class AppLogger(Logger):
    pass

registerLogger("my_app", AppLogger)

# Or with convenience parameters to configure registry settings:
registerLogger(
    "my_app",
    target_python_version=(3, 10),
    log_level_env_vars=["MYAPP_LOG_LEVEL", "LOG_LEVEL"],
    default_log_level="info",
    propagate=False,
    compat_mode=True,  # Enable stdlib compatibility
)
```

### registerCompatibilityMode

```python
registerCompatibilityMode(compat_mode: bool) -> None
```

Register the compatibility mode setting for stdlib drop-in replacement.

This sets the compatibility mode that will be used when creating loggers. If not set, the library defaults to `False` (improved behavior with enhancements).

**Compatibility Modes:**

- **`compat_mode=False` (default):** Improved behavior with enhancements. May include changes from stdlib behavior (e.g., `getLogger(None)` auto-infers logger name from calling module).
- **`compat_mode=True`:** Standard library compatible behavior with no breaking changes. Restores stdlib behavior where possible (e.g., `getLogger(None)` returns root logger).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `compat_mode` | bool | Compatibility mode setting. When `True`, enables stdlib-compatible behavior with no breaking changes. When `False` (default), uses improved behavior with enhancements. |

**Example:**
```python
from apathetic_utils import registerCompatibilityMode

# Enable stdlib-compatible behavior (no breaking changes)
registerCompatibilityMode(compat_mode=True)
# Now getLogger(None) returns root logger (stdlib behavior)

# Use improved behavior with enhancements (default)
registerCompatibilityMode(compat_mode=False)
# Now getLogger(None) auto-infers logger name (improved behavior)
```

### getCompatibilityMode

```python
getCompatibilityMode() -> bool
```

Get the compatibility mode setting.

Returns the registered compatibility mode setting, or `False` (improved behavior) if not registered.

**Returns:**
- `bool`: Compatibility mode setting. `False` means improved behavior with enhancements (default). `True` means stdlib-compatible behavior with no breaking changes.

**Example:**
```python
from apathetic_utils import getCompatibilityMode

compat_mode = getCompatibilityMode()
print(compat_mode)  # False (default: improved behavior)
```

### registerLogLevelEnvVars

```python
registerLogLevelEnvVars(env_vars: list[str]) -> None
```

Register environment variable names to check for log level.

The environment variables will be checked in order, and the first non-empty value found will be used.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `env_vars` | list[str] | List of environment variable names to check (e.g., `["MYAPP_LOG_LEVEL", "LOG_LEVEL"]`) |

**Example:**
```python
from apathetic_utils import registerLogLevelEnvVars

registerLogLevelEnvVars(["MYAPP_LOG_LEVEL", "LOG_LEVEL"])
```

### registerDefaultLogLevel

```python
registerDefaultLogLevel(default_level: str) -> None
```

Register the default log level to use when no other source is found.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `default_level` | str | Default log level name (e.g., `"info"`, `"warning"`) |

**Example:**
```python
from apathetic_utils import registerDefaultLogLevel

registerDefaultLogLevel("warning")
```

### registerTargetPythonVersion

```python
registerTargetPythonVersion(version: tuple[int, int] | None) -> None
```

Register the target Python version for compatibility checking.

This sets the global target Python version that the library will use when checking for feature availability. Functions requiring a newer Python version than the registered target will raise a `NotImplementedError`, even if the runtime Python version is sufficient.

If not set, the library defaults to `TARGET_PYTHON_VERSION` (3.10) from constants.py.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `version` | tuple[int, int] \| None | A tuple (major, minor) representing the target Python version (e.g., `(3, 10)` for Python 3.10). If None, the registration is skipped. |

**Example:**
```python
from apathetic_utils import registerTargetPythonVersion

# Target Python 3.10
registerTargetPythonVersion((3, 10))

# Target Python 3.11
registerTargetPythonVersion((3, 11))
```

**Note:** This is useful when developing on a newer Python version (e.g., 3.12) but targeting an older version (e.g., 3.10). The library will validate function calls against your target version, preventing accidental use of features that don't exist in your target environment.

### registerPropagate

```python
registerPropagate(*, propagate: bool | None) -> None
```

Register the propagate setting for loggers.

This sets the default propagate value that will be used when creating loggers. If not set, the library defaults to `DEFAULT_PROPAGATE` (False) from constants.py.

When `propagate` is `False`, loggers do not propagate messages to parent loggers, avoiding duplicate root logs.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `propagate` | bool \| None | Propagate setting (True or False). If None, the registration is skipped. |

**Example:**
```python
from apathetic_utils import registerPropagate

# Enable propagation (messages propagate to parent loggers)
registerPropagate(propagate=True)

# Disable propagation (default, avoids duplicate logs)
registerPropagate(propagate=False)
```

### safeLog

```python
safeLog(msg: str) -> None
```

Emergency logger that never fails.

This function bypasses the normal logging system and writes directly to `sys.__stderr__`. It's designed for use in error handlers where the logging system itself might be broken.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |

**Example:**
```python
from apathetic_utils import safeLog

try:
    # Some operation
    pass
except Exception:
    safeLog("Critical error: logging system may be broken")
```

### safeTrace

```python
safeTrace(label: str, *args: Any, icon: str = "🧪") -> None
```

Debug tracing function for test development. Only active when `safeTrace` environment variable is set.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | str | Trace label |
| `*args` | Any | Additional arguments to trace |
| `icon` | str | Icon to use (default: `"🧪"`) |

### makeSafeTrace

```python
makeSafeTrace(icon: str = "🧪") -> Callable
```

Create a test trace function with a custom icon.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `icon` | str | Icon to use |

**Returns:**
- `Callable`: Test trace function

### hasLogger

```python
hasLogger(logger_name: str) -> bool
```

Check if a logger exists in the logging manager's registry.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger_name` | str | The name of the logger to check |

**Returns:**
- `bool`: True if the logger exists, False otherwise

### removeLogger

```python
removeLogger(logger_name: str) -> None
```

Remove a logger from the logging manager's registry.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger_name` | str | The name of the logger to remove |

### getDefaultLoggerName

```python
getDefaultLoggerName(
    logger_name: str | None = None,
    *,
    check_registry: bool = True,
    skip_frames: int = 1,
    raise_on_error: bool = False,
    infer: bool = True,
    register: bool = False
) -> str | None
```

Get default logger name with optional inference from caller's frame.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger_name` | str \| None | Explicit logger name, or None to infer (default: None) |
| `check_registry` | bool | If True, check registry before inferring (default: True) |
| `skip_frames` | int | Number of frames to skip (default: 1) |
| `raise_on_error` | bool | If True, raise RuntimeError if logger name cannot be resolved. If False (default), return None instead |
| `infer` | bool | If True (default), attempt to infer logger name from caller's frame when not found in registry. If False, skip inference |
| `register` | bool | If True, store inferred name in registry. If False (default), do not modify registry. Note: Explicit names are never stored regardless of this parameter |

**Returns:**
- `str | None`: Resolved logger name, or None if cannot be resolved and raise_on_error=False

**Raises:**
- `RuntimeError`: If logger name cannot be resolved and raise_on_error=True

### getLogLevelEnvVars

```python
getLogLevelEnvVars() -> list[str]
```

Get the environment variable names to check for log level.

Returns the registered environment variable names, or the default environment variables if none are registered.

**Returns:**
- `list[str]`: List of environment variable names to check for log level. Defaults to `["LOG_LEVEL"]` if not registered

### getDefaultLogLevel

```python
getDefaultLogLevel() -> str
```

Get the default log level.

Returns the registered default log level, or the module default if none is registered.

**Returns:**
- `str`: Default log level name (e.g., "detail", "info"). Defaults to `"detail"` if not registered

### getRegisteredLoggerName

```python
getRegisteredLoggerName() -> str | None
```

Get the registered logger name.

Returns the registered logger name, or None if no logger name has been registered. Unlike `getDefaultLoggerName()`, this does not perform inference - it only returns the explicitly registered value.

**Returns:**
- `str | None`: Registered logger name, or None if not registered

### getTargetPythonVersion

```python
getTargetPythonVersion() -> tuple[int, int]
```

Get the target Python version.

Returns the registered target Python version, or the minimum supported version if none is registered.

**Returns:**
- `tuple[int, int]`: Target Python version as (major, minor) tuple. Defaults to `(3, 10)` if not registered

### getDefaultPropagate

```python
getDefaultPropagate() -> bool
```

Get the default propagate setting.

Returns the registered propagate setting, or the module default if none is registered.

**Returns:**
- `bool`: Default propagate setting (True or False). Defaults to `False` if not registered

### basicConfig

```python
basicConfig(*args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.basicConfig()`. Configure the logging system.

For detailed documentation, see the [Python logging.basicConfig() documentation](https://docs.python.org/3/library/logging.html#logging.basicConfig).

### addLevelName

```python
addLevelName(level: int, level_name: str) -> None
```

Wrapper for `logging.addLevelName()`. Associate a level name with a numeric level.

For detailed documentation, see the [Python logging.addLevelName() documentation](https://docs.python.org/3/library/logging.html#logging.addLevelName).

### getLevelName

```python
getLevelName(level: int | str, *, strict: bool = False) -> str | int
```

Return the textual or numeric representation of a logging level.

Behavior depends on compatibility mode (set via `registerCompatibilityMode()`):

**Compatibility mode enabled (`compat_mode=True`):**
- Behaves like stdlib `logging.getLevelName()` (bidirectional)
- Returns `str` for integer input, `int` for string input (known levels)
- Returns `"Level {level}"` string for unknown levels
- Value-add: Uppercases string inputs before processing (case-insensitive)

**Compatibility mode disabled (`compat_mode=False`, default):**
- Accepts both integer and string input
- For string input: uppercases and returns the string (value-add, no conversion)
- For integer input: returns level name as string (never returns `int`)
- Optional strict mode to raise `ValueError` for unknown integer levels

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int \| str | Log level as integer or string name |
| `strict` | bool | If True, raise ValueError for unknown levels. If False (default), returns "Level {level}" format for unknown integer levels (matching stdlib behavior). Only used when compatibility mode is disabled and level is an integer. |

**Returns:**
- Compatibility mode enabled: `str | int` (bidirectional like stdlib)
- Compatibility mode disabled: `str` (always string; string input is uppercased and returned, int input is converted to name)

**Raises:**
- `ValueError`: If strict=True and level is an integer that cannot be resolved to a known level name

**Example:**
```python
from apathetic_utils import getLevelName, getLevelNumber, registerCompatibilityMode

# Compatibility mode enabled (stdlib-like behavior):
registerCompatibilityMode(compat_mode=True)
getLevelName(10)  # "DEBUG" (str)
getLevelName("DEBUG")  # 10 (int)
getLevelName("debug")  # 10 (int, case-insensitive)

# Compatibility mode disabled (improved behavior):
registerCompatibilityMode(compat_mode=False)
getLevelName(10)  # "DEBUG"
getLevelName("DEBUG")  # "DEBUG" (uppercased and returned)
getLevelName("debug")  # "DEBUG" (uppercased)
getLevelName(999, strict=True)  # ValueError: Unknown log level: 999

# For string→int conversion when compat mode disabled, use getLevelNumber()
getLevelNumber("DEBUG")  # 10
```

### getLevelNumber

```python
getLevelNumber(level: str | int) -> int
```

Convert a log level name to its numeric value.

Recommended way to convert string level names to integers. This function explicitly performs string→int conversion, unlike `getLevelName()` which has bidirectional behavior for backward compatibility.

Handles all levels registered via `logging.addLevelName()` (including standard library levels, custom apathetic levels, and user-registered levels).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | str \| int | Log level as string name (case-insensitive) or integer |

**Returns:**
- `int`: Integer level value

**Raises:**
- `ValueError`: If level cannot be resolved to a known level

**Example:**
```python
from apathetic_utils import getLevelNumber

# Known levels return int
getLevelNumber("DEBUG")  # 10
getLevelNumber("TRACE")  # 5
getLevelNumber(20)       # 20

# Unknown level raises ValueError
getLevelNumber("UNKNOWN")  # ValueError: Unknown log level: 'UNKNOWN'
```

**See Also:**
- `getLevelName()` - Bidirectional conversion with compatibility mode
- `getLevelNameStr()` - Unidirectional conversion (always returns string)

### getLevelNameStr

```python
getLevelNameStr(level: int | str, *, strict: bool = False) -> str
```

Convert a log level to its string name representation.

Unidirectional function that always returns a string. This is the recommended way to convert log levels to strings when you want guaranteed string output without compatibility mode behavior.

Unlike `getLevelName()` which has compatibility mode and bidirectional behavior, this function always returns a string:
- Integer input: converts to level name string (returns "Level {level}" for unknown levels unless strict=True)
- String input: validates level exists, then returns uppercased string

Handles all levels registered via `logging.addLevelName()` (including standard library levels, custom apathetic levels, and user-registered levels).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int \| str | Log level as integer or string name (case-insensitive) |
| `strict` | bool | If True, raise ValueError for unknown integer levels. If False (default), returns "Level {level}" format for unknown integer levels (matching stdlib behavior). |

**Returns:**
- `str`: Level name as uppercase string

**Raises:**
- `ValueError`: If string level cannot be resolved to a known level, or if strict=True and integer level cannot be resolved to a known level

**Example:**
```python
from apathetic_utils import getLevelNameStr

# Integer input converts to level name
getLevelNameStr(10)  # "DEBUG"
getLevelNameStr(5)   # "TRACE"
getLevelNameStr(20)  # "INFO"

# String input validates and returns uppercased string
getLevelNameStr("DEBUG")  # "DEBUG"
getLevelNameStr("debug")  # "DEBUG"
getLevelNameStr("Info")  # "INFO"

# Unknown integer levels return "Level {level}" format (strict=False, default)
getLevelNameStr(999)  # "Level 999"

# Unknown integer levels raise ValueError when strict=True
getLevelNameStr(999, strict=True)  # ValueError: Unknown log level: 999

# Unknown string input raises ValueError
getLevelNameStr("UNKNOWN")  # ValueError: Unknown log level: 'UNKNOWN'
```

**See Also:**
- `getLevelNumber()` - Convert string to int (complementary function)
- `getLevelName()` - Bidirectional conversion with compatibility mode

### getLevelNamesMapping

```python
getLevelNamesMapping() -> dict[int, str]
```

**Requires Python 3.11+**

Wrapper for `logging.getLevelNamesMapping()`. Get mapping of level names to numeric values.

For detailed documentation, see the [Python logging.getLevelNamesMapping() documentation](https://docs.python.org/3.11/library/logging.html#logging.getLevelNamesMapping).

### getLoggerClass

```python
getLoggerClass() -> type[logging.Logger]
```

Wrapper for `logging.getLoggerClass()`. Return the class to be used when instantiating a logger.

For detailed documentation, see the [Python logging.getLoggerClass() documentation](https://docs.python.org/3/library/logging.html#logging.getLoggerClass).

### setLoggerClass

```python
setLoggerClass(klass: type[logging.Logger]) -> None
```

Wrapper for `logging.setLoggerClass()`. Set the class to be used when instantiating a logger.

For detailed documentation, see the [Python logging.setLoggerClass() documentation](https://docs.python.org/3/library/logging.html#logging.setLoggerClass).

### getLogRecordFactory

```python
getLogRecordFactory() -> Callable
```

Wrapper for `logging.getLogRecordFactory()`. Return the factory function used to create LogRecords.

For detailed documentation, see the [Python logging.getLogRecordFactory() documentation](https://docs.python.org/3/library/logging.html#logging.getLogRecordFactory).

### setLogRecordFactory

```python
setLogRecordFactory(factory: Callable) -> None
```

Wrapper for `logging.setLogRecordFactory()`. Set the factory function used to create LogRecords.

For detailed documentation, see the [Python logging.setLogRecordFactory() documentation](https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory).

### shutdown

```python
shutdown() -> None
```

Wrapper for `logging.shutdown()`. Perform an orderly shutdown of the logging system.

For detailed documentation, see the [Python logging.shutdown() documentation](https://docs.python.org/3/library/logging.html#logging.shutdown).

### disable

```python
disable(level: int) -> None
```

Wrapper for `logging.disable()`. Disable all logging calls of severity 'level' and below.

For detailed documentation, see the [Python logging.disable() documentation](https://docs.python.org/3/library/logging.html#logging.disable).

### captureWarnings

```python
captureWarnings(capture: bool) -> None
```

Wrapper for `logging.captureWarnings()`. Capture warnings issued by the warnings module.

For detailed documentation, see the [Python logging.captureWarnings() documentation](https://docs.python.org/3/library/logging.html#logging.captureWarnings).

### critical

```python
critical(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.critical()`. Log a message with severity CRITICAL.

For detailed documentation, see the [Python logging.critical() documentation](https://docs.python.org/3/library/logging.html#logging.critical).

### debug

```python
debug(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.debug()`. Log a message with severity DEBUG.

For detailed documentation, see the [Python logging.debug() documentation](https://docs.python.org/3/library/logging.html#logging.debug).

### error

```python
error(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.error()`. Log a message with severity ERROR.

For detailed documentation, see the [Python logging.error() documentation](https://docs.python.org/3/library/logging.html#logging.error).

### exception

```python
exception(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.exception()`. Log a message with severity ERROR with exception info.

For detailed documentation, see the [Python logging.exception() documentation](https://docs.python.org/3/library/logging.html#logging.exception).

### fatal

```python
fatal(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.fatal()`. Log a message with severity CRITICAL.

For detailed documentation, see the [Python logging.fatal() documentation](https://docs.python.org/3/library/logging.html#logging.fatal).

### info

```python
info(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.info()`. Log a message with severity INFO.

For detailed documentation, see the [Python logging.info() documentation](https://docs.python.org/3/library/logging.html#logging.info).

### log

```python
log(level: int, msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.log()`. Log a message with an explicit level.

For detailed documentation, see the [Python logging.log() documentation](https://docs.python.org/3/library/logging.html#logging.log).

### warn

```python
warn(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.warn()`. Log a message with severity WARNING.

For detailed documentation, see the [Python logging.warn() documentation](https://docs.python.org/3/library/logging.html#logging.warn).

### warning

```python
warning(msg: str, *args: Any, **kwargs: Any) -> None
```

Wrapper for `logging.warning()`. Log a message with severity WARNING.

For detailed documentation, see the [Python logging.warning() documentation](https://docs.python.org/3/library/logging.html#logging.warning).

### trace

```python
trace(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message with severity TRACE on the root logger.

TRACE is more verbose than DEBUG. This function gets an `apathetic_utils.Logger` instance (ensuring the root logger is an apathetic logger) and calls its `trace()` method.

If the logger has no handlers, `basicConfig()` is automatically called to add a console handler with a pre-defined format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments for message formatting |
| `**kwargs` | Any | Additional keyword arguments (e.g., `exc_info`, `stacklevel`) |

**Example:**
```python
import apathetic_utils

# Log a trace message
apathetic_utils.trace("Detailed trace information: %s", variable)
```

### detail

```python
detail(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message with severity DETAIL on the root logger.

DETAIL is more detailed than INFO. This function gets an `apathetic_utils.Logger` instance (ensuring the root logger is an apathetic logger) and calls its `detail()` method.

If the logger has no handlers, `basicConfig()` is automatically called to add a console handler with a pre-defined format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments for message formatting |
| `**kwargs` | Any | Additional keyword arguments (e.g., `exc_info`, `stacklevel`) |

**Example:**
```python
import apathetic_utils

# Log a detail message
apathetic_utils.detail("Additional detail: %s", information)
```

### minimal

```python
minimal(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message with severity MINIMAL on the root logger.

MINIMAL is less detailed than INFO. This function gets an `apathetic_utils.Logger` instance (ensuring the root logger is an apathetic logger) and calls its `minimal()` method.

If the logger has no handlers, `basicConfig()` is automatically called to add a console handler with a pre-defined format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments for message formatting |
| `**kwargs` | Any | Additional keyword arguments (e.g., `exc_info`, `stacklevel`) |

**Example:**
```python
import apathetic_utils

# Log a minimal message
apathetic_utils.minimal("Minimal information: %s", summary)
```

### getHandlerByName

```python
getHandlerByName(name: str) -> logging.Handler | None
```

**Requires Python 3.12+**

Wrapper for `logging.getHandlerByName()`. Get a handler with the specified name.

For detailed documentation, see the [Python logging.getHandlerByName() documentation](https://docs.python.org/3.12/library/logging.html#logging.getHandlerByName).

### getHandlerNames

```python
getHandlerNames() -> list[str]
```

**Requires Python 3.12+**

Wrapper for `logging.getHandlerNames()`. Return all known handler names.

For detailed documentation, see the [Python logging.getHandlerNames() documentation](https://docs.python.org/3.12/library/logging.html#logging.getHandlerNames).

### makeLogRecord

```python
makeLogRecord(
    name: str,
    level: int,
    fn: str,
    lno: int,
    msg: str,
    args: tuple,
    exc_info: Any
) -> logging.LogRecord
```

Wrapper for `logging.makeLogRecord()`. Create a LogRecord from the given parameters.

For detailed documentation, see the [Python logging.makeLogRecord() documentation](https://docs.python.org/3/library/logging.html#logging.makeLogRecord).

### currentframe

```python
currentframe(*args: Any, **kwargs: Any) -> FrameType | None
```

Wrapper for `logging.currentframe()`. Return the frame object for the caller's stack frame.

For detailed documentation, see the [Python logging.currentframe() documentation](https://docs.python.org/3/library/logging.html#logging.currentframe).

## 4. `apathetic_utils.Logger` Function Reference

### Constructor

```python
Logger(
    name: str,
    level: int = logging.NOTSET,
    *,
    enable_color: bool | None = None
)
```

Logger class for all Apathetic tools. Extends Python's standard `logging.Logger`.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Logger name |
| `level` | int | Initial log level (defaults to `logging.NOTSET`) |
| `enable_color` | bool \| None | Whether to enable colorized output. If None, auto-detects based on TTY and environment variables. |

### setLevel

```python
setLevel(level: int | str, *, minimum: bool | None = False) -> None
```

Set the logging level. Accepts both string names (case-insensitive) and numeric values.

**Changed from stdlib:** Accepts string level names and has a `minimum` parameter.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int \| str | Log level name or numeric value |
| `minimum` | bool \| None | If True, only set the level if it's more verbose (lower numeric value) than the current level. Defaults to False. |

**Example:**
```python
logger.setLevel("debug")
logger.setLevel(logging.DEBUG)
```

### determineLogLevel

```python
determineLogLevel(
    *,
    args: argparse.Namespace | None = None,
    root_log_level: str | None = None
) -> str
```

Resolve log level from CLI → env → root config → default.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `args` | argparse.Namespace \| None | Parsed command-line arguments (checks for `args.log_level`) |
| `root_log_level` | str \| None | Root logger level to use as fallback |

**Returns:**
- `str`: Resolved log level name (uppercase)

**Example:**
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--log-level", default="info")
args = parser.parse_args()

level = logger.determineLogLevel(args=args)
logger.setLevel(level)
```

### determineColorEnabled

```python
determineColorEnabled() -> bool
```

Return True if colored output should be enabled. (classmethod)

Checks:
- `NO_COLOR` environment variable (disables colors)
- `FORCE_COLOR` environment variable (enables colors)
- TTY detection (enables colors if stdout is a TTY)

**Returns:**
- `bool`: True if colors should be enabled

### extendLoggingModule

```python
extendLoggingModule() -> bool
```

Extend Python's logging module with TRACE and SILENT levels. (classmethod)

This method:
- Sets `apathetic_utils.Logger` as the default logger class
- Adds `TRACE` and `SILENT` level names
- Adds `logging.TRACE` and `logging.SILENT` constants

**Returns:**
- `bool`: True if the extension ran, False if it was already extended

### trace

```python
trace(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message at TRACE level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments (e.g., `exc_info`, `stacklevel`) |

### detail

```python
detail(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message at DETAIL level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

### minimal

```python
minimal(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message at MINIMAL level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

### test

```python
test(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message at TEST level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Message to log |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

### errorIfNotDebug

```python
errorIfNotDebug(msg: str, *args: Any, **kwargs: Any) -> None
```

Log an error with full traceback only if debug/trace is enabled.

If debug mode is enabled, shows full exception traceback. Otherwise, shows only the error message.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Error message |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

**Example:**
```python
try:
    risky_operation()
except Exception:
    logger.errorIfNotDebug("Operation failed")
```

### criticalIfNotDebug

```python
criticalIfNotDebug(msg: str, *args: Any, **kwargs: Any) -> None
```

Log a critical error with full traceback only if debug/trace is enabled.

Similar to `errorIfNotDebug()` but logs at CRITICAL level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | Error message |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

### colorize

```python
colorize(text: str, color: str, *, enable_color: bool | None = None) -> str
```

Apply ANSI color codes to text.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | str | Text to colorize |
| `color` | str | ANSI color code (e.g., `ANSIColors.CYAN`, `ANSIColors.RED`) |
| `enable_color` | bool \| None | Override color enablement. If None, uses instance setting. |

**Returns:**
- `str`: Colorized text (or original text if colors disabled)

### logDynamic

```python
logDynamic(level: str | int, msg: str, *args: Any, **kwargs: Any) -> None
```

Log a message at a dynamically specified level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | str \| int | Log level name or numeric value |
| `msg` | str | Message to log |
| `*args` | Any | Format arguments |
| `**kwargs` | Any | Additional keyword arguments |

**Example:**
```python
logger.logDynamic("warning", "This is a warning")
logger.logDynamic(logging.ERROR, "This is an error")
```

### useLevel

```python
useLevel(level: str | int, *, minimum: bool = False) -> ContextManager
```

Context manager to temporarily change log level.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | str \| int | Log level to use |
| `minimum` | bool | If True, only set the level if it's more verbose (lower numeric value) than the current level. Prevents downgrading from a more verbose level. |

**Returns:**
- Context manager that restores the previous level on exit

**Example:**
```python
with logger.useLevel("debug"):
    logger.debug("This will be shown")

# Level is restored after the context
```

### levelName

```python
levelName: str
```

Return the explicit level name set on this logger (read-only property).

This property returns the name of the level explicitly set on this logger.
For the effective level name (what's actually used, considering inheritance),
use `effectiveLevelName` instead.

**Example:**
```python
logger.setLevel("debug")
print(logger.levelName)  # "DEBUG"
```

### effectiveLevel

```python
effectiveLevel: int
```

Return the effective level (what's actually used) (read-only property).

This property returns the effective logging level for this logger, considering
inheritance from parent loggers. This is the preferred way to get the effective
level. Also available via `getEffectiveLevel()` for stdlib compatibility.

**Example:**
```python
parent = getLogger("parent")
parent.setLevel("info")

child = getLogger("parent.child")
print(child.level)  # 0 (NOTSET - explicit)
print(child.effectiveLevel)  # 20 (INFO - effective, from parent)
```

### effectiveLevelName

```python
effectiveLevelName: str
```

Return the effective level name (what's actually used) (read-only property).

This property returns the name of the effective logging level for this logger,
considering inheritance from parent loggers. This is the preferred way to get
the effective level name. Also available via `getEffectiveLevelName()` for
consistency.

**Example:**
```python
parent = getLogger("parent")
parent.setLevel("info")

child = getLogger("parent.child")
print(child.levelName)  # "NOTSET" (explicit)
print(child.effectiveLevelName)  # "INFO" (effective, from parent)
```

### getLevel

```python
getLevel() -> int
```

Return the explicit level set on this logger.

This method returns the level explicitly set on this logger (same as `level`
property). For the effective level, use `getEffectiveLevel()` or the
`effectiveLevel` property.

**Returns:**
- `int`: The explicit level value set on this logger

**Example:**
```python
logger.setLevel("debug")
print(logger.getLevel())  # 10
```

### getLevelName

```python
getLevelName() -> str
```

Return the explicit level name set on this logger.

This method returns the name of the level explicitly set on this logger (same
as `levelName` property). For the effective level name, use
`getEffectiveLevelName()` or the `effectiveLevelName` property.

**Returns:**
- `str`: The explicit level name set on this logger

**Example:**
```python
logger.setLevel("debug")
print(logger.getLevelName())  # "DEBUG"
```

### getEffectiveLevelName

```python
getEffectiveLevelName() -> str
```

Return the effective level name (what's actually used).

This method returns the name of the effective logging level for this logger,
considering inheritance from parent loggers. Prefer the `effectiveLevelName` property
for convenience, or use this method for consistency with `getEffectiveLevel()`.

**Returns:**
- `str`: The effective level name for this logger

**Example:**
```python
parent = getLogger("parent")
parent.setLevel("info")

child = getLogger("parent.child")
print(child.getEffectiveLevelName())  # "INFO" (from parent)
```

### getChildren

```python
getChildren() -> set[logging.Logger]
```

**Requires Python 3.12+**

Return a set of loggers that are immediate children of this logger.

This method returns only the direct children of the logger (loggers whose names are one level deeper in the hierarchy). For example, if you have loggers named `foo`, `foo.bar`, and `foo.bar.baz`, calling `getLogger("foo").getChildren()` will return a set containing only the `foo.bar` logger, not `foo.bar.baz`.

**Returns:**
- `set[logging.Logger]`: A set of Logger instances that are immediate children of this logger

**Example:**
```python
from apathetic_utils import getLogger

root = getLogger("")
foo = getLogger("foo")
bar = getLogger("foo.bar")
baz = getLogger("foo.bar.baz")

# Get immediate children of root logger
children = root.getChildren()  # {foo logger}

# Get immediate children of foo logger
children = foo.getChildren()  # {bar logger}

# Get immediate children of bar logger
children = bar.getChildren()  # {baz logger}
```

For detailed documentation, see the [Python logging.Logger.getChildren() documentation](https://docs.python.org/3.12/library/logging.html#logging.Logger.getChildren).

### ensureHandlers

```python
ensureHandlers() -> None
```

Ensure handlers are attached to this logger.

DualStreamHandler is what will ensure logs go to the write channel.
Rebuilds handlers if they're missing or if stdout/stderr have changed.

### validateLevelPositive

```python
validateLevelPositive(level: int, *, level_name: str | None = None) -> None
```

Validate that a level value is positive (> 0). (staticmethod)

Custom levels with values <= 0 will inherit from the root logger,
causing NOTSET inheritance issues.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int | The numeric level value to validate |
| `level_name` | str \| None | Optional name for the level (for error messages). If None, will attempt to get from getLevelName() |

**Raises:**
- `ValueError`: If level <= 0

**Example:**
```python
Logger.validateLevelPositive(5, level_name="TRACE")
Logger.validateLevelPositive(0, level_name="TEST")
# ValueError: Level 'TEST' has value 0...
```

### _log

```python
_log(level: int, msg: str, args: tuple[Any, ...], **kwargs: Any) -> None
```

Log a message with the specified level.

**Changed from stdlib:** Automatically ensures handlers are attached via `ensureHandlers()`.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int | The numeric logging level |
| `msg` | str | The message format string |
| `args` | tuple[Any, ...] | Arguments for the message format string |
| `**kwargs` | Any | Additional keyword arguments passed to the base implementation |

### addLevelName

```python
addLevelName(level: int, level_name: str) -> None
```

Associate a level name with a numeric level. (staticmethod)

**Changed from stdlib:** Validates that level value is positive (> 0) to prevent NOTSET
inheritance issues. Sets `logging.<LEVEL_NAME>` attribute for convenience.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `level` | int | The numeric level value (must be > 0 for custom levels) |
| `level_name` | str | The name to associate with this level |

**Raises:**
- `ValueError`: If level <= 0 (which would cause NOTSET inheritance)
- `ValueError`: If `logging.<LEVEL_NAME>` already exists with an invalid value

## Classes

### TagFormatter

Custom formatter that adds colored tags to log messages.

#### Constructor

```python
TagFormatter(format: str)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `format` | str | Format string (typically `"%(message)s"`) |

The formatter automatically adds tags based on log level:
- `TRACE` → `[TRACE]` (gray)
- `DEBUG` → `[DEBUG]` (cyan)
- `WARNING` → `⚠️`
- `ERROR` → `❌`
- `CRITICAL` → `💥`

### DualStreamHandler

Stream handler that routes messages to stdout or stderr based on log level.

- **stdout**: Used for INFO messages
- **stderr**: Used for TRACE, DEBUG, WARNING, ERROR, and CRITICAL messages

#### Constructor

```python
DualStreamHandler()
```

#### Properties

##### `enable_color: bool`

Whether to enable colorized output for this handler.

## Constants

### Log Levels

- `TRACE_LEVEL` — Numeric value for TRACE level (`logging.DEBUG - 5`)
- `SILENT_LEVEL` — Numeric value for SILENT level (`logging.CRITICAL + 1`)
- `LEVEL_ORDER` — List of all log level names in order: `["trace", "debug", "info", "warning", "error", "critical", "silent"]`

### ANSI Colors

Access via `ANSIColors` class:

- `ANSIColors.RESET` — ANSI reset code (`\033[0m`)
- `ANSIColors.CYAN` — Cyan color (`\033[36m`)
- `ANSIColors.YELLOW` — Yellow color (`\033[93m`)
- `ANSIColors.RED` — Red color (`\033[91m`)
- `ANSIColors.GREEN` — Green color (`\033[92m`)
- `ANSIColors.GRAY` — Gray color (`\033[90m`)

**Example:**
```python
from apathetic_utils import ANSIColors

message = f"{ANSIColors.CYAN}Colored text{ANSIColors.RESET}"
```

### Tag Styles

- `TAG_STYLES` — Dictionary mapping level names to (color, tag_text) tuples

### Defaults

- `DEFAULT_APATHETIC_LOG_LEVEL` — Default log level string (`"info"`)
- `DEFAULT_APATHETIC_LOG_LEVEL_ENV_VARS` — Default environment variable names (`["LOG_LEVEL"]`)

## Testing Utilities

### safeTrace(label: str, *args: Any, icon: str = "🧵") -> None

Debug tracing function for test development. Only active when `safeTrace` environment variable is set.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `label` | str | Trace label |
| `*args` | Any | Additional arguments to trace |
| `icon` | str | Icon to use (default: `"🧵"`) |

### makeSafeTrace(icon: str = "🧵") -> Callable

Create a test trace function with a custom icon.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `icon` | str | Icon to use |

**Returns:**
- `Callable`: Test trace function

### safeTrace_ENABLED: bool

Boolean flag indicating if test tracing is enabled (checks `safeTrace` environment variable).

## Compatibility Mode

This library provides two modes of operation:

### Default Mode (Improved Behavior)

When compatibility mode is **disabled** (`compat_mode=False`, the default), the library provides improved behavior with enhancements over the standard library:

- **Auto-inference:** `getLogger(None)` auto-infers the logger name from the calling module's `__package__` attribute, making it easier to use the logger without explicitly registering a name.
- **Enhanced features:** Additional improvements and quality-of-life enhancements.

### Compatibility Mode (Standard Library Compatible)

When compatibility mode is **enabled** (`compat_mode=True`), the library maintains standard library compatible behavior with **no breaking changes**:

- **Stdlib behavior:** `getLogger(None)` returns the root logger (matching standard library behavior).
- **Full compatibility:** All behavior matches the Python standard library `logging` module.

### Enabling Compatibility Mode

To enable compatibility mode for stdlib-compatible behavior:

```python
from apathetic_utils import registerCompatibilityMode

registerCompatibilityMode(compat_mode=True)
# Now getLogger(None) returns root logger (stdlib behavior)
```

You can also set it when registering a logger:

```python
from apathetic_utils import registerLogger

registerLogger("my_app", compat_mode=True)
```

### Behavior Differences

**`getLogger(None)` behavior:**

- **Default mode (`compat_mode=False`):** Auto-infers logger name from calling module (improved behavior)
- **Compatibility mode (`compat_mode=True`):** Returns root logger (stdlib behavior)

**To get root logger in default mode:**

```python
logger = getLogger("")  # Returns root logger (works in both modes)
```

See [`registerCompatibilityMode()`](#registercompatibilitymode) for more details.
