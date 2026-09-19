"""Operation model built on the Toolkit safety core."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .safety import OperationPlan, SafetyDecision, evaluate


@dataclass(frozen=True)
class Operation:
    """A named operation plus the plan used to decide whether it may run."""

    plan: OperationPlan
    checks: tuple[Callable[[OperationPlan], str | None], ...] = ()

    def assess(self) -> SafetyDecision:
        """Return a safety decision without changing the device."""
        return evaluate(self.plan, checks=self.checks)
