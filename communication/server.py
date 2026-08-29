from flask import Flask, request
from flask_cors import CORS

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

    return {
        "status": "success",
        "command": command_text,
        "result": {
            "message": "Command received successfully"
        },
        "error": None
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )