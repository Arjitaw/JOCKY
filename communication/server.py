from flask import Flask, request
from flask_cors import CORS

from compiler.parser import parse_command
from communication.dispatcher import execute_command

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "JOCKY API is running"
    }


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}

    command_text = data.get("command", "").strip()

    if not command_text:
        return {
            "status": "error",
            "error": "Command cannot be empty"
        }, 400

    try:
        print("Received:", command_text)

        parsed = parse_command(command_text)
        print("Parsed:", parsed)

        result = execute_command(parsed)

        return {
            "status": "success",
            "command": command_text,
            "result": result,
            "error": None
        }

    except Exception as error:
        print("ERROR:", error)

        return {
            "status": "error",
            "command": command_text,
            "error": str(error)
        }, 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )