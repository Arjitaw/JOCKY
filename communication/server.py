from flask import Flask, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "JOCKY API is running"
    }


@app.route("/command", methods=["POST"])
def command():

    data = request.json

    print("Received:")
    print(data)

    return {
        "status": "received",
        "data": data
    }


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )