---
layout: base
title: Home
permalink: /
---

# Apathetic Python Utils

**Minimal wrapper for the Python standard library logger.**  
*Because consistent logging shouldn't require large dependencies.*

*Apathetic Python Utils* provides a lightweight, dependency-free logging solution designed for CLI tools. It extends Python's standard library `logging` module with colorized output, dual-stream handling (stdout/stderr), extra logging levels, and seamless integration with Apathetic Tools projects.

## Features
- 🪶 **Zero dependencies** — Uses only Python's standard library
- 🔄 **Drop-in replacement** — Can be used as a drop-in replacement for stdlib `logging`
- 🐍 **stdlib-compatible** — Uses camelCase naming to match Python's standard library `logging` module
- 🔄 **Dual-stream handling** — Smart routing to stdout/stderr
- 📊 **Extra logging levels** — TEST, TRACE, DETAIL, MINIMAL, and SILENT levels for fine-grained control
- 🏷️ **Tag-based formatting** — Clean, readable log tags with emoji support
- 🎨 **Colorized output** — Automatic color detection with TTY support
- 🔧 **CLI-friendly** — Designed with command-line applications in mind
- 🧩 **Apathetic Tools integration** — Works seamlessly with serger and other Apathetic Tools


## Quick Example

```python
from apathetic_utils import getLogger, registerLogger

# Register your logger
registerLogger("my_app")

# Get the logger instance
logger = getLogger()

# Use it!
logger.info("Hello, world!")
logger.detail("Extra verbosity above INFO")
logger.minimal("Lower verbosity than INFO")
logger.trace("Trace information")
```

## Requirements

- **Python 3.10+**

No other dependencies required — this library uses only Python's standard library.

## Installation

Install via **poetry** or **pip**:

```bash
# Using poetry
poetry add apathetic-logger

# Using pip
pip install apathetic-logger
```

For alternative installation methods, see the [Installation Guide]({{ '/installation' | relative_url }}).

## Documentation

- **[Installation Guide]({{ '/installation' | relative_url }})** — How to install and set up
- **[Quick Start]({{ '/quickstart' | relative_url }})** — Get up and running in minutes
- **[API Reference]({{ '/api' | relative_url }})** — Complete API documentation
- **[Examples]({{ '/examples' | relative_url }})** — Advanced usage examples
- **[Custom Logger Guide]({{ '/custom-logger' | relative_url }})** — Creating application-specific loggers
- **[Contributing]({{ '/contributing' | relative_url }})** — How to contribute

## License

[MIT-a-NOAI License](https://github.com/apathetic-tools/python-logs/blob/main/LICENSE)

You're free to use, copy, and modify the library under the standard MIT terms.  
The additional rider simply requests that this project not be used to train or fine-tune AI/ML systems until the author deems fair compensation frameworks exist.  
Normal use, packaging, and redistribution for human developers are unaffected.

## Resources

- 📘 [Roadmap](https://github.com/apathetic-tools/python-logs/blob/main/ROADMAP.md)
- 📝 [Release Notes](https://github.com/apathetic-tools/python-logs/releases)
- 🐛 [Issue Tracker](https://github.com/apathetic-tools/python-logs/issues)
- 💬 [Discord](https://discord.gg/PW6GahZ7)

