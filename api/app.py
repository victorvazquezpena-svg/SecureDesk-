from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Clave temporal para gestionar sesiones.
# Más adelante se moverá a una variable de entorno.
app.secret_key = "dev-secret-key"

# Almacenamiento temporal hasta conectar MySQL.
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

    if not username or not password:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    if username in usuarios:
        return jsonify({
            "error": "el usuario ya existe"
        }), 409

    usuarios[username] = generate_password_hash(password)

    return jsonify({
        "username": username
    }), 201


@app.post("/api/login")
def login():
    datos = request.get_json(silent=True) or {}

    username = datos.get("username")
    password = datos.get("password")

    if not username or not password:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    if username not in usuarios:
        return jsonify({
            "error": "usuario o contraseña incorrectos"
        }), 401

    if not check_password_hash(usuarios[username], password):
        return jsonify({
            "error": "usuario o contraseña incorrectos"
        }), 401

    session["username"] = username

    return jsonify({
        "message": "sesión iniciada correctamente",
        "username": username
    }), 200