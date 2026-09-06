"""
Read-only process observation for forensic context.

Lists currently running processes and basic resource metadata. This
module only *reads* process table information via psutil; it never
starts, stops, suspends, injects into, or otherwise controls a process.
"""

from __future__ import annotations

from datetime import datetime, timezone

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None

MAX_PROCESSES_RETURNED = 60


def list_processes() -> dict:
    if psutil is None:
        raise RuntimeError("psutil is required for process observation but is not installed")

    collected = []
    total_seen = 0
    for proc in psutil.process_iter(
        ["pid", "name", "username", "status", "memory_percent", "cpu_percent", "create_time"]
    ):
        total_seen += 1
        try:
            data = proc.info
            collected.append(
                {
                    "pid": data.get("pid"),
                    "name": data.get("name") or "unknown",
                    "username": data.get("username") or "n/a",
                    "status": data.get("status") or "unknown",
                    "memory_percent": round(data.get("memory_percent") or 0.0, 3),
                    "cpu_percent": round(data.get("cpu_percent") or 0.0, 2),
                    "created": (
                        datetime.fromtimestamp(data["create_time"], tz=timezone.utc).isoformat()
                        if data.get("create_time")
                        else None
                    ),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process exited mid-scan or is not observable; skip silently,
            # this module never attempts to gain elevated access.
            continue

    collected.sort(key=lambda p: p["memory_percent"], reverse=True)
    truncated = len(collected) > MAX_PROCESSES_RETURNED
    top = collected[:MAX_PROCESSES_RETURNED]

    return {
        "action": "processes",
        "process_count": total_seen,
        "returned_count": len(top),
        "truncated": truncated,
        "processes": top,
        "collected_at": datetime.now(tz=timezone.utc).isoformat(),
        "status": "success",
        "message": f"{total_seen} processes observed (showing top {len(top)} by memory use)",
    }
