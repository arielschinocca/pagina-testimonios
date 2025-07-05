from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)

# Permitir solo tu dominio frontend para CORS
CORS(app, resources={r"/*": {"origins": ["https://tarotcentaura.com"]}})

DATA_FILE = "testimonios.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def home():
    return "API Tarot Centaura funcionando"

@app.route("/api/testimonios", methods=["GET"])
def get_testimonios():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/api/testimonios", methods=["POST"])
def add_testimonio():
    data = request.get_json()
    nombre = data.get("nombre", "Anónimo").strip()
    texto = data.get("texto", "").strip()
    instagram = data.get("instagram", "").replace("@", "").strip()
    puntuacion = data.get("puntuacion", 5)

    if len(texto.split()) < 2:
        return jsonify({"error": "El testimonio debe tener al menos 2 palabras."}), 400

    nuevo = {
        "nombre": nombre,
        "texto": texto,
        "instagram": instagram,
        "puntuacion": puntuacion
    }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        testimonios = json.load(f)

    testimonios.append(nuevo)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(testimonios, f, ensure_ascii=False, indent=2)

    return jsonify({"success": True}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

