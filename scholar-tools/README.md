# scholar-tools

Supporting CLI/tooling for the [scholar](https://github.com/davorrunje/scholar)
research-workflow plugin. Distributed as `scholar-tools`; exposes the `scholar`
CLI.

Per [ADR-0024](../decisions/0024-tooling-package-and-bootstrap.md), the plugin
stays pure-markdown and this package is installed **isolated** (never into a
consumer's ML environment) on demand via the
[`ensure-tooling`](../resources/ensure-tooling.md) procedure. The CLI is the
authoritative interface; a thin MCP wrapper over the same modules may follow.

## Install (development)

```bash
cd scholar-tools
uv sync
uv run scholar --version
uv run scholar doctor
```

Isolated install from the plugin repo (as `ensure-tooling` does):

```bash
uv tool install "git+https://github.com/davorrunje/scholar.git#subdirectory=scholar-tools"
```

## CLI

```
scholar --version
scholar doctor                                       # environment report (implemented)
scholar literature resolve | cites | refs | enrich | neighbors   # scholar#1
scholar dataset    register | fetch | verify | mirror | audit    # scholar#2 / #3
scholar defend     record                                        # scholar#4
scholar backlog    add | list | rank | promote | drop            # scholar#5
```

Only `doctor` and `--version` are implemented; the domain sub-commands are
typed stubs exiting with code 2 and a pointer to their tracking issue.

## Develop

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```
