import os

from flask import Flask, jsonify, request

from counter import count_text

app = Flask(__name__, static_folder="static", static_url_path="")

MAX_TEXT_BYTES = 5 * 1024 * 1024
app.config["MAX_CONTENT_LENGTH"] = MAX_TEXT_BYTES


@app.get("/")
def index():
    return app.send_static_file("index.html")


@app.post("/api/count")
def count():
    payload = request.get_json(silent=True)
    text = payload.get("text") if isinstance(payload, dict) else None
    if not isinstance(text, str):
        return jsonify(error="Expected JSON body with a 'text' string."), 400
    return jsonify(count_text(text).to_dict())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="127.0.0.1", port=port, debug=os.environ.get("DEBUG") == "1")
