from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # timeout 5 segundos
    client.server_info()  # Forzar conexión para testear
    print("Conectado a MongoDB correctamente")
except errors.ServerSelectionTimeoutError as err:
    print("Error conectando a MongoDB:", err)

db = client["tarotcentaura"]
collection = db["testimonios"]

@app.route("/")
def home():
    return "API Tarot Centaura funcionando con MongoDB"

@app.route("/api/testimonios", methods=["GET"])
def get_testimonios():
    try:
        testimonios = list(collection.find({}, {"_id": 0}))
        return jsonify(testimonios)
    except Exception as e:
        print("Error al obtener testimonios:", e)
        return jsonify({"error": "No se pudieron cargar los testimonios"}), 500

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

    try:
        collection.insert_one(nuevo)
        return jsonify({"success": True}), 201
    except Exception as e:
        print("Error al guardar testimonio:", e)
        return jsonify({"error": "No se pudo guardar el testimonio."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
