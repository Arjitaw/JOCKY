"""
Read-only directory listing and file-search analysis.

Both functions only read filesystem metadata (names, sizes, timestamps).
Neither opens file contents, executes anything, nor modifies the
filesystem in any way.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

from .indicators import evaluate_filename

MAX_LIST_ENTRIES = 500
MAX_SEARCH_MATCHES = 200
MAX_SEARCH_ENTRIES_SCANNED = 20000


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def list_files(path: str) -> dict:
    if not path:
        path = "."

    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    if not os.path.isdir(path):
        raise ValueError(f"Path is not a directory: {path}")

    entries = []
    with os.scandir(path) as it:
        for entry in it:
            try:
                stat = entry.stat(follow_symlinks=False)
                entries.append(
                    {
                        "name": entry.name,
                        "path": os.path.join(path, entry.name),
                        "type": "directory" if entry.is_dir(follow_symlinks=False) else "file",
                        "size_bytes": stat.st_size if entry.is_file(follow_symlinks=False) else 0,
                        "modified": _iso(stat.st_mtime),
                        "indicators": evaluate_filename(entry.name),
                    }
                )
            except OSError:
                continue

    entries.sort(key=lambda e: (e["type"] != "directory", e["name"].lower()))
    truncated = len(entries) > MAX_LIST_ENTRIES
    limited = entries[:MAX_LIST_ENTRIES]

    return {
        "action": "list",
        "target": os.path.abspath(path),
        "entry_count": len(entries),
        "returned_count": len(limited),
        "truncated": truncated,
        "entries": limited,
        "status": "success",
        "message": f"{len(entries)} entries found in {path}",
    }


def search_file(filename: str, search_path: str) -> dict:
    if not filename:
        raise ValueError("No filename provided to search for")
    if not search_path:
        search_path = "."
    if not os.path.exists(search_path):
        raise FileNotFoundError(f"Search directory not found: {search_path}")

    matches = []
    scanned = 0
    truncated_by_scan_limit = False
    truncated_by_match_limit = False
    needle = filename.lower()

    for root, _dirs, files in os.walk(search_path):
        for name in files:
            scanned += 1
            if scanned > MAX_SEARCH_ENTRIES_SCANNED:
                truncated_by_scan_limit = True
                break
            if needle in name.lower():
                full_path = os.path.join(root, name)
                try:
                    stat = os.stat(full_path)
                    matches.append(
                        {
                            "name": name,
                            "path": full_path,
                            "size_bytes": stat.st_size,
                            "modified": _iso(stat.st_mtime),
                            "indicators": evaluate_filename(name),
                        }
                    )
                except OSError:
                    continue
                if len(matches) >= MAX_SEARCH_MATCHES:
                    truncated_by_match_limit = True
                    break
        if truncated_by_scan_limit or truncated_by_match_limit:
            break

    return {
        "action": "search",
        "search_target": filename,
        "search_directory": os.path.abspath(search_path),
        "match_count": len(matches),
        "entries_scanned": scanned,
        "truncated": truncated_by_scan_limit or truncated_by_match_limit,
        "results": matches,
        "status": "success",
        "message": f"{len(matches)} match(es) for '{filename}' under {search_path}",
    }
