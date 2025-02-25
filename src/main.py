from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return "Hello, this is a secure Python app!"


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")  # Default to localhost
    port = int(os.getenv("FLASK_RUN_PORT", "8080"))
    app.run(host=host, port=port)
