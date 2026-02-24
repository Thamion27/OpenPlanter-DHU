# ═══════════════════════════════════════════════════════════════
# DigitalHermetica Studios — OpenPlanter-DHU
# Module: cpl (Cognitive Process Ledger)
# ═══════════════════════════════════════════════════════════════
# COP v1.0 — Logs every agent action for auditability
# Ledger Reference: DHU-KBASE-COP-001
# ═══════════════════════════════════════════════════════════════

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from typing import Any, Optional

from .cop_types import (
    COPStage, LogSeverity, CPLEntry, QualityGate,
    GateVerdict, new_id, now_iso,
)


class CPLLogger:
    """Cognitive Process Ledger — records all COP pipeline events."""

    def __init__(self, workspace: str, session_id: Optional[str] = None):
        self.session_id = session_id or new_id()
        self.log_dir = Path(workspace) / '.cop' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f'session_{self.session_id}.jsonl'
        self.entries: list[CPLEntry] = []
        self._start_time = time.time()

        self.info(COPStage.RAP, 'session_start', f'CPL session started: {self.session_id}')

    def _write(self, entry: CPLEntry) -> None:
        self.entries.append(entry)
        record = {
            'id': entry.id,
            'correlation_id': entry.correlation_id,
            'stage': entry.stage.value,
            'severity': entry.severity.value,
            'event': entry.event,
            'message': entry.message,
            'data': entry.data,
            'timestamp': entry.timestamp,
            'duration_ms': entry.duration_ms,
        }
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record) + '\n')

    def log(self, stage: COPStage, severity: LogSeverity, event: str,
            message: str, data: Optional[dict[str, Any]] = None,
            duration_ms: Optional[float] = None) -> CPLEntry:
        entry = CPLEntry(
            correlation_id=self.session_id,
            stage=stage,
            severity=severity,
            event=event,
            message=message,
            data=data,
            duration_ms=duration_ms,
        )
        self._write(entry)
        return entry

    def debug(self, stage: COPStage, event: str, message: str, **kw) -> CPLEntry:
        return self.log(stage, LogSeverity.DEBUG, event, message, **kw)

    def info(self, stage: COPStage, event: str, message: str, **kw) -> CPLEntry:
        return self.log(stage, LogSeverity.INFO, event, message, **kw)

    def warn(self, stage: COPStage, event: str, message: str, **kw) -> CPLEntry:
        return self.log(stage, LogSeverity.WARN, event, message, **kw)

    def error(self, stage: COPStage, event: str, message: str, **kw) -> CPLEntry:
        return self.log(stage, LogSeverity.ERROR, event, message, **kw)

    def fatal(self, stage: COPStage, event: str, message: str, **kw) -> CPLEntry:
        return self.log(stage, LogSeverity.FATAL, event, message, **kw)

    def log_gate(self, gate: QualityGate) -> CPLEntry:
        return self.info(
            gate.stage,
            'gate_evaluated',
            f'Gate {gate.stage.value}: {gate.verdict.value} '
            f'(score={gate.aggregate_score:.3f}, threshold={gate.threshold:.3f})',
            data={
                'verdict': gate.verdict.value,
                'score': gate.aggregate_score,
                'threshold': gate.threshold,
                'checks': len(gate.checks),
                'passed_checks': sum(1 for c in gate.checks if c.passed),
            },
        )

    def log_tool(self, tool_name: str, args: dict, result: str,
                 duration_ms: float, success: bool = True) -> CPLEntry:
        return self.log(
            COPStage.TSP,
            LogSeverity.INFO if success else LogSeverity.ERROR,
            'tool_invoke',
            f'Tool: {tool_name} ({"OK" if success else "FAIL"}, {duration_ms:.0f}ms)',
            data={
                'tool': tool_name,
                'args_keys': list(args.keys()),
                'result_length': len(result),
                'success': success,
            },
            duration_ms=duration_ms,
        )

    def summary(self) -> dict[str, Any]:
        elapsed = (time.time() - self._start_time) * 1000
        stage_counts: dict[str, int] = {}
        error_count = 0
        for e in self.entries:
            stage_counts[e.stage.value] = stage_counts.get(e.stage.value, 0) + 1
            if e.severity in (LogSeverity.ERROR, LogSeverity.FATAL):
                error_count += 1
        return {
            'session_id': self.session_id,
            'total_entries': len(self.entries),
            'stage_breakdown': stage_counts,
            'errors': error_count,
            'total_duration_ms': round(elapsed, 2),
            'log_file': str(self.log_file),
        }

    def close(self) -> dict[str, Any]:
        s = self.summary()
        self.info(COPStage.OMP, 'session_end',
                  f'CPL session closed: {len(self.entries)} entries, {s["errors"]} errors',
                  data=s)
        return s
