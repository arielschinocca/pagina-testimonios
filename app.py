from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://www.tarotcentaura.com",
    "https://tarotcentaura.com",
    "https://pagina-testimonios-backend.onrender.com"
]}})


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
print("Conectando a:", MONGO_URI)  # Agregado para debug
db = client["tarotcentaura"]
collection = db["testimonios"]

@app.route("/")
def home():
    return "API Tarot Centaura funcionando con MongoDB"

@app.route("/api/testimonios", methods=["GET"])
def get_testimonios():
    testimonios = list(collection.find({}, {"_id": 0}))
    return jsonify(testimonios)

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

    collection.insert_one(nuevo)
    return jsonify({"success": True}), 201

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

