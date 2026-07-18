#!/usr/bin/env bash
set -euo pipefail

# Validate the Claude Code plugin manifest.
# Prefer the official `claude plugin validate` when the CLI is on PATH;
# otherwise fall back to a JSON well-formedness check of the manifests.
cd "$(dirname "$0")/.."

if command -v claude >/dev/null 2>&1; then
    echo "Validating plugin via 'claude plugin validate .'..."
    claude plugin validate .
else
    echo "'claude' not on PATH — falling back to JSON load of plugin manifests..."
    python3 -c "import json, sys; [json.load(open(p)) for p in sys.argv[1:]]; print('plugin manifests are valid JSON')" \
        .claude-plugin/plugin.json \
        .claude-plugin/marketplace.json
fi
