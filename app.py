from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "testimonios.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/api/testimonios", methods=["GET"])
def get_testimonios():
    with open("testimonios.json") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/testimonios", methods=["POST"])
def add_testimonio():
    data = request.get_json()
    nuevo = {
        "nombre": data.get("nombre", "Anónimo"),
        "texto": data.get("texto", "")
    }
    with open("testimonios.json") as f:
        testimonios = json.load(f)
    testimonios.append(nuevo)
    with open("testimonios.json", "w") as f:
        json.dump(testimonios, f)
    return jsonify({"success": True}), 201


if __name__ == "__main__":
    app.run()


