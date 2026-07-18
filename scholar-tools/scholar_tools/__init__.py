"""scholar-tools — supporting CLI/tooling for the scholar research plugin.

The authoritative interface is the ``scholar`` Typer CLI
(:mod:`scholar_tools.cli`); an optional MCP wrapper over the same modules may
follow later (see ADR-0024).
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("scholar-tools")
except PackageNotFoundError:  # pragma: no cover - not installed (e.g. source tree)
    __version__ = "0.0.0"

__all__ = ["__version__"]
