"""JSON exporter for traces."""

from __future__ import annotations

import json
from pathlib import Path

from django_llm_profiler.types import RequestTrace


def export_trace_json(trace: RequestTrace, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(trace.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return output_path
