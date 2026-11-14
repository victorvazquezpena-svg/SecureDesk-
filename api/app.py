from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Temporal hasta conectar MySQL
usuarios = {}


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "app": "NoVa"
    }), 200


@app.post("/api/register")
def register():
    datos = request.get_json(silent=True) or {}

    username = datos.get("username")
    password = datos.get("password")

    # Comprobamos que los datos existen
    if not username or not password:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    # Comprobamos que el usuario no exista
    if username in usuarios:
        return jsonify({
            "error": "el usuario ya existe"
        }), 409

    # Guardamos la contraseña como hash
    usuarios[username] = generate_password_hash(password)

    return jsonify({
        "username": username
    }), 201