"""Core structured profiler types."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


JSONValue = str | int | float | bool | None | dict[str, Any] | list[Any]


@dataclass(slots=True)
class StackFrame:
    file: str
    line: int
    function: str

    def to_dict(self) -> dict[str, JSONValue]:
        return asdict(self)


@dataclass(slots=True)
class QueryEvent:
    sql: str
    normalized_sql: str
    fingerprint: str
    duration_ms: float
    timestamp: datetime
    callsite_file: str | None = None
    callsite_line: int | None = None
    callsite_function: str | None = None
    stack: list[StackFrame] = field(default_factory=list)

    def to_dict(self) -> dict[str, JSONValue]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


@dataclass(slots=True)
class Issue:
    issue_type: str
    confidence: float
    message: str
    suggestion: str | None
    fingerprint: str | None
    repeat_count: int
    evidence: dict[str, JSONValue] = field(default_factory=dict)

    def to_dict(self) -> dict[str, JSONValue]:
        return asdict(self)


@dataclass(slots=True)
class TraceSummary:
    trace_id: str
    trace_type: str
    total_query_count: int
    total_db_time_ms: float
    duplicate_query_groups: list[dict[str, JSONValue]]
    normalized_duplicate_query_groups: list[dict[str, JSONValue]]
    issues: list[Issue]
    metadata: dict[str, JSONValue] = field(default_factory=dict)

    def to_dict(self) -> dict[str, JSONValue]:
        data = asdict(self)
        data["issues"] = [issue.to_dict() for issue in self.issues]
        return data


@dataclass(slots=True)
class RequestTrace:
    trace_id: str
    trace_type: str
    started_at: datetime
    ended_at: datetime | None = None
    metadata: dict[str, JSONValue] = field(default_factory=dict)
    queries: list[QueryEvent] = field(default_factory=list)
    summary: TraceSummary | None = None

    def to_dict(self) -> dict[str, JSONValue]:
        return {
            "trace_id": self.trace_id,
            "trace_type": self.trace_type,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "metadata": self.metadata,
            "queries": [query.to_dict() for query in self.queries],
            "summary": self.summary.to_dict() if self.summary else None,
        }
