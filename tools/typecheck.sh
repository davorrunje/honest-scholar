#!/usr/bin/env bash
set -euo pipefail

# Type-check the scholar-tools package with mypy (strict).
cd "$(dirname "$0")/../scholar-tools"

echo "Running mypy..."
uv run mypy
