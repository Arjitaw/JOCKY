import os
import time

from flask import Flask, request
from flask_cors import CORS

from communication.dispatcher import execute_command
from compiler.Language_meta import LANGUAGE_REFERENCE
from compiler.parser import parse_command
from reports.report import create_report

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "JOCKY API is running",
        "engine": "online",
    }


@app.route("/commands", methods=["GET"])
def commands():
    """Expose the supported command reference so the frontend never has
    to hardcode syntax that could drift from the grammar."""
    return {"status": "success", "commands": LANGUAGE_REFERENCE}


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}

    command_text = data.get("command", "").strip()

    if not command_text:
        return {
            "status": "error",
            "error": "Command cannot be empty",
        }, 400

    start = time.perf_counter()

    try:
        print("Received:", command_text)

        parsed = parse_command(command_text)
        print("Parsed:", parsed)

        result = execute_command(parsed)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        report = create_report(
            command=command_text,
            action=parsed.get("action"),
            target=parsed.get("path"),
            status="completed",
            result=result,
            execution_time_ms=elapsed_ms,
        )

        return {
            "status": "success",
            "command": command_text,
            "result": result,
            "report": report,
            "error": None,
        }

    except Exception as error:
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        print("ERROR:", error)

        report = create_report(
            command=command_text,
            action=None,
            target=None,
            status="failed",
            result=None,
            execution_time_ms=elapsed_ms,
            errors=[str(error)],
        )

        return {
            "status": "error",
            "command": command_text,
            "report": report,
            "error": str(error),
        }, 400


if __name__ == "__main__":
    app.run(
        host=os.environ.get("JOCKY_HOST", "127.0.0.1"),
        port=int(os.environ.get("JOCKY_PORT", "5000")),
        debug=True,
    )
