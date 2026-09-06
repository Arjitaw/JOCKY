"""
Cryptographic hashing for digital evidence integrity verification.

Read-only: opens the target file, streams it through a hash digest, and
reports metadata. Never modifies the file being analyzed.

Also runs a lightweight structural integrity pre-check (analysis/integrity.py)
and compares the freshly computed digest against JOCKY's own hash ledger
(analysis/ledger.py) so the analyst immediately knows both (a) whether the
file looks structurally intact, and (b) whether it has changed since JOCKY
last hashed it.
"""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone

from .indicators import evaluate_filename
from .integrity import check_basic_integrity
from .ledger import compare_to_last, get_last_hash, record_hash

SUPPORTED_ALGORITHMS = ("sha256", "sha1", "md5", "sha512")
CHUNK_SIZE = 65536


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def hash_file(path: str, algorithm: str = "sha256") -> dict:
    if not path:
        raise ValueError("No file path provided")

    algorithm = (algorithm or "sha256").lower()
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. Supported: {', '.join(SUPPORTED_ALGORITHMS)}"
        )

    if not os.path.exists(path):
        raise FileNotFoundError(f"Target not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Target is not a file: {path}")

    absolute_path = os.path.abspath(path)

    # Structural sanity check first -- corruption doesn't prevent hashing
    # (a corrupted file's hash is still valid evidence), so this never
    # blocks the digest below; it's reported alongside it.
    integrity_check = check_basic_integrity(path)

    digest = hashlib.new(algorithm)
    size_bytes = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
            size_bytes += len(chunk)

    hash_value = digest.hexdigest()

    # Compare against JOCKY's own prior record for this exact path BEFORE
    # writing the new one, then record the new observation for next time.
    previous_hash = get_last_hash(absolute_path)
    integrity_history = compare_to_last(previous_hash, algorithm, hash_value)
    record_hash(absolute_path, algorithm, hash_value, size_bytes)

    stat = os.stat(path)
    filename = os.path.basename(path)

    verification_state = {
        "first_recorded": "computed (first record)",
        "unchanged": "verified unchanged",
        "altered": "ALTERED since last hash",
        "algorithm_mismatch": "computed (algorithm differs from last record)",
    }[integrity_history["status"]]

    return {
        "action": "hash",
        "target": path,
        "filename": filename,
        "algorithm": algorithm.upper(),
        "hash": hash_value,
        "size_bytes": size_bytes,
        "modified": _iso(stat.st_mtime),
        "created": _iso(stat.st_ctime),
        "absolute_path": absolute_path,
        "verification_state": verification_state,
        "integrity_check": integrity_check,
        "previous_hash": previous_hash,
        "integrity_history": integrity_history,
        "indicators": evaluate_filename(filename),
        "status": "success",
        "message": f"{algorithm.upper()} digest computed for {filename}",
    }
