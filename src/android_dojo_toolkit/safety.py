"""Small, dependency-free safety core for Android Dojo Toolkit.

This module deliberately knows nothing about Android transports, vendors, or
specific flashing tools. It defines the safety vocabulary that those organs
must use before an operation can execute.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Mapping


class RiskLevel(str, Enum):
    """Declared consequence level for an operation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SafetyError(RuntimeError):
    """Base class for safety-gate failures."""


class SafetyBlocked(SafetyError):
    """Raised when an operation must not proceed."""


@dataclass(frozen=True)
class OperationPlan:
    """The evidence and requirements for one proposed operation."""

    name: str
    target: str
    risk: RiskLevel
    prerequisites: tuple[str, ...] = ()
    evidence: Mapping[str, str] = field(default_factory=dict)
    compatibility: tuple[str, ...] = ()
    affected_artifacts: tuple[str, ...] = ()
    reversible: bool = False
    backup_required: bool = False
    backup_verified: bool = False
    dry_run: bool = True
    verified: bool = False
    recovery_plan: str | None = None
    ambiguity: tuple[str, ...] = ()


@dataclass(frozen=True)
class SafetyDecision:
    """The result of evaluating an operation plan."""

    allowed: bool
    reasons: tuple[str, ...] = ()
    requires_backup: bool = False
    requires_verification: bool = False


def evaluate(
    plan: OperationPlan,
    *,
    checks: tuple[Callable[[OperationPlan], str | None], ...] = (),
) -> SafetyDecision:
    """Evaluate a plan without performing any device operation.

    The default rules are intentionally conservative:
    - unresolved ambiguity blocks execution;
    - missing required backups block execution;
    - unverified plans cannot execute;
    - destructive operations require a recovery path;
    - caller-supplied checks may add domain-specific requirements.
    """

    reasons: list[str] = []

    if plan.ambiguity:
        reasons.extend(f"ambiguous: {item}" for item in plan.ambiguity)

    if plan.backup_required and not plan.backup_verified:
        reasons.append("required backup has not been verified")

    if not plan.verified:
        reasons.append("operation has not been verified")

    if not plan.reversible and not plan.recovery_plan:
        reasons.append("non-reversible operation has no recovery plan")

    for check in checks:
        reason = check(plan)
        if reason:
            reasons.append(reason)

    return SafetyDecision(
        allowed=not reasons,
        reasons=tuple(reasons),
        requires_backup=plan.backup_required and not plan.backup_verified,
        requires_verification=not plan.verified,
    )


def require_allowed(
    plan: OperationPlan,
    *,
    checks: tuple[Callable[[OperationPlan], str | None], ...] = (),
) -> SafetyDecision:
    """Evaluate a plan and raise SafetyBlocked if execution is not allowed."""

    decision = evaluate(plan, checks=checks)
    if not decision.allowed:
        detail = "; ".join(decision.reasons)
        raise SafetyBlocked(f"{plan.name}: {detail}")
    return decision
