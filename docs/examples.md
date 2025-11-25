---
layout: base
title: Examples
permalink: /examples/
---

# Usage Examples

Advanced usage patterns and examples for Apathetic Python Utils.

## Basic CLI Application

A complete example of a command-line application using Apathetic Python Utils:

```python
#!/usr/bin/env python3
"""Example CLI application with Apathetic Logging."""

import argparse
import sys
from apathetic_utils import getLogger, registerLogger

def main():
    parser = argparse.ArgumentParser(description="Example CLI tool")
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["trace", "debug", "info", "warning", "error", "critical", "silent"],
        help="Set the log level",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Register logger
    registerLogger("example_cli")
    logger = getLogger()
    
    # Set log level from arguments
    if args.verbose:
        logger.setLevel("debug")
    else:
        logger.setLevel(args.log_level)
    
    # Use the logger
    logger.info("Application started")
    logger.debug("Debug information (only shown with --verbose or --log-level debug)")
    
    try:
        # Your application logic here
        result = process_data()
        logger.info(f"Processing complete: {result}")
    except Exception:
        logger.errorIfNotDebug("Processing failed")
        sys.exit(1)

def process_data():
    """Example processing function."""
    return "success"

if __name__ == "__main__":
    main()
```

## Context Manager for Temporary Verbosity

Temporarily increase verbosity for specific operations:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()

# Normal operation
logger.info("Starting operation")

# Temporarily enable debug for a specific block
with logger.useLevel("debug"):
    logger.debug("Detailed step 1")
    logger.debug("Detailed step 2")
    logger.trace("Very detailed trace")

# Back to normal level
logger.info("Operation complete")
```

## Conditional Exception Logging

Show full tracebacks only in debug mode:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()

def risky_operation():
    """An operation that might fail."""
    raise ValueError("Something went wrong")

try:
    risky_operation()
except Exception:
    # Full traceback only if debug/trace is enabled
    logger.errorIfNotDebug("Risky operation failed")
    # In production (info level), users see: "❌ Risky operation failed"
    # In development (debug level), users see full traceback
```

## Custom Environment Variables

Register custom environment variables for log level:

```python
from apathetic_utils import (
    getLogger,
    registerLogger,
    registerLogLevelEnvVars,
    registerDefaultLogLevel,
)

# Use custom environment variable names
registerLogLevelEnvVars(["MYAPP_LOG_LEVEL", "APP_LOG_LEVEL", "LOG_LEVEL"])

# Set a custom default
registerDefaultLogLevel("warning")

registerLogger("my_app")
logger = getLogger()

# Logger will check MYAPP_LOG_LEVEL, then APP_LOG_LEVEL, then LOG_LEVEL
# If none are set, defaults to "warning"
logger.info("This might not show if default is warning")
```

## Integration with argparse

Seamless integration with argparse for CLI tools:

```python
import argparse
from apathetic_utils import getLogger, registerLogger

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level",
        default=None,  # Let logger determine from env/default
        choices=["trace", "debug", "info", "warning", "error", "critical", "silent"],
        help="Set the log level",
    )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    registerLogger("my_cli")
    logger = getLogger()
    
    # Determine log level from args, env, or default
    level = logger.determineLogLevel(args=args)
    logger.setLevel(level)
    
    logger.info("CLI tool started")
    logger.debug("Debug mode enabled")
```

## Dynamic Log Levels

Log at different levels dynamically:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()

# Log at different levels based on conditions
def log_result(success: bool, message: str):
    if success:
        logger.logDynamic("info", message)
    else:
        logger.logDynamic("error", message)

# Or use numeric levels
import logging
logger.logDynamic(logging.WARNING, "This is a warning")
```

## Color Customization

Work with colors directly:

```python
from apathetic_utils import apathetic_utils, ANSIColors

# Create logger with explicit color control
logger = ApatheticLogger("my_app", enable_color=True)

# Use colorize method
colored_text = logger.colorize("Important message", ANSIColors.RED)
print(colored_text)

# Or use color constants directly
message = f"{ANSIColors.CYAN}This is cyan{ANSIColors.RESET}"
print(message)
```

## Testing with Logger

Example of using the logger in tests:

```python
import pytest
from apathetic_utils import getLogger, registerLogger

@pytest.fixture
def logger():
    registerLogger("test_app")
    logger = getLogger()
    logger.setLevel("debug")  # Verbose for tests
    return logger

def test_operation(logger):
    logger.info("Starting test")
    # Test logic here
    logger.debug("Test step completed")
    assert True
```

## Silent Mode

Completely disable logging:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()

# Enable silent mode
logger.setLevel("silent")

# These won't be shown
logger.info("This won't show")
logger.error("This won't show either")
logger.critical("Even this won't show")

# Re-enable logging
logger.setLevel("info")
logger.info("Now this will show")
```

## Multi-Module Application

Using the logger across multiple modules:

```main.py```
```python
from apathetic_utils import registerLogger
import module_a
import module_b

# Register once at application entry point
registerLogger("my_app")

# Modules can now use getLogger()
module_a.do_something()
module_b.do_something_else()
```

```module_a.py```
```python
from apathetic_utils import getLogger

logger = getLogger()  # Gets the "my_app" logger

def do_something():
    logger.info("Module A doing something")
```

```module_b.py```
```python
from apathetic_utils import getLogger

logger = getLogger()  # Gets the same "my_app" logger

def do_something_else():
    logger.info("Module B doing something else")
```

## Error Handling with Safe Logging

Use `safeLog` for critical error reporting:

```python
from apathetic_utils import safeLog, getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()

def critical_operation():
    try:
        # Some operation that might break logging
        pass
    except Exception as e:
        # If normal logging fails, use safeLog
        try:
            logger.critical(f"Critical error: {e}")
        except Exception:
            # Fallback to safeLog which never fails
            safeLog(f"CRITICAL: {e}")
        raise
```

## Minimum Level Context

Only increase verbosity, never decrease:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("my_app")
logger = getLogger()
logger.setLevel("trace")  # Most verbose

# This won't downgrade to debug (trace is more verbose)
with logger.useLevel("debug", minimum=True):
    logger.trace("This will still show (trace is more verbose)")
    logger.debug("This will also show")

# But if current level is info, this will upgrade to debug
logger.setLevel("info")
with logger.useLevel("debug", minimum=True):
    logger.debug("This will show (upgraded from info to debug)")
```

## Target Python Version Configuration

When developing on a newer Python version (e.g., 3.12) but targeting an older version (e.g., 3.10), you can register your target Python version to ensure compatibility:

```python
from apathetic_utils import (
    registerLogger,
    registerTargetPythonVersion,
    getLogger,
)

# Register your target Python version
# This ensures functions requiring 3.11+ will raise errors
# even if you're running on 3.12
registerTargetPythonVersion((3, 10))

# Register logger
registerLogger("my_app")
logger = getLogger()

# Now if you try to use a 3.11+ function, it will raise
# even though you're running on 3.12
try:
    from apathetic_utils import getLevelNamesMapping
    mapping = getLevelNamesMapping()  # Raises NotImplementedError on 3.10 target
except NotImplementedError as e:
    logger.warning(f"Function not available: {e}")
    # Error message will suggest raising target version if needed
```

**Why this matters:**
- Prevents accidental use of newer Python features during development
- Ensures your code works on your target Python version
- Error messages guide you to either avoid the function or raise your target version

**Example with convenience parameters:**
```python
from apathetic_utils import registerLogger

# Configure everything at once
registerLogger(
    "my_app",
    target_python_version=(3, 10),  # Target Python 3.10
    log_level_env_vars=["MYAPP_LOG_LEVEL", "LOG_LEVEL"],
    default_log_level="info",
    propagate=False,  # Don't propagate to root logger
)
```

These examples demonstrate the flexibility and power of Apathetic Python Utils. 

## Next Steps

- **[API Reference]({{ '/api' | relative_url }})** — Complete API documentation
- **[Quick Start Guide]({{ '/quickstart' | relative_url }})** — Get up and running quickly
- **[Custom Logger Guide]({{ '/custom-logger' | relative_url }})** — Learn how to create application-specific logger subclasses

