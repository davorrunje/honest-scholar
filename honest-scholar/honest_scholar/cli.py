"""The ``honest-scholar`` command-line interface.

A Typer command tree mirroring the plugin's skill verbs. ``doctor`` is
implemented; the domain sub-commands are typed stubs pending their tracking
issues (see ADR-0024 and ``docs/design/proposals/tooling-package.md``).
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess  # nosec B404 - used only to read `--version` of trusted tools
import sys
from pathlib import Path
from typing import Annotated

import typer

from honest_scholar import __version__
from honest_scholar.defend import record as record_mod

app = typer.Typer(
    name="honest-scholar",
    help="Supporting tooling for the honest-scholar research-workflow plugin.",
    no_args_is_help=True,
    add_completion=False,
)


def _not_implemented(issue: int) -> None:
    """Emit the standard not-yet-implemented notice and exit.

    :param issue: The tracking issue number in the ``honest-scholar`` repo.
    :raises typer.Exit: Always, with code 2.
    """
    typer.echo(f"not yet implemented — see honest-scholar#{issue}")
    raise typer.Exit(code=2)


def _version_callback(value: bool) -> None:
    """Print the package version and exit when ``--version`` is given.

    :param value: Whether the ``--version`` flag was supplied.
    :raises typer.Exit: With code 0 after printing, when `value` is true.
    """
    if value:
        typer.echo(__version__)
        raise typer.Exit(code=0)


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=_version_callback,
            is_eager=True,
            help="Show the honest-scholar version and exit.",
        ),
    ] = False,
) -> None:
    """honest-scholar — research-workflow tooling CLI."""


def _tool_report(name: str) -> str:
    """Report the presence and version of an external tool on ``PATH``.

    Absence is reported, not treated as an error.

    :param name: Executable name to look up via :func:`shutil.which`.
    :returns: A human-readable one-line status string.
    """
    path = shutil.which(name)
    if path is None:
        return f"{name}: not found"
    try:
        proc = subprocess.run(  # nosec B603 - `path` resolved from PATH; fixed args
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - defensive
        return f"{name}: found ({path}), version unknown"
    output = (proc.stdout or proc.stderr).strip().splitlines()
    detail = output[0] if output else "version unknown"
    return f"{name}: {detail} ({path})"


@app.command()
def doctor() -> None:
    """Report the local environment: Python, ``uv`` and ``rclone``.

    Prints a short diagnostic report. Missing optional tools (``uv``,
    ``rclone``) are reported, not treated as failures. Always exits 0.
    """
    typer.echo("honest-scholar doctor")
    typer.echo(f"  honest-scholar: {__version__}")
    typer.echo(f"  python: {platform.python_version()} ({platform.platform()})")
    typer.echo(f"  {_tool_report('uv')}")
    typer.echo(f"  {_tool_report('rclone')}")
    raise typer.Exit(code=0)


# --- literature (honest-scholar#1) ------------------------------------------------
literature = typer.Typer(
    help="Citation-graph and metadata tools.", no_args_is_help=True
)
app.add_typer(literature, name="literature")


@literature.command()
def resolve(identifier: str) -> None:
    """Resolve an identifier (DOI, arXiv id, title) to a canonical work.

    :param identifier: The identifier to resolve.
    """
    _not_implemented(1)


@literature.command()
def cites(identifier: str) -> None:
    """List works that cite the given work.

    :param identifier: The work identifier.
    """
    _not_implemented(1)


@literature.command()
def refs(identifier: str) -> None:
    """List the references of the given work.

    :param identifier: The work identifier.
    """
    _not_implemented(1)


@literature.command()
def enrich(identifier: str) -> None:
    """Enrich a work's metadata from external sources.

    :param identifier: The work identifier.
    """
    _not_implemented(1)


@literature.command()
def neighbors(identifier: str) -> None:
    """List citation-graph neighbors of the given work.

    :param identifier: The work identifier.
    """
    _not_implemented(1)


# --- dataset (honest-scholar#2 manifest / #3 retrieval) ---------------------------
dataset = typer.Typer(
    help="Dataset manifest, retrieval and mirroring.", no_args_is_help=True
)
app.add_typer(dataset, name="dataset")


@dataset.command()
def validate(
    manifest: Annotated[
        str, typer.Argument(help="Path to the manifest to validate.")
    ] = "datasets.yml",
) -> None:
    """Validate a ``datasets.yml`` manifest (the register/audit gate).

    :param manifest: Path to the manifest to validate.
    """
    _not_implemented(2)


@dataset.command()
def ingest(croissant: str) -> None:
    """Ingest a published Croissant JSON-LD file to bootstrap a manifest entry.

    :param croissant: Path to the Croissant JSON-LD file.
    """
    _not_implemented(2)


@dataset.command()
def emit(identifier: str) -> None:
    """Emit a Croissant JSON-LD file for a manifest entry.

    :param identifier: The dataset id to emit (or ``--all`` in a later revision).
    """
    _not_implemented(2)


@dataset.command()
def fetch(identifier: str) -> None:
    """Fetch a registered dataset through the resolution chain (pooch/rclone).

    :param identifier: The dataset id to fetch.
    """
    _not_implemented(3)


@dataset.command()
def verify(identifier: str) -> None:
    """Verify on-disk bytes against the manifest SHA-256 (offline).

    :param identifier: The dataset id to verify.
    """
    _not_implemented(3)


@dataset.command()
def mirror(identifier: str) -> None:
    """Populate/refresh the private rclone mirror for a dataset.

    :param identifier: The dataset id to mirror.
    """
    _not_implemented(3)


@dataset.command()
def audit(
    identifier: Annotated[
        str, typer.Argument(help="Optional dataset id; whole manifest if omitted.")
    ] = "",
) -> None:
    """Audit fixity, mirror presence and manifest completeness.

    :param identifier: Optional dataset id; audits the whole manifest if omitted.
    """
    _not_implemented(3)


# --- defend (honest-scholar#4) ----------------------------------------------------
defend = typer.Typer(help="Defensibility record helpers.", no_args_is_help=True)
app.add_typer(defend, name="defend")


def _parse_acks(acks: str) -> list[dict[str, str]]:
    """Parse ``"gap::by||gap2::by2"`` into per-gap acknowledgement dicts."""
    result: list[dict[str, str]] = []
    for item in filter(None, (a.strip() for a in acks.split("||"))):
        gap, _, by = item.partition("::")
        result.append({"gap": gap.strip(), "by": by.strip()})
    return result


@defend.command()
def record(
    artifact: Annotated[
        str, typer.Option("--artifact", help="Target markdown artifact.")
    ],
    target: Annotated[
        str, typer.Option("--target", help="claim | cited-work | methodology.")
    ],
    gaps: Annotated[
        str, typer.Option("--gaps", help="Observed gap facts, '||'-separated.")
    ] = "",
    signed_off_by: Annotated[str, typer.Option("--signed-off-by")] = "",
    override: Annotated[bool, typer.Option("--override")] = False,
    acks: Annotated[
        str, typer.Option("--acks", help="Per-gap sign-offs, 'gap::name||…'.")
    ] = "",
    transcript: Annotated[
        str, typer.Option("--transcript", help="Transcript file, or '-' for stdin.")
    ] = "",
    log_dir: Annotated[str, typer.Option("--log-dir")] = str(
        record_mod.DEFAULT_LOG_DIR
    ),
) -> None:
    """Record a ``defend`` examination: patch understanding + append the log.

    Writes ``status.understanding`` into the artifact frontmatter and appends the
    outcome to the accountability log. Records observed facts only — never a
    verdict, score, or answer key.

    :param artifact: The examined markdown artifact.
    :param target: ``claim`` / ``cited-work`` / ``methodology``.
    :param gaps: Observed gap facts, ``||``-separated (empty means no gaps).
    :param signed_off_by: Named human; required when gaps are waved through.
    :param override: A blanket logged override of the surfaced gaps.
    :param acks: Per-gap acknowledgements, ``gap::name``, ``||``-separated.
    :param transcript: Transcript file path, or ``-`` for stdin.
    :param log_dir: Directory for the accountability log.
    :raises typer.Exit: Code 1 on a guard violation or malformed artifact.
    """
    gap_list = [g.strip() for g in gaps.split("||") if g.strip()]
    transcript_text: str | None = None
    if transcript == "-":
        transcript_text = sys.stdin.read()
    elif transcript:
        transcript_text = Path(transcript).read_text(encoding="utf-8")
    try:
        result = record_mod.record(
            artifact,
            target,
            gap_list,
            signed_off_by=signed_off_by or None,
            override=override,
            acknowledgements=_parse_acks(acks),
            transcript=transcript_text,
            log_dir=log_dir,
        )
    except (record_mod.RecordError, OSError) as exc:
        typer.echo(f"defend record failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(
        json.dumps(
            {
                "outcome": result.outcome,
                "artifact": str(result.artifact),
                "log_entry": str(result.log_entry),
                "transcript": str(result.transcript) if result.transcript else None,
            },
            indent=2,
        )
    )
    raise typer.Exit(code=0)


# --- backlog (honest-scholar#5) ---------------------------------------------------
backlog = typer.Typer(help="Exploration backlog management.", no_args_is_help=True)
app.add_typer(backlog, name="backlog")


@backlog.command()
def park(item: str) -> None:
    """Park a raw one-line idea as a backlog row before it is lost.

    :param item: The one-line idea (its origin/provenance is required).
    """
    _not_implemented(5)


@backlog.command()
def add(item: str) -> None:
    """Add an item to the exploration backlog.

    :param item: The backlog item description.
    """
    _not_implemented(5)


@backlog.command(name="list")
def list_() -> None:
    """List the current exploration backlog."""
    _not_implemented(5)


@backlog.command()
def rank() -> None:
    """Rank the exploration backlog by priority."""
    _not_implemented(5)


@backlog.command()
def promote(item: str) -> None:
    """Promote a backlog item to an active investigation.

    :param item: The backlog item identifier.
    """
    _not_implemented(5)


@backlog.command()
def drop(item: str) -> None:
    """Drop an item from the exploration backlog.

    :param item: The backlog item identifier.
    """
    _not_implemented(5)


if __name__ == "__main__":  # pragma: no cover
    app()
