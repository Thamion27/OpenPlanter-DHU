# ═══════════════════════════════════════════════════════════════
# DigitalHermetica Studios — OpenPlanter-DHU
# Module: cop_config
# ═══════════════════════════════════════════════════════════════
# COP v1.0 — Gate policies and configuration
# Ledger Reference: DHU-KBASE-COP-001
# ═══════════════════════════════════════════════════════════════

from .cop_types import COPStage, GatePolicy

# Default gate policies for each COP stage
DEFAULT_GATE_POLICIES: dict[str, GatePolicy] = {
    COPStage.RAP.value: GatePolicy(
        stage=COPStage.RAP,
        minimum_threshold=0.70,
        max_retries=2,
        timeout_ms=5000,
        required_checks=['intent_classified'],
    ),
    COPStage.SAP.value: GatePolicy(
        stage=COPStage.SAP,
        minimum_threshold=0.60,
        max_retries=1,
        timeout_ms=10000,
        required_checks=['plan_valid'],
    ),
    COPStage.TSP.value: GatePolicy(
        stage=COPStage.TSP,
        minimum_threshold=0.80,
        max_retries=3,
        timeout_ms=30000,
        required_checks=['tool_success'],
    ),
    COPStage.EVP.value: GatePolicy(
        stage=COPStage.EVP,
        minimum_threshold=0.75,
        max_retries=2,
        timeout_ms=15000,
        required_checks=['quality_check'],
    ),
    COPStage.OMP.value: GatePolicy(
        stage=COPStage.OMP,
        minimum_threshold=0.90,
        max_retries=1,
        timeout_ms=5000,
        required_checks=['output_formatted'],
    ),
}


def get_policy(stage: COPStage) -> GatePolicy:
    return DEFAULT_GATE_POLICIES[stage.value]


def get_all_policies() -> dict[str, GatePolicy]:
    return DEFAULT_GATE_POLICIES.copy()


# COP feature flags
COP_CONFIG = {
    'enabled': False,
    'log_level': 'INFO',
    'log_dir': '.cop/logs',
    'gates_enabled': True,
    'cpl_enabled': True,
    'strict_mode': False,
}
