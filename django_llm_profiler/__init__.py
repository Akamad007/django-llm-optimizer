"""Machine-readable Django query profiling for LLMs, tests, and CI."""

from .api import analyze_queries, export_trace, get_last_trace, profile_block

__all__ = [
    "analyze_queries",
    "export_trace",
    "get_last_trace",
    "profile_block",
]

__version__ = "0.1.0"
