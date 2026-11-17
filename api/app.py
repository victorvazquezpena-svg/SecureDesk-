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


# -------------------------------------------------------------------
# MODIFICAR TICKET
# -------------------------------------------------------------------
# Esta ruta permite modificar un ticket existente.

# Ejemplo:
#
# PUT /api/items/1
#
# El número que aparece al final de la URL corresponde al ID del ticket.
#
# Flask recoge automáticamente ese número gracias a:
#
# <int:ticket_id>
#
# Si hacemos:
#
# PUT /api/items/3
#
# entonces:
#
# ticket_id = 3
#

@app.put("/api/items/<int:ticket_id>")
def update_item(ticket_id):

    # Antes de modificar nada comprobamoos que haya un usuario autenticado.
    #
    # Si no existe "username" dentro de session,
    # significa que el usuario no ha iniciado sesión.
    if "username" not in session:
        return jsonify({
            "error": "usuario no autenticado"
        }), 401

    # -------------------------------------------------------------------
    # BUSCAR EL TICKET
    # -------------------------------------------------------------------
    
    # Inicialmente suponemos que no hemos encontrado ningún ticket.
    ticket_encontrado = None

    # Recorremos uno por uno todos los tickets guardados en memoria.
    for ticket in tickets:
        # Comparamos el ID del ticket actual con el ID recibido en la URL.
        #
        # Ejemplo:
        #
        # URL:
        # PUT /api/items/3
        #
        # ticket_id = 3
        #
        # Si encontramos:
        #
        # ticket["id"] == 3
        #
        # significa que hemos encontrado el ticket solicitado.    
        if ticket["id"] == ticket_id:

            # Guardamos ese ticket en una variable.
            ticket_encontrado = ticket

            # Ya no necesitamos seguir recorriendo la lista.
            break

    # Si después de recorrer todos los tickets seguimos teniendo None,
    # significa que no existe ningún ticket con ese ID.
    if ticket_encontrado is None:
        return jsonify({
            "error": "ticket no encontrado"
        }), 404

    
    # -------------------------------------------------------------------
    # COMPROBAR PROPIETARIO
    # -------------------------------------------------------------------

    # Aunque el ticket exista, todavía tenemos que comprobar
    # que pertenezca al usuario que ha iniciado sesión.
    #
    # Ejemplo:
    #
    # ticket:
    # owner = "carlos"
    #
    # sesión:
    # username = "victor"
    #
    # Carlos != Victor
    #
    # Por tanto Victor NO puede modificar ese ticket.
    if ticket_encontrado["owner"] != session["username"]:
        return jsonify({
            "error": "ticket no encontrado"
        }), 404

    # Devolvemos también 404 cuando el ticket pertenece a otro usuario.
    #
    # Así no revelamos si el ticket realmente existe o pertenece
    # a otra persona.


    # -------------------------------------------------------------------
    # LEER LOS NUEVOS DATOS
    # -------------------------------------------------------------------

    # Leemos el JSON enviado por el cliente.
    #
    # Ejemplo:
    #
    # {
    #     "title": "Problema VPN corporativa",
    #     "text": "Sigue sin funcionar",
    #     "category": "Red",
    #     "priority": "Alta",
    #     "status": "En progreso"
    # }
    #
    datos = request.get_json(silent=True) or {}
    print("DATOS RECIBIDOS:", datos)
    # Extraer todos los campos recibidos.
    title = datos.get("title")
    text = datos.get("text")
    category = datos.get("category")
    priority = datos.get("priority")
    status = datos.get("status")


    # Para esta ruta PUT exigimos todos los campos.
    #
    # Si falta cualquiera de ellos, rechazamos la petición.
    if not title or not text or not category or not priority or not status:
        return jsonify({
            "error": "datos no válidos"
        }), 400

    # -------------------------------------------------------------------
    # VALIDAR CATEGORÍA
    # -------------------------------------------------------------------
    
    # Categorías permitidas por NoVa.
    categorias_permitidas = [
        "Hardware",
        "Software",
        "Red",
        "Acceso y cuentas",
        "Otros"
    ]

    # Prioridades permitidas.
    prioridades_permitidas = [
        "Baja",
        "Media",
        "Alta",
        "Crítica"
    ]

    # Estados permitidos
    estados_permitidos = [
        "Abierta",
        "En progreso",
        "Resuelta",
        "Cerrada"
    ]

    # Comprobamos que la categoría enviada sea válida.
    if category not in categorias_permitidas:
        return jsonify({
            "error": "categoría no válida"
        }), 400
    
    # Comprobamos que la prioridad sea válida.
    if priority not in prioridades_permitidas:
        return jsonify({
            "error": "prioridad no válida"
        }), 400
    
    # Comprobamos que el estado sea uno de los permitidos.
    if status not in estados_permitidos:
        return jsonify({
            "error": "estado no válido"
        }), 400

    # -------------------------------------------------------------------
    # ACTUALIZAR EL TICKET
    # -------------------------------------------------------------------

    # Una vez realizadas todas las comprobaciones,
    # modificamos los valores del ticket existente.
    ticket_encontrado["title"] = title
    ticket_encontrado["text"] = text
    ticket_encontrado["category"] = category
    ticket_encontrado["priority"] = priority
    ticket_encontrado["status"] = status


    # La fecha de creación NO cambia.
    #
    # Solo actualizamos la fecha de modificación para indicar
    # cuándo se realizó el último cambio.
    ticket_encontrado["updated_at"] = datetime.now(timezone.utc).isoformat()


    # -------------------------------------------------------------------
    # PREPARAR RESPUESTA
    # -------------------------------------------------------------------
    
    # Construimos el JSON que devolveremos al cliente.
    #
    # Igual que al crear tickets, no devolvemos "owner"
    # porque es información interna del servidor.
    respuesta = {
        "id": ticket_encontrado["id"],
        "title": ticket_encontrado["title"],
        "text": ticket_encontrado["text"],
        "category": ticket_encontrado["category"],
        "priority": ticket_encontrado["priority"],
        "status": ticket_encontrado["status"],
        "created_at": ticket_encontrado["created_at"],
        "updated_at": ticket_encontrado["updated_at"]
    }

    # Devolvemos el ticket actualizado y código 200 OK.
    return jsonify(respuesta), 200



# -------------------------------------------------------------------
# ELIMINAR TICKET
# -------------------------------------------------------------------

# Esta ruta permite eliminar un ticket existente.
#
# Ejemplo:
#
# DELETE /api/items/1
#
# El número final corresponde al ID del ticket que queremos borrar.
@app.delete("/api/items/<int:ticket_id>")
def delete_item(ticket_id):

    # Solo un usuario autenticado puede eliminar tickets.
    if "username" not in session:
        return jsonify({
            "error": "usuario no autenticado"
        }), 401


    # -------------------------------------------------------------------
    # BUSCAR EL TICKET
    # -------------------------------------------------------------------

    # Inicialmente no hemos encontrado ningún ticket.
    ticket_encontrado = None


    # Recorremos la lista de tickets.
    for ticket in tickets:

        # Si encontramos el ID recibido en la URL,
        # guardamos ese ticket.
        if ticket["id"] == ticket_id:
            ticket_encontrado = ticket
            break


    # Si no existe ningún ticket con ese ID,
    # devolvemos 404.
    if ticket_encontrado is None:
        return jsonify({
            "error": "ticket no encontrado"
        }), 404


    # -------------------------------------------------------------------
    # COMPROBAR PROPIETARIO
    # -------------------------------------------------------------------

    # El ticket solo puede ser eliminado por su propietario.
    #
    # Si pertenece a otro usuario devolvemos también 404
    # para no revelar que ese ticket existe.
    if ticket_encontrado["owner"] != session["username"]:
        return jsonify({
            "error": "ticket no encontrado"
        }), 404


    # -------------------------------------------------------------------
    # ELIMINAR TICKET
    # -------------------------------------------------------------------

    # Eliminamos el ticket de la lista.
    tickets.remove(ticket_encontrado)


    # Código 204 significa:
    #
    # La operación se ha realizado correctamente,
    # pero no devolvemos contenido en la respuesta.
    return "", 204