#!/usr/bin/env bash
set -euo pipefail

# Lint the scholar-tools package with ruff (check + format verification).
cd "$(dirname "$0")/../scholar-tools"

echo "Running ruff linter..."
uv run ruff check .

echo "Running ruff formatter (check only)..."
uv run ruff format --check .
