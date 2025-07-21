from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        serverSelectionTimeoutMS=5000
    )
    client.server_info()  # Forzar conexión para validar
    print("Conectado a MongoDB correctamente")
except errors.ServerSelectionTimeoutError as err:
    print("Error conectando a MongoDB:", err)

db = client["tarotcentaura"]
collection = db["testimonios"]

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    traceback.print_exc()  # Log del error en consola
    return jsonify({"error": "Error interno del servidor", "message": str(e)}), 500

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
