from android_dojo_toolkit.safety import (
    OperationPlan,
    RiskLevel,
    SafetyBlocked,
    evaluate,
    require_allowed,
)


def test_verified_reversible_operation_is_allowed() -> None:
    plan = OperationPlan(
        name="inspect",
        target="device",
        risk=RiskLevel.LOW,
        reversible=True,
        verified=True,
    )

    decision = evaluate(plan)

    assert decision.allowed
    assert decision.reasons == ()


def test_ambiguity_blocks_operation() -> None:
    plan = OperationPlan(
        name="flash",
        target="device",
        risk=RiskLevel.HIGH,
        reversible=False,
        recovery_plan="restore stock image",
        verified=True,
        ambiguity=("device variant is unknown",),
    )

    decision = evaluate(plan)

    assert not decision.allowed
    assert "ambiguous: device variant is unknown" in decision.reasons


def test_required_backup_must_be_verified() -> None:
    plan = OperationPlan(
        name="erase",
        target="userdata",
        risk=RiskLevel.CRITICAL,
        reversible=False,
        recovery_plan="restore from verified backup",
        backup_required=True,
        verified=True,
    )

    decision = evaluate(plan)

    assert not decision.allowed
    assert decision.requires_backup
    assert "required backup has not been verified" in decision.reasons


def test_unverified_operation_is_blocked() -> None:
    plan = OperationPlan(
        name="flash",
        target="boot",
        risk=RiskLevel.HIGH,
        reversible=False,
        recovery_plan="restore stock boot image",
    )

    decision = evaluate(plan)

    assert not decision.allowed
    assert decision.requires_verification


def test_non_reversible_operation_requires_recovery_plan() -> None:
    plan = OperationPlan(
        name="erase",
        target="partition",
        risk=RiskLevel.CRITICAL,
        reversible=False,
        verified=True,
    )

    decision = evaluate(plan)

    assert not decision.allowed
    assert "non-reversible operation has no recovery plan" in decision.reasons


def test_require_allowed_raises_without_mutating_anything() -> None:
    plan = OperationPlan(
        name="flash",
        target="boot",
        risk=RiskLevel.HIGH,
    )

    try:
        require_allowed(plan)
    except SafetyBlocked as exc:
        assert "flash:" in str(exc)
    else:
        raise AssertionError("SafetyBlocked was not raised")
