"""Defensibility record helper (scholar#4)."""

from __future__ import annotations

from typing import Any


def record(claim: str, evidence: list[str]) -> dict[str, Any]:
    """Record a defensibility entry for a claim or decision.

    :param claim: The claim or decision being recorded.
    :param evidence: Supporting evidence references for the claim.
    :returns: The recorded defensibility entry.
    :raises NotImplementedError: Always — pending implementation (scholar#4).
    """
    raise NotImplementedError("defend record helper — see scholar#4")
