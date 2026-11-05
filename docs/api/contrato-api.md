# NoVa — Contrato de la API

## 1. Objetivo

Este documento define cómo se comunicarán el cliente web y el servidor de NoVa.

El contrato establece:

- Las rutas disponibles.
- Los métodos HTTP utilizados.
- Los datos que debe enviar el cliente.
- Las respuestas del servidor.
- Los códigos HTTP.
- Las reglas de autenticación y autorización.

El frontend deberá respetar este contrato al realizar peticiones mediante `fetch()` y el backend deberá responder siguiendo el formato definido.

---

# 2. Formato general

La API utilizará:

- HTTP.
- JSON para el intercambio de datos.
- Sesiones para identificar al usuario autenticado.

Las peticiones que incluyan datos utilizarán:

```http
Content-Type: application/json
```

Ejemplo:

```json
{
  "username": "victor",
  "password": "ClaveSegura123"
}
```

---

# 3. Autenticación

NoVa utilizará una sesión asociada al usuario después de iniciar sesión correctamente.

El usuario no enviará su identificador (`id_usuario`) en las operaciones sobre tickets.

El backend obtendrá siempre el usuario propietario a partir de la sesión autenticada.

Por tanto, nunca se aceptará una petición como:

```json
{
  "id_usuario": 5,
  "title": "Problema de red"
}
```

para decidir a qué usuario pertenece una incidencia.

El propietario será determinado por el servidor.

---

# 4. Formato general de errores

Cuando sea posible, los errores de la API utilizarán una estructura común:

```json
{
  "error": "invalid_data",
  "message": "Los datos enviados no son válidos."
}
```

Las respuestas nunca deberán mostrar:

- Consultas SQL.
- Contraseñas.
- Hashes.
- Rutas internas del servidor.
- Variables de entorno.
- Trazas completas de Python.
- Información sensible de configuración.

---

# 5. Códigos HTTP utilizados

| Código | Significado |
|---|---|
| `200 OK` | Operación realizada correctamente |
| `201 Created` | Recurso creado correctamente |
| `204 No Content` | Operación correcta sin contenido de respuesta |
| `400 Bad Request` | Datos enviados incorrectos |
| `401 Unauthorized` | Usuario no autenticado o credenciales incorrectas |
| `403 Forbidden` | Usuario autenticado sin permisos |
| `404 Not Found` | Recurso inexistente o no accesible |
| `409 Conflict` | Conflicto con un recurso existente |

---

# 6. Registro de usuarios

## POST `/api/register`

Permite crear una nueva cuenta.

### Petición

```json
{
  "username": "victor",
  "password": "ClaveSegura123"
}
```

### Validaciones iniciales

`username`:

- Obligatorio.
- Texto.
- Entre 3 y 50 caracteres.
- Debe ser único.

`password`:

- Obligatoria.
- Texto.
- Entre 8 y 128 caracteres.

### Respuesta correcta

```http
201 Created
```

```json
{
  "message": "Cuenta creada correctamente."
}
```

### Posibles errores

#### Datos incorrectos

```http
400 Bad Request
```

```json
{
  "error": "invalid_data",
  "message": "Los datos enviados no son válidos."
}
```

#### Usuario existente

```http
409 Conflict
```

```json
{
  "error": "username_exists",
  "message": "El nombre de usuario ya está registrado."
}
```

---

# 7. Inicio de sesión

## POST `/api/login`

Permite autenticar al usuario.

### Petición

```json
{
  "username": "victor",
  "password": "ClaveSegura123"
}
```

### Respuesta correcta

```http
200 OK
```

```json
{
  "message": "Sesión iniciada correctamente."
}
```

El servidor creará la sesión correspondiente.

### Credenciales incorrectas

```http
401 Unauthorized
```

```json
{
  "error": "invalid_credentials",
  "message": "Usuario o contraseña incorrectos."
}
```

La respuesta no deberá indicar si el error corresponde específicamente al usuario o a la contraseña.

---

# 8. Cierre de sesión

## POST `/api/logout`

Ruta adicional de NoVa para permitir cerrar una sesión.

### Petición

No necesita cuerpo.

### Respuesta

```http
204 No Content
```

La sesión utilizada por el usuario deberá quedar invalidada.

---

# 9. Consultar incidencias

## GET `/api/items`

Devuelve las incidencias pertenecientes al usuario autenticado.

### Petición

No necesita cuerpo.

### Respuesta correcta

```http
200 OK
```

Ejemplo:

```json
[
  {
    "id": 12,
    "title": "No funciona la VPN",
    "text": "No consigo conectarme desde casa.",
    "category": "Red",
    "priority": "Alta",
    "status": "Abierta",
    "created_at": "2026-11-05T19:30:00",
    "updated_at": "2026-11-05T19:30:00"
  },
  {
    "id": 15,
    "title": "Problema con aplicación",
    "text": "La aplicación se cierra al iniciar.",
    "category": "Software",
    "priority": "Media",
    "status": "En progreso",
    "created_at": "2026-11-05T19:40:00",
    "updated_at": "2026-11-05T20:10:00"
  }
]
```

La API únicamente devolverá incidencias pertenecientes al usuario autenticado.

### Sin sesión

```http
401 Unauthorized
```

---

# 10. Crear incidencia

## POST `/api/items`

Crea una nueva incidencia para el usuario autenticado.

### Petición

```json
{
  "title": "No funciona la VPN",
  "text": "No consigo conectarme desde casa.",
  "category": "Red",
  "priority": "Alta"
}
```

El cliente no enviará:

```text
id_usuario
fecha_creacion
fecha_modificacion
```

Estos datos serán gestionados por el servidor.

El estado inicial será:

```text
Abierta
```

### Categorías permitidas

- `Hardware`
- `Software`
- `Red`
- `Acceso y cuentas`
- `Otros`

### Prioridades permitidas

- `Baja`
- `Media`
- `Alta`
- `Crítica`

### Respuesta correcta

```http
201 Created
```

Ejemplo:

```json
{
  "id": 12,
  "title": "No funciona la VPN",
  "text": "No consigo conectarme desde casa.",
  "category": "Red",
  "priority": "Alta",
  "status": "Abierta",
  "created_at": "2026-11-05T19:30:00",
  "updated_at": "2026-11-05T19:30:00"
}
```

### Sin sesión

```http
401 Unauthorized
```

### Datos incorrectos

```http
400 Bad Request
```

---

# 11. Modificar incidencia

## PUT `/api/items/{id}`

Permite modificar una incidencia perteneciente al usuario autenticado.

Ejemplo:

```http
PUT /api/items/12
```

### Petición

```json
{
  "title": "Problema con VPN corporativa",
  "text": "Sigue sin conectar después de reiniciar.",
  "category": "Red",
  "priority": "Alta",
  "status": "En progreso"
}
```

### Estados permitidos

- `Abierta`
- `En progreso`
- `Resuelta`
- `Cerrada`

### Respuesta correcta

```http
200 OK
```

Ejemplo:

```json
{
  "id": 12,
  "title": "Problema con VPN corporativa",
  "text": "Sigue sin conectar después de reiniciar.",
  "category": "Red",
  "priority": "Alta",
  "status": "En progreso",
  "created_at": "2026-11-05T19:30:00",
  "updated_at": "2026-11-05T20:15:00"
}
```

### Sin sesión

```http
401 Unauthorized
```

### Ticket inexistente o ajeno

```http
404 Not Found
```

NoVa utilizará `404` tanto cuando el ticket no exista como cuando pertenezca a otro usuario.

De esta forma no se revela a un usuario la existencia de recursos pertenecientes a otras cuentas.

### Datos incorrectos

```http
400 Bad Request
```

---

# 12. Eliminar incidencia

## DELETE `/api/items/{id}`

Permite eliminar una incidencia propia.

Ejemplo:

```http
DELETE /api/items/12
```

### Respuesta correcta

```http
204 No Content
```

La respuesta no tendrá cuerpo.

### Sin sesión

```http
401 Unauthorized
```

### Ticket inexistente o ajeno

```http
404 Not Found
```

El servidor deberá comprobar siempre que la incidencia pertenece al usuario autenticado antes de eliminarla.

---

# 13. Resumen de endpoints

| Método | Ruta | Autenticación | Función |
|---|---|---|---|
| POST | `/api/register` | No | Registrar usuario |
| POST | `/api/login` | No | Iniciar sesión |
| POST | `/api/logout` | Sí | Cerrar sesión |
| GET | `/api/items` | Sí | Consultar mis incidencias |
| POST | `/api/items` | Sí | Crear incidencia |
| PUT | `/api/items/{id}` | Sí | Modificar una incidencia propia |
| DELETE | `/api/items/{id}` | Sí | Eliminar una incidencia propia |

---

# 14. Regla de propiedad

La regla principal de autorización de NoVa será:

> Un usuario solamente puede consultar, modificar o eliminar las incidencias que le pertenecen.

Conceptualmente:

```text
Usuario autenticado
        |
        v
   solicita ticket
        |
        v
¿ticket.id_usuario == usuario.id?
        |
   +----+----+
   |         |
   Sí        No
   |         |
   v         v
Permitir    404
```

El control se realizará siempre en el backend.

---

# 15. Validación

El backend será responsable de validar todos los datos recibidos.

El cliente web podrá realizar validaciones para mejorar la experiencia del usuario, pero estas comprobaciones nunca sustituirán a las realizadas por el servidor.

Se comprobarán especialmente:

- Campos obligatorios.
- Longitudes.
- Tipos de datos.
- Valores permitidos.
- Identificadores.
- Sesión.
- Propiedad del recurso.

---

# 16. Correspondencia con la base de datos

La API utilizará dos entidades principales:

```text
USUARIOS
   |
   | 1
   |
   | N
   v
TICKETS
```

El identificador del usuario autenticado se utilizará internamente para consultar únicamente sus incidencias.

Ejemplo conceptual:

```text
GET /api/items

Sesión
   ↓
id_usuario = 3
   ↓
Backend
   ↓
Buscar tickets donde id_usuario = 3
   ↓
JSON
```

El cliente nunca decidirá directamente qué usuario es propietario de un ticket.

---

# 17. Consideraciones de seguridad

El contrato deberá mantenerse durante las posteriores fases de seguridad.

Se revisarán especialmente:

- Autenticación.
- Gestión de sesiones.
- Control de acceso.
- Validación de entradas.
- Inyecciones.
- XSS.
- CSRF.
- Manipulación de identificadores.
- Gestión de errores.
- Protección de contraseñas y credenciales.

Las mejoras de seguridad podrán modificar cabeceras, cookies o mecanismos internos sin cambiar necesariamente las rutas principales de la API.