import sys
from pathlib import Path

import pytest


# -------------------------------------------------------------------
# IMPORTAR LA APLICACIÓN
# -------------------------------------------------------------------

# Obtenemos la raíz del proyecto.
ROOT = Path(__file__).resolve().parents[1]

# Añadimos la carpeta api para poder importar app.py.
sys.path.insert(0, str(ROOT / "api"))

# Importamos el módulo completo para poder acceder
# a usuarios, tickets y siguiente_ticket_id.
import app as app_module

# Importamos la aplicación Flask.
from app import app


# -------------------------------------------------------------------
# LIMPIAR DATOS ANTES Y DESPUÉS DE CADA TEST
# -------------------------------------------------------------------

@pytest.fixture(autouse=True)
def limpiar_datos():

    # Como todavía usamos almacenamiento en memoria,
    # debemos asegurarnos de que cada test empieza
    # sin usuarios ni tickets creados anteriormente.
    app_module.usuarios.clear()
    app_module.tickets.clear()

    # Reiniciamos también el contador de tickets.
    app_module.siguiente_ticket_id = 1

    # Aquí se ejecutará el test.
    yield

    # Cuando termina el test volvemos a dejar
    # los datos completamente limpios.
    app_module.usuarios.clear()
    app_module.tickets.clear()
    app_module.siguiente_ticket_id = 1


# -------------------------------------------------------------------
# TEST 1 - HEALTH CHECK
# -------------------------------------------------------------------

def test_health():

    app.config["TESTING"] = True

    with app.test_client() as client:

        respuesta = client.get("/api/health")

        # Comprobamos que devuelve HTTP 200.
        assert respuesta.status_code == 200

        datos = respuesta.get_json()

        # Comprobamos el contenido del JSON.
        assert datos["status"] == "ok"
        assert datos["app"] == "NoVa"


# -------------------------------------------------------------------
# TEST 2 - REGISTRO CORRECTO
# -------------------------------------------------------------------

def test_register_usuario_correcto():

    app.config["TESTING"] = True

    with app.test_client() as client:

        respuesta = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        # El usuario debe crearse correctamente.
        assert respuesta.status_code == 201

        datos = respuesta.get_json()

        # Comprobamos que la API devuelve
        # el nombre del usuario registrado.
        assert datos["username"] == "victor"


# -------------------------------------------------------------------
# TEST 3 - USUARIO DUPLICADO
# -------------------------------------------------------------------

def test_register_usuario_duplicado():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos a Victor por primera vez.
        primera_respuesta = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        # La primera creación debe funcionar.
        assert primera_respuesta.status_code == 201


        # Intentamos registrar otra vez
        # exactamente el mismo usuario.
        segunda_respuesta = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        # La API debe rechazar el usuario duplicado.
        assert segunda_respuesta.status_code == 409

        datos = segunda_respuesta.get_json()

        assert datos["error"] == "el usuario ya existe"


# -------------------------------------------------------------------
# TEST 4 - REGISTRO INCOMPLETO
# -------------------------------------------------------------------

def test_register_datos_incompletos():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos registrar un usuario
        # sin enviar la contraseña.
        respuesta = client.post(
            "/api/register",
            json={
                "username": "victor"
            }
        )

        # La API debe rechazar la petición.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "datos no válidos"



# -------------------------------------------------------------------
# TEST 5 - LOGIN CORRECTO
# -------------------------------------------------------------------

def test_login_correcto():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Primero registramos al usuario,
        # porque no puede iniciar sesión si no existe.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Ahora intentamos iniciar sesión
        # con las credenciales correctas.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        # El login debe ser correcto.
        assert respuesta_login.status_code == 200

        datos = respuesta_login.get_json()

        # Comprobamos el contenido de la respuesta.
        assert datos["message"] == "sesión iniciada correctamente"
        assert datos["username"] == "victor"


        # -------------------------------------------------------------------
# TEST 6 - LOGIN CON CONTRASEÑA INCORRECTA
# -------------------------------------------------------------------

def test_login_password_incorrecta():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Primero registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Intentamos iniciar sesión con una contraseña incorrecta.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "ClaveIncorrecta123"
            }
        )

        # La API debe rechazar el inicio de sesión.
        assert respuesta_login.status_code == 401

        datos = respuesta_login.get_json()

        assert datos["error"] == "usuario o contraseña incorrectos"


# -------------------------------------------------------------------
# TEST 7 - LOGIN CON USUARIO INEXISTENTE
# -------------------------------------------------------------------

def test_login_usuario_inexistente():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos iniciar sesión con un usuario
        # que no ha sido registrado previamente.
        respuesta = client.post(
            "/api/login",
            json={
                "username": "pepe",
                "password": "Clave-1234"
            }
        )

        # La API debe rechazar el inicio de sesión.
        assert respuesta.status_code == 401

        datos = respuesta.get_json()

        assert datos["error"] == "usuario o contraseña incorrectos"




# -------------------------------------------------------------------
# TEST 8 - LOGIN CON DATOS INCOMPLETOS
# -------------------------------------------------------------------

def test_login_datos_incompletos():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos iniciar sesión enviando únicamente
        # el nombre de usuario y sin contraseña.
        respuesta = client.post(
            "/api/login",
            json={
                "username": "victor"
            }
        )

        # La API debe rechazar la petición.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "datos no válidos"



# -------------------------------------------------------------------
# TEST 9 - LISTAR TICKETS SIN SESIÓN
# -------------------------------------------------------------------

def test_get_items_sin_sesion():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos consultar los tickets sin haber iniciado sesión.
        respuesta = client.get("/api/items")

        # La API debe rechazar la petición.
        assert respuesta.status_code == 401

        datos = respuesta.get_json()

        assert datos["error"] == "usuario no autenticado"



# -------------------------------------------------------------------
# TEST 10 - LISTAR TICKETS CON SESIÓN Y SIN TICKETS
# -------------------------------------------------------------------

def test_get_items_con_sesion_sin_tickets():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Primero registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Ahora consultamos los tickets del usuario.
        respuesta = client.get("/api/items")


        # La petición debe funcionar correctamente.
        assert respuesta.status_code == 200

        datos = respuesta.get_json()


        # Como todavía no hemos creado ningún ticket,
        # esperamos recibir una lista vacía.
        assert datos == []


# -------------------------------------------------------------------
# TEST 11 - CREAR TICKET CORRECTAMENTE
# -------------------------------------------------------------------

def test_create_item_correcto():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Creamos un ticket válido.
        respuesta = client.post(
            "/api/items",
            json={
                "title": "No funciona la VPN",
                "text": "No consigo conectarme desde casa",
                "category": "Red",
                "priority": "Alta"
            }
        )


        # El ticket debe crearse correctamente.
        assert respuesta.status_code == 201

        datos = respuesta.get_json()


        # Comprobamos los datos principales del ticket.
        assert datos["id"] == 1
        assert datos["title"] == "No funciona la VPN"
        assert datos["text"] == "No consigo conectarme desde casa"
        assert datos["category"] == "Red"
        assert datos["priority"] == "Alta"

        # Los tickets nuevos siempre empiezan abiertos.
        assert datos["status"] == "Abierta"

        # Comprobamos que se han generado las fechas.
        assert "created_at" in datos
        assert "updated_at" in datos


# -------------------------------------------------------------------
# TEST 12 - CREAR TICKET CON CATEGORÍA NO VÁLIDA
# -------------------------------------------------------------------

def test_create_item_categoria_invalida():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Intentamos crear un ticket con una categoría
        # que no está permitida por la aplicación.
        respuesta = client.post(
            "/api/items",
            json={
                "title": "Problema de prueba",
                "text": "Este ticket tiene una categoría incorrecta",
                "category": "Patatas",
                "priority": "Alta"
            }
        )


        # La API debe rechazar la petición.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "categoría no válida"



# -------------------------------------------------------------------
# TEST 13 - CREAR TICKET CON PRIORIDAD NO VÁLIDA
# -------------------------------------------------------------------

def test_create_item_prioridad_invalida():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Intentamos crear un ticket con una prioridad
        # que no está permitida por la aplicación.
        respuesta = client.post(
            "/api/items",
            json={
                "title": "Problema de prueba",
                "text": "Este ticket tiene una prioridad incorrecta",
                "category": "Red",
                "priority": "Urgentísima"
            }
        )


        # La API debe rechazar la petición.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "prioridad no válida"


# -------------------------------------------------------------------
# TEST 14 - CREAR TICKET CON DATOS INCOMPLETOS
# -------------------------------------------------------------------

def test_create_item_datos_incompletos():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Intentamos crear un ticket sin el campo "text".
        respuesta = client.post(
            "/api/items",
            json={
                "title": "Problema incompleto",
                "category": "Red",
                "priority": "Alta"
            }
        )


        # La API debe rechazar la petición.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "datos no válidos"


# -------------------------------------------------------------------
# TEST 15 - MODIFICAR TICKET CORRECTAMENTE
# -------------------------------------------------------------------

def test_update_item_correcto():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Creamos primero un ticket.
        respuesta_creacion = client.post(
            "/api/items",
            json={
                "title": "No funciona la VPN",
                "text": "No consigo conectarme desde casa",
                "category": "Red",
                "priority": "Alta"
            }
        )

        assert respuesta_creacion.status_code == 201


        # Ahora modificamos el ticket recién creado.
        respuesta = client.put(
            "/api/items/1",
            json={
                "title": "Problema con VPN corporativa",
                "text": "Sigue sin conectar después de reiniciar",
                "category": "Red",
                "priority": "Alta",
                "status": "En progreso"
            }
        )


        # La modificación debe funcionar correctamente.
        assert respuesta.status_code == 200

        datos = respuesta.get_json()


        # El ticket mantiene el mismo ID.
        assert datos["id"] == 1

        # Comprobamos los nuevos valores.
        assert datos["title"] == "Problema con VPN corporativa"
        assert datos["text"] == "Sigue sin conectar después de reiniciar"
        assert datos["category"] == "Red"
        assert datos["priority"] == "Alta"
        assert datos["status"] == "En progreso"

        # Debe seguir teniendo fechas de creación y modificación.
        assert "created_at" in datos
        assert "updated_at" in datos


# -------------------------------------------------------------------
# TEST 16 - MODIFICAR TICKET CON ESTADO NO VÁLIDO
# -------------------------------------------------------------------

def test_update_item_estado_invalido():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Creamos primero un ticket válido.
        respuesta_creacion = client.post(
            "/api/items",
            json={
                "title": "Problema VPN",
                "text": "No conecta",
                "category": "Red",
                "priority": "Alta"
            }
        )

        assert respuesta_creacion.status_code == 201


        # Intentamos modificar el ticket usando
        # un estado que no está permitido.
        respuesta = client.put(
            "/api/items/1",
            json={
                "title": "Problema VPN",
                "text": "Sigue sin conectar",
                "category": "Red",
                "priority": "Alta",
                "status": "Volando"
            }
        )


        # La API debe rechazar la modificación.
        assert respuesta.status_code == 400

        datos = respuesta.get_json()

        assert datos["error"] == "estado no válido"


# -------------------------------------------------------------------
# TEST 17 - MODIFICAR TICKET SIN SESIÓN
# -------------------------------------------------------------------

def test_update_item_sin_sesion():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos modificar un ticket sin haber iniciado sesión.
        respuesta = client.put(
            "/api/items/1",
            json={
                "title": "Problema VPN",
                "text": "Sigue sin conectar",
                "category": "Red",
                "priority": "Alta",
                "status": "En progreso"
            }
        )

        # La API debe rechazar la petición.
        assert respuesta.status_code == 401

        datos = respuesta.get_json()

        assert datos["error"] == "usuario no autenticado"


# -------------------------------------------------------------------
# TEST 18 - MODIFICAR TICKET DE OTRO USUARIO
# -------------------------------------------------------------------

def test_update_item_otro_usuario():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # -------------------------------------------------------------------
        # REGISTRAR E INICIAR SESIÓN COMO VICTOR
        # -------------------------------------------------------------------

        respuesta_registro_victor = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro_victor.status_code == 201


        respuesta_login_victor = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login_victor.status_code == 200


        # Víctor crea un ticket.
        respuesta_creacion = client.post(
            "/api/items",
            json={
                "title": "Ticket de Victor",
                "text": "Este ticket pertenece a Victor",
                "category": "Red",
                "priority": "Alta"
            }
        )

        assert respuesta_creacion.status_code == 201


        # -------------------------------------------------------------------
        # REGISTRAR A CARLOS
        # -------------------------------------------------------------------

        respuesta_registro_carlos = client.post(
            "/api/register",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_registro_carlos.status_code == 201


        # Iniciamos sesión como Carlos.
        #
        # Como usamos el mismo cliente de Flask,
        # este login sustituye la sesión anterior de Víctor.
        respuesta_login_carlos = client.post(
            "/api/login",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_login_carlos.status_code == 200


        # -------------------------------------------------------------------
        # CARLOS INTENTA MODIFICAR EL TICKET DE VICTOR
        # -------------------------------------------------------------------

        respuesta = client.put(
            "/api/items/1",
            json={
                "title": "Ticket modificado por Carlos",
                "text": "Carlos intenta modificarlo",
                "category": "Red",
                "priority": "Baja",
                "status": "Cerrada"
            }
        )


        # La API debe impedirlo.
        #
        # Devolvemos 404 en vez de 403 para no revelar
        # que el ticket pertenece realmente a otro usuario.
        assert respuesta.status_code == 404

        datos = respuesta.get_json()

        assert datos["error"] == "ticket no encontrado"


# -------------------------------------------------------------------
# TEST 19 - ELIMINAR TICKET CORRECTAMENTE
# -------------------------------------------------------------------

def test_delete_item_correcto():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Creamos un ticket.
        respuesta_creacion = client.post(
            "/api/items",
            json={
                "title": "Problema con impresora",
                "text": "La impresora no responde",
                "category": "Hardware",
                "priority": "Media"
            }
        )

        assert respuesta_creacion.status_code == 201


        # Eliminamos el ticket.
        respuesta_delete = client.delete("/api/items/1")


        # DELETE correcto devuelve 204 No Content.
        assert respuesta_delete.status_code == 204


        # Comprobamos además que el ticket
        # realmente haya desaparecido.
        respuesta_get = client.get("/api/items")

        assert respuesta_get.status_code == 200

        datos = respuesta_get.get_json()

        assert datos == []


# -------------------------------------------------------------------
# TEST 20 - ELIMINAR TICKET SIN SESIÓN
# -------------------------------------------------------------------

def test_delete_item_sin_sesion():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Intentamos eliminar un ticket
        # sin haber iniciado sesión.
        respuesta = client.delete("/api/items/1")


        # La API debe rechazar la petición.
        assert respuesta.status_code == 401

        datos = respuesta.get_json()

        assert datos["error"] == "usuario no autenticado"



# -------------------------------------------------------------------
# TEST 21 - ELIMINAR TICKET INEXISTENTE
# -------------------------------------------------------------------

def test_delete_item_inexistente():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # Registramos al usuario.
        respuesta_registro = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro.status_code == 201


        # Iniciamos sesión.
        respuesta_login = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login.status_code == 200


        # Intentamos eliminar un ticket que no existe.
        respuesta = client.delete("/api/items/999")


        # La API debe devolver 404.
        assert respuesta.status_code == 404

        datos = respuesta.get_json()

        assert datos["error"] == "ticket no encontrado"



# -------------------------------------------------------------------
# TEST 22 - ELIMINAR TICKET DE OTRO USUARIO
# -------------------------------------------------------------------

def test_delete_item_otro_usuario():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # -------------------------------------------------------------------
        # REGISTRAR E INICIAR SESIÓN COMO VICTOR
        # -------------------------------------------------------------------

        respuesta_registro_victor = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro_victor.status_code == 201


        respuesta_login_victor = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login_victor.status_code == 200


        # Víctor crea un ticket.
        respuesta_creacion = client.post(
            "/api/items",
            json={
                "title": "Ticket de Victor",
                "text": "Este ticket pertenece a Victor",
                "category": "Red",
                "priority": "Alta"
            }
        )

        assert respuesta_creacion.status_code == 201


        # -------------------------------------------------------------------
        # REGISTRAR E INICIAR SESIÓN COMO CARLOS
        # -------------------------------------------------------------------

        respuesta_registro_carlos = client.post(
            "/api/register",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_registro_carlos.status_code == 201


        respuesta_login_carlos = client.post(
            "/api/login",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_login_carlos.status_code == 200


        # -------------------------------------------------------------------
        # CARLOS INTENTA ELIMINAR EL TICKET DE VICTOR
        # -------------------------------------------------------------------

        respuesta = client.delete("/api/items/1")


        # Carlos no debe poder borrar el ticket.
        assert respuesta.status_code == 404

        datos = respuesta.get_json()

        assert datos["error"] == "ticket no encontrado"


        # Además comprobamos que el ticket
        # sigue existiendo realmente.
        assert len(app_module.tickets) == 1
        assert app_module.tickets[0]["owner"] == "victor"


# -------------------------------------------------------------------
# TEST 23 - UN USUARIO NO VE LOS TICKETS DE OTRO
# -------------------------------------------------------------------

def test_get_items_aislamiento_usuarios():

    app.config["TESTING"] = True

    with app.test_client() as client:

        # -------------------------------------------------------------------
        # VICTOR CREA SU TICKET
        # -------------------------------------------------------------------

        respuesta_registro_victor = client.post(
            "/api/register",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_registro_victor.status_code == 201


        respuesta_login_victor = client.post(
            "/api/login",
            json={
                "username": "victor",
                "password": "Clave-1234"
            }
        )

        assert respuesta_login_victor.status_code == 200


        respuesta_ticket_victor = client.post(
            "/api/items",
            json={
                "title": "Ticket de Victor",
                "text": "Este ticket pertenece a Victor",
                "category": "Red",
                "priority": "Alta"
            }
        )

        assert respuesta_ticket_victor.status_code == 201


        # -------------------------------------------------------------------
        # CARLOS INICIA SESIÓN
        # -------------------------------------------------------------------

        respuesta_registro_carlos = client.post(
            "/api/register",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_registro_carlos.status_code == 201


        respuesta_login_carlos = client.post(
            "/api/login",
            json={
                "username": "carlos",
                "password": "Clave-5678"
            }
        )

        assert respuesta_login_carlos.status_code == 200


        # -------------------------------------------------------------------
        # CARLOS CONSULTA SUS TICKETS
        # -------------------------------------------------------------------

        respuesta = client.get("/api/items")

        assert respuesta.status_code == 200

        datos = respuesta.get_json()


        # Carlos no ha creado ningún ticket,
        # por lo que debe recibir una lista vacía.
        #
        # El ticket creado por Victor NO debe aparecer.
        assert datos == []


    