# JOCKY

**JOCKY** is a defensive digital forensics and security analysis platform. It gives an
analyst a small command language, a real backend engine, and a polished investigation
console for running read-only forensic operations against files, directories, and a
host system — then turns every result into a structured, timestamped report.

JOCKY performs **no offensive, evasive, or system-altering actions**. Every capability
in this repository is read-only observation or evidence-handling (hashing, encrypting
evidence at rest). See [PRD.md](./PRD.md) for the full scope statement and how the
original SIH problem statement's threat-modeling language maps (or doesn't) to what's
implemented here.

## What it does

- **HASH** a file (SHA-256 / SHA-1 / MD5 / SHA-512) for integrity verification —
  and for every hash, JOCKY automatically:
  - runs a **structural integrity pre-check** (catches empty files, corrupted
    ZIP/Office/JAR archives via CRC validation, truncated JPEG/PNG/PDF files)
  - looks up the **last time JOCKY hashed this exact file** (kept locally in
    `data/hash_ledger.json`) and reports whether the contents are unchanged
    or have been altered since then
- **ENCRYPT** a file at rest to protect evidence during a chain-of-custody hold
- **SYSTEM INFO** — read-only host facts: OS, architecture, CPU, memory, uptime
- **PROCESSES** — read-only observation of running processes
- **LIST FILES** — directory listings with size/type/modified metadata
- **SEARCH FILE** — recursive filename search under a directory

Every one of the above also gets a set of neutral, static filename indicators
(e.g. "notable extension", "possible double-extension spoofing") to help an analyst
triage what to look at next. These are string-based heuristics only — JOCKY never
executes, scans the contents of, or makes a verdict about a file.

## Architecture

```
React 19 / Vite (TanStack Start) dashboard
              │  fetch("/command", "/health", "/commands")
              ▼
        Flask API  (communication/server.py)
              │
        JOCKY compiler/parser  (compiler/*.py, Lark grammar)
              │
        dispatcher  (communication/dispatcher.py)
              │
        analysis modules  (analysis/*.py)
              │
        structured JSON report  (reports/report.py)
```

- **compiler/** — the JOCKY command language: `grammar.lark` (Lark grammar),
  `parser.py`, `Transformer.py`, and `Language_meta.py` (structured reference
  served at `GET /commands` so the frontend never hardcodes stale syntax).
- **communication/** — `server.py` (Flask app, CORS-enabled) and `dispatcher.py`
  (routes a parsed command to the right analysis module and reports errors safely).
- **analysis/** — the actual forensic work: `hashing.py`, `system.py`,
  `processes.py`, `files.py` (list + search), `indicators.py` (static,
  read-only triage heuristics), `integrity.py` (structural corruption
  pre-checks), and `ledger.py` (local hash history used to detect changes
  between runs).
- **crypto/** — evidence-at-rest encryption (`crypto.py`) plus the project's own
  SHA-256 reference implementation/source (`sha256/`) for the "SHA-256
  implementation" requirement.
- **reports/** — `report.py` wraps every dispatcher result into a structured
  report object (`report_id`, `timestamp`, `command`, `action`, `target`,
  `status`, `execution_time_ms`, `result`, `warnings`, `errors`).
- **dashboard/** — the React/Vite/TanStack Start frontend (see below).
- **agent/** — the C++ authorized analysis client component (existing).

## Project structure

```
jocky/
├── analysis/            # hashing, system, processes, files, indicators
├── communication/        # Flask server + dispatcher
├── compiler/              # JOCKY grammar, parser, transformer, language reference
├── crypto/                 # evidence encryption + SHA-256 source
├── reports/                 # structured report builder
├── tests/                    # backend unit tests
├── dashboard/                 # React/Vite/TanStack Start frontend
│   └── src/
│       ├── routes/               # 9 file-based routes (Overview, Command Center, ...)
│       ├── components/
│       │   ├── layout/                # app shell, sidebar, top bar, metric card
│       │   ├── forensics/            # command console + result renderers
│       │   ├── reports/             # A4 report document
│       │   └── ui/                 # shadcn/ui primitives
│       ├── lib/                      # types, store, formatting, nav
│       └── services/api.ts            # Flask API client
├── requirements.txt
└── PRD.md
```

## Running the backend

```bash
cd jocky
python3 -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python3 -m communication.server
```

The API listens on `http://localhost:5000` by default (`FLASK_RUN_PORT`/edit
`server.py` to change it). Health check: `GET /health`.

## Desktop App — Fully Bundled Windows Runtime

JOCKY has a production Windows packaging path that bundles:

- the React/Vite frontend as static production assets
- Electron + Chromium as the desktop runtime
- the Flask/Python forensic backend frozen with PyInstaller

The **target Windows PC does not need Python, Node.js, npm, Vite, or a terminal**.
Those tools are only required on the machine used to build the application.

### Build on Windows

From the project root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\desktop\build_windows.ps1
```

Or double-click:

```text
desktop\build_windows.bat
```

The build produces both an NSIS installer and a portable Windows executable in:

```text
desktop-app\release\
```

The packaged application starts the bundled Flask engine invisibly, waits for `/health`, and loads the production frontend directly from the application resources. It never starts `npm run dev`.

### Runtime architecture

```text
JOCKY.exe
  ├─ Electron / Chromium runtime
  ├─ dashboard/  (production static frontend)
  └─ backend/
      └─ JOCKY-backend.exe  (PyInstaller Python runtime + Flask + analysis engine)
```

The backend listens only on `127.0.0.1:5000` and is used by the local desktop UI.

### Troubleshooting

If the packaged application cannot start, the backend log is written to the current Windows user's JOCKY application-data directory as `jocky-backend.log`. The startup dialog shows the log path.

The old `desktop/launcher.py` remains only as a developer/legacy placeholder; it is **not** the production packaging path.

## Running the frontend

```bash
cd jocky/dashboard
npm install
npm run dev
```

By default the frontend talks to `http://localhost:5000`. To point it elsewhere,
create `dashboard/.env`:

```
VITE_API_BASE_URL=http://localhost:5000
```

Then `npm run build` for a production build, or `npm run dev` for local development.

> **Note on this delivery:** the sandbox this was built in could not run `npm run
> build` (a native binding for the bundler was missing for that container's OS —
> unrelated to the source changes). Every file was type-checked with `tsc --noEmit`
> and linted with `eslint` (both pass with zero errors), but please run a full
> `npm install && npm run build` locally before your first demo, in case your
> platform surfaces something the sandbox couldn't.

## Supported commands

| Command | Syntax | Example |
| --- | --- | --- |
| Hash | `HASH FILE <path>` | `HASH FILE evidence.bin` |
| Encrypt | `ENCRYPT FILE <path>` | `ENCRYPT FILE evidence.bin` |
| System Info | `SYSTEM INFO` | `SYSTEM INFO` |
| List Files | `LIST FILES <path>` | `LIST FILES ./evidence` |
| Processes | `PROCESSES` | `PROCESSES` |
| Search File | `SEARCH FILE <name> IN <path>` | `SEARCH FILE malware.exe IN ./samples` |

This table is also served live at `GET /commands` and rendered in the Command
Center so the UI never drifts from the grammar.

## API overview

| Endpoint | Method | Purpose |
| --- | --- | --- |
| `/health` | GET | Liveness check used by the frontend's status pill |
| `/commands` | GET | Structured command reference |
| `/command` | POST `{ "command": "HASH FILE x.bin" }` | Parses, executes, and returns `{ status, command, result, report, error }` |

Every `/command` call — success or failure — returns a full `report` object, so
the frontend's Reports archive and Investigation Workspace are built entirely
from real, timestamped backend output. There is no fake/mock API data path.

## Testing

Backend:

```bash
cd jocky
python3 -m pytest tests/
```

Frontend:

```bash
cd jocky/dashboard
npx tsc --noEmit     # type-check
npm run lint          # eslint
```

## Deployment

- **Backend**: any standard WSGI host (gunicorn/uwsgi behind nginx, or a
  container) running `communication/server.py`'s Flask `app`. Set `FLASK_ENV`
  appropriately and disable `debug=True` in production.
- **Frontend**: `npm run build` in `dashboard/` produces a deployable build
  (TanStack Start supports both static and SSR output — see
  `dashboard/README.md` for the framework-level details). Set
  `VITE_API_BASE_URL` to your deployed Flask API's URL at build time.
- Serve both over HTTPS in production; the frontend detects and reports
  mixed-content blocking (HTTPS page → HTTP API) instead of failing silently.

## Safety & scope

JOCKY implements **defensive, read-only forensic analysis only**. See
[PRD.md](./PRD.md#security--safety-boundaries) for the explicit boundary
between what's implemented here and the offensive/evasive terminology that
appears only as threat-modeling context in the original problem statement.
