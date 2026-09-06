"""
Local hash ledger.

Every time JOCKY hashes a file, it records {algorithm, hash, size, timestamp}
for that absolute path in a small local JSON file. The next time the same
path is hashed, JOCKY can tell the analyst whether the file has changed
since the last time JOCKY looked at it -- entirely from its own prior
observations, with no external "known-good" reference required.

This is local, evidentiary bookkeeping only: it reads and appends to one
JSON file under jocky/data/ and never touches the files being analyzed.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone

_LEDGER_LOCK = threading.Lock()
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
_LEDGER_PATH = os.path.join(_DATA_DIR, "hash_ledger.json")

MAX_HISTORY_PER_FILE = 20


def _load_ledger() -> dict:
    if not os.path.exists(_LEDGER_PATH):
        return {}
    try:
        with open(_LEDGER_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        # A corrupted or unreadable ledger should never break hashing itself;
        # treat it as empty rather than raising.
        return {}


def _save_ledger(ledger: dict) -> None:
    os.makedirs(_DATA_DIR, exist_ok=True)
    tmp_path = _LEDGER_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        json.dump(ledger, handle, indent=2)
    os.replace(tmp_path, _LEDGER_PATH)


def get_last_hash(absolute_path: str) -> dict | None:
    """Return the most recent recorded hash entry for this path, or None."""
    with _LEDGER_LOCK:
        ledger = _load_ledger()
    history = ledger.get(absolute_path) or []
    return history[-1] if history else None


def record_hash(absolute_path: str, algorithm: str, hash_value: str, size_bytes: int) -> None:
    """Append a new hash observation for this path to the ledger."""
    entry = {
        "algorithm": algorithm.upper(),
        "hash": hash_value,
        "size_bytes": size_bytes,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
    with _LEDGER_LOCK:
        ledger = _load_ledger()
        history = ledger.get(absolute_path) or []
        history.append(entry)
        ledger[absolute_path] = history[-MAX_HISTORY_PER_FILE:]
        _save_ledger(ledger)


def compare_to_last(previous: dict | None, algorithm: str, hash_value: str) -> dict:
    """
    Build a human-readable comparison between a freshly computed hash and
    the previously recorded one (if any) for the same file.

    Returns:
        {
          "has_previous": bool,
          "status": "first_recorded" | "unchanged" | "altered" | "algorithm_mismatch",
          "message": str,
        }
    """
    if previous is None:
        return {
            "has_previous": False,
            "status": "first_recorded",
            "message": "No prior JOCKY hash is on record for this file; this is the first observation.",
        }

    if previous["algorithm"].upper() != algorithm.upper():
        return {
            "has_previous": True,
            "status": "algorithm_mismatch",
            "message": (
                f"A previous {previous['algorithm']} hash is on record from {previous['timestamp']}, "
                f"but this run used {algorithm.upper()}. Re-run with {previous['algorithm']} to compare directly."
            ),
        }

    if previous["hash"].lower() == hash_value.lower():
        return {
            "has_previous": True,
            "status": "unchanged",
            "message": f"Unchanged since it was last hashed by JOCKY at {previous['timestamp']}.",
        }

    return {
        "has_previous": True,
        "status": "altered",
        "message": (
            f"ALTERED since it was last hashed by JOCKY at {previous['timestamp']}: "
            f"the {algorithm.upper()} digest no longer matches."
        ),
    }
