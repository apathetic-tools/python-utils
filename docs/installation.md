---
layout: base
title: Installation
permalink: /installation/
---

# Installation Guide

Apathetic Python Utils can be installed using several methods. Choose the one that best fits your project's needs.

## Primary Method: PyPI (Recommended)

The recommended way to install Apathetic Python Utils is via PyPI. We prefer `poetry` over `pip` for its `pyproject.toml` support, automatic venv management, and tool configuration without dotfiles.

### Using Poetry (Preferred)

```bash
poetry add apathetic-logger
```

### Using pip

```bash
pip install apathetic-logger
```

This installation method provides:
- Easy dependency management
- Version pinning
- Integration with your existing Python project structure

## Alternative: Single-File Distribution

For projects that prefer a single-file dependency, we also distribute a standalone `apathetic_utils.py` file that you can download directly from [releases](https://github.com/apathetic-tools/python-logs/releases).

### Download and Use

1. Download `apathetic_utils.py` from the [latest release](https://github.com/apathetic-tools/python-logs/releases)
2. Place it in your project directory
3. Import it directly:

```python
import apathetic_utils
```

This method is useful for:
- Projects that want to integrate dependencies directly into their codebase  
  *(avoiding package managers and external dependencies)*
- Embedded systems or restricted environments  
  *(including offline/air-gapped deployments)*

## Requirements

- **Python 3.10+**

Apathetic Python Utils has **zero runtime dependencies** — it uses only Python's standard library. This makes it perfect for CLI tools and applications where dependency bloat is a concern.

## Verification

After installation, verify that it works:

```python
from apathetic_utils import getLogger, registerLogger

registerLogger("test")
logger = getLogger()
logger.minimal("Installation successful!")
```

If you see the info message, installation was successful!

## Next Steps

- Read the [Quick Start Guide]({{ '/quickstart' | relative_url }}) to get up and running
- Check out the [API Reference]({{ '/api' | relative_url }}) for detailed documentation
- See [Examples]({{ '/examples' | relative_url }}) for advanced usage patterns

