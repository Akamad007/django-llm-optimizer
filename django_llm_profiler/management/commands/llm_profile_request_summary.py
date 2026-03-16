from __future__ import annotations

import json

from django.core.management.base import BaseCommand

from django_llm_profiler.conf import get_storage


class Command(BaseCommand):
    help = "Summarize stored django-llm-profiler traces."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--format", choices=["text", "json"], default="text")

    def handle(self, *args, **options):
        traces = get_storage().list_traces()
        payload = [
            {
                "trace_id": trace.trace_id,
                "trace_type": trace.trace_type,
                "started_at": trace.started_at.isoformat(),
                "query_count": len(trace.queries),
                "metadata": trace.metadata,
            }
            for trace in traces
        ]
        if options["format"] == "json":
            self.stdout.write(json.dumps(payload, indent=2, sort_keys=True))
            return
        if not payload:
            self.stdout.write("No traces available.")
            return
        for item in payload:
            self.stdout.write(
                f"{item['trace_type']} {item['trace_id']} queries={item['query_count']} metadata={item['metadata']}"
            )
