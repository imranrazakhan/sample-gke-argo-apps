from flask import Flask

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return "Hello, this is a secure Python app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
