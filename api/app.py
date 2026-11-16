#Importamos Flask para crear la aplicación web
# request nos permite leer los datos que envía el cliente.
# jsonify convierte diccionarios/listas de Python en JSON.
# session nos permite recordar qué usuario ha iniciado sesión.
from flask import Flask, request, jsonify, session

# generate_password_hash transforma una contraseña en un hash seguro.
# check_password_hash permite comprobar si una contraseña coincide con ese hash.
from werkzeug.security import generate_password_hash, check_password_hash

# Lo usamos para guardar la fecha y hora de creación/modificación de los tickets.
from datetime import datetime, timezone

# Creamos la aplicación con Flask
app = Flask(__name__)


# Flask necesita una clave para firmar las cookies de sesión.
# DE MOMENTO es temporal


# Clave temporal para las sesiones.
# Más adelante se moverá a una variable de entorno.
app.secret_key = "dev-secret-key"



# -------------------------------------------------------------------
# DATOS TEMPORALES
# -------------------------------------------------------------------

# Todavía no estamos usando MYSQL.
# Por eso guardamos los usuarios temporalmente en un diccionario.

#Ejemplo:

# usuarios = {
#     "victor": "hash_de_la_contraseña"
# }

usuarios = {}

# Los tickets también se guardan temporalmente en memoria.

# Cada ticket será un diccionario dentro de esta lista.

# Ejemplo:
#
# tickets = [
#     {
#         "id": 1,
#         "owner": "victor",
#         "title": "Problema VPN",
#         ...
#     }
# ]
tickets = []


# Simulamos un ID autoincremental de base de datos.
#
# Primer ticket  -> ID 1
# Segundo ticket -> ID 2
# Tercer ticket  -> ID 3

siguiente_ticket_id = 1


# -------------------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------------------
# Esta ruta sirve simplemente para comprobar que la API está funcionando.
#
# Si hacemos:
#
# GET /api/health
#
# Flask ejecuta esta función.

@app.get("/api/health")
def health():

    # Devolvemos JSON y código HTTP 200.
    return jsonify({
        "status": "ok",
        "app": "NoVa"
    }), 200


# -------------------------------------------------------------------
# REGISTRO DE USUARIOS
# -------------------------------------------------------------------
#Esta función se ejecuta cuando recibimos:
#
# POST /api/register

@app.post("/api/register")
def register():

    # Intentamos leer el JSON recibido.
    #
    # Ejemplo esperado:
    #
    # {
    #     "username": "victor",
    #     "password": "Clave-1234"
    # }
    #
    # Si no llega JSON válido, usamos {}.
    datos = request.get_json(silent=True) or {}

    # Sacamos los dos valores del JSON
    username = datos.get("username")
    password = datos.get("password")

    # Si falta username o password, rechazamos la petición (400).
    if not username or not password:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    # Comprobamos que el nombre de usuario no esté registrado
    if username in usuarios:
        return jsonify({
            "error": "el usuario ya existe"
        }), 409

    # NUNCA guardamos la contraseña en texto plano.
    #
    # Por ejemplo:
    #
    # "Clave-1234"
    #
    # se transforma en algo parecido a:
    #
    # scrypt:32768:8:1$....
    #

    usuarios[username] = generate_password_hash(password)

    # El usuario se ha creado correctamente
    return jsonify({
        "username": username
    }), 201

# -------------------------------------------------------------------
# LOGIN
# -------------------------------------------------------------------

# Esta función se ejecuta con:
#
# POST /api/login
#

@app.post("/api/login")
def login():

    datos = request.get_json(silent=True) or {}

    username = datos.get("username")
    password = datos.get("password")

    # Si faltan datos:
    if not username or not password:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    # Primero comprobamos si el usuario existe
    if username not in usuarios:
        return jsonify({
            "error": "usuario o contraseña incorrectos"
        }), 401

    # usuarios[username] contiene el HASH.
    #
    # check_password_hash compara:
    #
    # contraseña introducida
    #        VS
    # hash almacenado
    #

    if not check_password_hash(usuarios[username], password):
        return jsonify({
            "error": "usuario o contraseña incorrectos"
        }), 401

    # Si llegamos aquí:
    #
    # usuario correcto
    # contraseña correcta
    #
    # Guardamos el usuario en la sesión.

    session["username"] = username

    return jsonify({
        "message": "sesión iniciada correctamente",
        "username": username
    }), 200


# -------------------------------------------------------------------
# LISTAR TICKETS
# -------------------------------------------------------------------

# Esta ruta devuelve los tickets del usuario conectado.
#
# GET /api/items
#
@app.get("/api/items")
def get_items():

    # Antes de hacer nada comprobamos que haya sesión.
    #
    # Si session no contiene "username",
    # significa que nadie ha iniciado sesión.
    if "username" not in session:
        return jsonify({
            "error": "usuario no autenticado"
        }), 401

    # Recuperamos el nombre del usuario conectado
    username = session["username"]

    # Buscamos únicamente tickets cuyo propietario sea
    # el usuario que ha iniciado sesión.
    #
    # Ejemplo:
    #
    # victor tiene tickets 1 y 3
    # carlos tiene ticket 2
    #
    # Si inicia sesión victor:
    #
    # devolveremos 1 y 3.
    #
    
    mis_tickets = [
        {
            "id": ticket["id"],
            "title": ticket["title"],
            "text": ticket["text"],
            "category": ticket["category"],
            "priority": ticket["priority"],
            "status": ticket["status"],
            "created_at": ticket["created_at"],
            "updated_at": ticket["updated_at"]
        }

        # Recorremos todos los tickets
        for ticket in tickets

        # Pero solo cogemos los que pertenecen al usuario
        if ticket["owner"] == username
    ]

    # Devolvemos la lista como JSON
    return jsonify(mis_tickets), 200

# -------------------------------------------------------------------
# CREAR TICKET
# -------------------------------------------------------------------
# Esta ruta crea un ticket nuevo.
#
# POST /api/items
#
@app.post("/api/items")
def create_item():

    # Le decimos a Python que queremos modificar la variable
    # global siguiente_ticket_id.
    global siguiente_ticket_id

    # Solo un usuario autenticado puede crear tickets.
    if "username" not in session:
        return jsonify({
            "error": "usuario no autenticado"
        }), 401

    # Leemos el JSON enviado por el cliente.
    datos = request.get_json(silent=True) or {}

    # Extraemos los campos.
    title = datos.get("title")
    text = datos.get("text")
    category = datos.get("category")
    priority = datos.get("priority")

    # Todos los campos son obligatorios.
    if not title or not text or not category or not priority:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    # Solo permitimos estas categorías
    categorias_permitidas = [
        "Hardware",
        "Software",
        "Red",
        "Acceso y cuentas",
        "Otros"
    ]

    # Y únicamente estas prioridades
    prioridades_permitidas = [
        "Baja",
        "Media",
        "Alta",
        "Crítica"
    ]

    
    # Si el usuario intenta enviar:
    #
    # "category": "Patatas"
    #
    # se rechaza.
    if category not in categorias_permitidas:
        return jsonify({
            "error": "categoría no válida"
        }), 400

    # La misma lógica se aplica a la prioridad
    if priority not in prioridades_permitidas:
        return jsonify({
            "error": "prioridad no válida"
        }), 400

    # Guardamos la fecha/hora actual.
    #
    # timezone.utc significa que usamos UTC.
    #
    # isoformat produce algo como:
    #
    # 2026-11-16T18:30:20+00:00
    #

    fecha_actual = datetime.now(timezone.utc).isoformat()

    # Contruimos el ticket.
    nuevo_ticket = {
        
        # ID único del ticket
        "id": siguiente_ticket_id,
        # MUY IMPORTANTE:
        # el propietario NO viene del cliente.
        #
        # Lo sacamos directamente de la sesión.
        "owner": session["username"],

        "title": title,
        "text": text,
        "category": category,
        "priority": priority,

        # Los tickets nuevos siempre empiezan abiertos.
        "status": "Abierta",
        "created_at": fecha_actual,
        "updated_at": fecha_actual
    }

    # Añadimos el ticket a la lista.
    tickets.append(nuevo_ticket)

    # Preparamos el siguiente ID.
    siguiente_ticket_id += 1


    # Construimos la respuesta.
    #
    # Fíjate que NO devolvemos "owner".
    # El cliente no necesita conocer ese dato interno.
    respuesta = {
        "id": nuevo_ticket["id"],
        "title": nuevo_ticket["title"],
        "text": nuevo_ticket["text"],
        "category": nuevo_ticket["category"],
        "priority": nuevo_ticket["priority"],
        "status": nuevo_ticket["status"],
        "created_at": nuevo_ticket["created_at"],
        "updated_at": nuevo_ticket["updated_at"]
    }

    # Ticket creado correctamente.
    return jsonify(respuesta), 201