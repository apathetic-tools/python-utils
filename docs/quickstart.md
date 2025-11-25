---
layout: base
title: Quick Start
permalink: /quickstart/
---

# Quick Start Guide

Get up and running with Apathetic Python Utils in minutes.

## Basic Usage

The simplest way to use Apathetic Python Utils is to register a logger name and get a logger instance:

```python
from apathetic_utils import getLogger, registerLogger

# Register your logger
registerLogger("my_app")

# Get the logger instance
logger = getLogger()

# Start logging!
logger.info("Application started")
logger.debug("Debug information")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### Module-Level Convenience Functions

You can also use module-level convenience functions that log to the root logger:

```python
import apathetic_utils

# Standard levels
apathetic_utils.debug("Debug message")
apathetic_utils.info("Info message")
apathetic_utils.warning("Warning message")
apathetic_utils.error("Error message")
apathetic_utils.critical("Critical message")

# Custom levels
apathetic_utils.trace("Trace message")
apathetic_utils.detail("Detail message")
apathetic_utils.minimal("Minimal message")
```

These functions automatically ensure the root logger is an apathetic logger and handle configuration if needed.

## Log Levels

Apathetic Python Utils supports the following log levels (in order of verbosity):

- `trace` — Most verbose, for detailed tracing
- `debug` — Debug information
- `info` — General informational messages (default)
- `warning` — Warning messages
- `error` — Error messages
- `critical` — Critical errors
- `silent` — Disables all logging

### Setting Log Levels

You can set the log level in several ways:

#### 1. Environment Variable

```bash
export LOG_LEVEL=debug
python my_app.py
```

#### 2. Programmatically

```python
logger.setLevel("debug")  # Case-insensitive
logger.setLevel(logging.DEBUG)  # Or use logging constants
```

#### 3. Using Context Manager

Temporarily change the log level for a specific block:

```python
with logger.useLevel("debug"):
    logger.debug("This will be shown")
    logger.trace("This will also be shown if trace is enabled")
```

## Colorized Output

Apathetic Python Utils automatically detects if your terminal supports colors and enables colorized output by default.

### Color Detection

Colors are enabled when:
- Output is a TTY (terminal)
- `FORCE_COLOR` environment variable is set to `1`, `true`, or `yes`

Colors are disabled when:
- `NO_COLOR` environment variable is set
- Output is redirected to a file or pipe

### Manual Control

```python
from apathetic_utils import ApatheticLogging

# Create logger with colors explicitly enabled/disabled
logger = ApatheticLogger("my_app", enable_color=True)
```

## Tag Formatting

Log messages are automatically prefixed with tags:

- `[TRACE]` — Gray tag
- `[DEBUG]` — Cyan tag
- `⚠️` — Warning emoji
- `❌` — Error emoji
- `💥` — Critical emoji

## Dual-Stream Handling

Apathetic Python Utils automatically routes log messages to the appropriate stream:

- **stdout** — Used for normal output
- **stderr** — Used for errors and warnings

This ensures proper separation of output and error streams, which is important for CLI tools.

## Advanced Features

### Dynamic Log Levels

Log at different levels dynamically:

```python
logger.logDynamic("warning", "This is a warning")
logger.logDynamic(logging.ERROR, "This is an error")
```

### Conditional Exception Logging

Only show full tracebacks when debug mode is enabled:

```python
try:
    risky_operation()
except Exception:
    logger.errorIfNotDebug("Operation failed")
    # Full traceback only shown if debug/trace is enabled
```

### Temporary Level Changes

Use a context manager to temporarily change log levels:

```python
# Only set level if it's more verbose (won't downgrade from trace to debug)
with logger.useLevel("debug", minimum=True):
    logger.debug("This will be shown")
```

## Integration with CLI Tools

For command-line applications, you can integrate with `argparse`:

```python
import argparse
from apathetic_utils import getLogger, registerLogger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", default="info")
    args = parser.parse_args()
    
    registerLogger("my_cli")
    logger = getLogger()
    
    # Logger will automatically use args.log_level
    level = logger.determineLogLevel(args=args)
    logger.setLevel(level)
    
    logger.info("CLI tool started")
```

## Drop-in Replacement for stdlib logging

Apathetic Python Utils can be used as a drop-in replacement for Python's standard library `logging` module:

```python
# Instead of: import logging
import apathetic_utils as logging

# Works just like stdlib logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_app")  # Note: getLogger is CamelCase in stdlib
logger.info("Hello, world!")
logger.debug("Debug message")
logger.warning("Warning message")
```

> **Note:** When using `getLogger(None)`, the logger name is auto-inferred from the calling module (improved behavior). To get the root logger, use `getLogger("")` instead. For stdlib-compatible behavior where `getLogger(None)` returns the root logger, enable [Compatibility Mode]({{ '/api' | relative_url }}#compatibility-mode).

## Next Steps

- Read the [API Reference]({{ '/api' | relative_url }}) for complete documentation
- Check out [Examples]({{ '/examples' | relative_url }}) for more advanced patterns
- See [Contributing]({{ '/contributing' | relative_url }}) if you want to help improve the project

