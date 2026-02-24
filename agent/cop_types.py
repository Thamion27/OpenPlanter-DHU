# ═══════════════════════════════════════════════════════════════
# DigitalHermetica Studios — OpenPlanter-DHU
# Module: cop_types
# ═══════════════════════════════════════════════════════════════
# COP v1.0 — Cognitive Orchestration Protocol Type Definitions
# Python port of @cop/core TypeScript types
# Ledger Reference: DHU-KBASE-COP-001
# ═══════════════════════════════════════════════════════════════

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import time
import uuid


# ── ENUMERATIONS ──

class COPStage(str, Enum):
    RAP = 'RAP'  # Reception & Analysis
    SAP = 'SAP'  # Structuring & Alignment
    TSP = 'TSP'  # Transformation & Synthesis
    EVP = 'EVP'  # Evaluation & Validation
    OMP = 'OMP'  # Output & Manifestation


class GateVerdict(str, Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'


class PipelineStatus(str, Enum):
    IDLE = 'IDLE'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    ABORTED = 'ABORTED'


class ConfidenceLevel(str, Enum):
    HIGH = 'HIGH'      # >= 0.85
    MEDIUM = 'MEDIUM'  # 0.60 - 0.84
    LOW = 'LOW'        # < 0.60


class LogSeverity(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


# ── HELPER FUNCTIONS ──

def new_id() -> str:
    return str(uuid.uuid4())

def now_iso() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

def classify_confidence(score: float) -> ConfidenceLevel:
    if score >= 0.85:
        return ConfidenceLevel.HIGH
    elif score >= 0.60:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.LOW


# ── QUALITY GATE TYPES ──

@dataclass
class QualityCheck:
    name: str
    description: str
    passed: bool
    score: float
    timestamp: str = field(default_factory=now_iso)
    details: Optional[str] = None


@dataclass
class GatePolicy:
    stage: COPStage
    minimum_threshold: float
    max_retries: int = 2
    timeout_ms: int = 10000
    allow_manual_override: bool = False
    required_checks: list[str] = field(default_factory=list)


@dataclass
class QualityGate:
    stage: COPStage
    verdict: GateVerdict
    checks: list[QualityCheck]
    aggregate_score: float
    threshold: float
    evaluated_at: str = field(default_factory=now_iso)
    evaluator_id: str = 'cop-gate-engine'
    override_reason: Optional[str] = None

    @classmethod
    def evaluate(cls, stage: COPStage, checks: list[QualityCheck], policy: GatePolicy) -> 'QualityGate':
        if not checks:
            return cls(
                stage=stage,
                verdict=GateVerdict.FAIL,
                checks=[],
                aggregate_score=0.0,
                threshold=policy.minimum_threshold,
            )
        avg = sum(c.score for c in checks) / len(checks)
        verdict = GateVerdict.PASS if avg >= policy.minimum_threshold else GateVerdict.FAIL
        return cls(
            stage=stage,
            verdict=verdict,
            checks=checks,
            aggregate_score=round(avg, 4),
            threshold=policy.minimum_threshold,
        )


# ── CPL ENTRY ──

@dataclass
class CPLEntry:
    id: str = field(default_factory=new_id)
    correlation_id: str = ''
    stage: COPStage = COPStage.RAP
    severity: LogSeverity = LogSeverity.INFO
    event: str = ''
    message: str = ''
    data: Optional[dict[str, Any]] = None
    timestamp: str = field(default_factory=now_iso)
    duration_ms: Optional[float] = None


# ── PIPELINE RUN ──

@dataclass
class COPPipelineRun:
    id: str = field(default_factory=new_id)
    correlation_id: str = field(default_factory=new_id)
    status: PipelineStatus = PipelineStatus.IDLE
    current_stage: COPStage = COPStage.RAP
    gates: dict[str, QualityGate] = field(default_factory=dict)
    started_at: str = field(default_factory=now_iso)
    completed_at: Optional[str] = None
    total_duration_ms: Optional[float] = None
    retry_count: int = 0
    cpl_entries: list[CPLEntry] = field(default_factory=list)

    def log(self, stage: COPStage, severity: LogSeverity, event: str, message: str, data: Optional[dict] = None, duration_ms: Optional[float] = None):
        entry = CPLEntry(
            correlation_id=self.correlation_id,
            stage=stage,
            severity=severity,
            event=event,
            message=message,
            data=data,
            duration_ms=duration_ms,
        )
        self.cpl_entries.append(entry)
        return entry

    def set_gate(self, gate: QualityGate):
        self.gates[gate.stage.value] = gate

    def all_gates_passed(self) -> bool:
        return all(g.verdict == GateVerdict.PASS for g in self.gates.values())


# ── VERSION ──

COP_VERSION = '1.0.0'
COP_SPEC_ID = 'DHU-KBASE-COP-001'
