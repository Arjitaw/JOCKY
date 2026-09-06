"""
Structured metadata mirroring compiler/Language.md.

Kept separate from the grammar/parser so the frontend can render an
accurate, always-in-sync command reference via GET /commands instead of
hardcoding syntax that could drift from compiler/grammar.lark.
"""

LANGUAGE_REFERENCE = [
    {
        "name": "HASH",
        "syntax": "HASH FILE <path>",
        "example": "HASH FILE evidence.bin",
        "description": "Compute a cryptographic hash of a file for integrity verification.",
        "category": "integrity",
    },
    {
        "name": "ENCRYPT",
        "syntax": "ENCRYPT FILE <path>",
        "example": "ENCRYPT FILE evidence.bin",
        "description": "Encrypt a file in place to protect evidence at rest.",
        "category": "evidence-handling",
    },
    {
        "name": "SYSTEM INFO",
        "syntax": "SYSTEM INFO",
        "example": "SYSTEM INFO",
        "description": "Collect read-only host system information (OS, CPU, memory, runtime).",
        "category": "system",
    },
    {
        "name": "LIST FILES",
        "syntax": "LIST FILES <path>",
        "example": "LIST FILES ./evidence",
        "description": "List files and directories at a given path with metadata.",
        "category": "filesystem",
    },
    {
        "name": "PROCESSES",
        "syntax": "PROCESSES",
        "example": "PROCESSES",
        "description": "Observe currently running processes (read-only).",
        "category": "system",
    },
    {
        "name": "SEARCH FILE",
        "syntax": "SEARCH FILE <name> IN <path>",
        "example": "SEARCH FILE malware.exe IN ./samples",
        "description": "Search a directory tree for files matching a name.",
        "category": "filesystem",
    },
]
