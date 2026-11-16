# Plan de pruebas — NoVa

Este documento recoge las pruebas manuales realizadas sobre la API de NoVa durante la Fase 1 del proyecto.

El objetivo es comprobar el comportamiento de los endpoints antes de crear las pruebas automáticas.

## Entorno de pruebas

- Backend: Python + Flask
- Puerto de ejecución: `8080`
- Formato de intercambio: JSON
- Sistema utilizado para las pruebas: Windows PowerShell
- Herramienta: `Invoke-RestMethod`
- Entorno virtual de Python: `venv`

La aplicación se arranca desde el directorio `api` mediante:

```powershell
flask --app app run --port 8080
```

---

# PR-01 — Comprobar estado de la API

## Objetivo

Comprobar que Flask está funcionando correctamente y que la API responde en el puerto `8080`.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/health" `
    -Method GET
```

## Resultado esperado

Código HTTP:

```text
200 OK
```

Respuesta:

```json
{
  "app": "NoVa",
  "status": "ok"
}
```

## Resultado obtenido

La API respondió correctamente.

**Estado: ✅ Superada**

---

# PR-02 — Registro correcto de usuario

## Objetivo

Comprobar que se puede crear un usuario enviando un nombre de usuario y una contraseña válidos.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor","password":"Clave-1234"}'
```

## Resultado esperado

Código HTTP:

```text
201 Created
```

Respuesta:

```json
{
  "username": "victor"
}
```

## Resultado obtenido

El usuario fue creado correctamente.

**Estado: ✅ Superada**

---

# PR-03 — Registro de usuario duplicado

## Objetivo

Comprobar que la API impide registrar dos usuarios con el mismo nombre.

## Comando utilizado

Se repite la petición anterior:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor","password":"Clave-1234"}'
```

## Resultado esperado

Código HTTP:

```text
409 Conflict
```

Respuesta:

```json
{
  "error": "el usuario ya existe"
}
```

## Resultado obtenido

La API rechazó correctamente el usuario duplicado.

**Estado: ✅ Superada**

---

# PR-04 — Registro con datos incompletos

## Objetivo

Comprobar que el servidor valida los datos recibidos y rechaza un registro sin contraseña.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor2"}'
```

## Resultado esperado

Código HTTP:

```text
400 Bad Request
```

Respuesta:

```json
{
  "error": "datos no válidos"
}
```

## Resultado obtenido

La API rechazó correctamente la petición.

**Estado: ✅ Superada**

---

# PR-05 — Inicio de sesión correcto

## Objetivo

Comprobar que un usuario registrado puede iniciar sesión utilizando sus credenciales.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor","password":"Clave-1234"}'
```

## Resultado esperado

Código HTTP:

```text
200 OK
```

Respuesta:

```json
{
  "message": "sesión iniciada correctamente",
  "username": "victor"
}
```

## Resultado obtenido

El inicio de sesión se realizó correctamente.

**Estado: ✅ Superada**

---

# PR-06 — Login con contraseña incorrecta

## Objetivo

Comprobar que no es posible iniciar sesión utilizando una contraseña incorrecta.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor","password":"ClaveIncorrecta123"}'
```

## Resultado esperado

Código HTTP:

```text
401 Unauthorized
```

Respuesta:

```json
{
  "error": "usuario o contraseña incorrectos"
}
```

## Resultado obtenido

La API rechazó correctamente el inicio de sesión.

**Estado: ✅ Superada**

---

# PR-07 — Login con usuario inexistente

## Objetivo

Comprobar el comportamiento cuando se intenta iniciar sesión con un usuario que no existe.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"pepe","password":"Clave-1234"}'
```

## Resultado esperado

Código HTTP:

```text
401 Unauthorized
```

Respuesta:

```json
{
  "error": "usuario o contraseña incorrectos"
}
```

La respuesta debe ser la misma que cuando la contraseña es incorrecta para no proporcionar información sobre la existencia de usuarios.

## Resultado obtenido

La API respondió correctamente.

**Estado: ✅ Superada**

---

# PR-08 — Login con datos incompletos

## Objetivo

Comprobar que el servidor rechaza una petición de login que no contiene todos los campos necesarios.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8080/api/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"username":"victor"}'
```

## Resultado esperado

Código HTTP:

```text
400 Bad Request
```

Respuesta:

```json
{
  "error": "datos no válidos"
}
```

## Resultado obtenido

La petición fue rechazada correctamente.

**Estado: ✅ Superada**

---

# Resumen de pruebas realizadas

| ID | Prueba | Código esperado | Estado |
|---|---|---:|---|
| PR-01 | Estado de la API | 200 | ✅ |
| PR-02 | Registro correcto | 201 | ✅ |
| PR-03 | Usuario duplicado | 409 | ✅ |
| PR-04 | Registro incompleto | 400 | ✅ |
| PR-05 | Login correcto | 200 | ✅ |
| PR-06 | Contraseña incorrecta | 401 | ✅ |
| PR-07 | Usuario inexistente | 401 | ✅ |
| PR-08 | Login incompleto | 400 | ✅ |

## Nota sobre PowerShell

`Invoke-RestMethod` muestra las respuestas HTTP `400`, `401` y `409` como errores de PowerShell.

Esto no significa que la prueba haya fallado. En estos casos esos códigos son precisamente el comportamiento esperado de la API.

---

# Pruebas pendientes

Cuando se implemente el CRUD de tickets se añadirán:

- Acceso a tickets sin sesión → `401`.
- Crear un ticket.
- Listar tickets propios.
- Modificar un ticket propio.
- Eliminar un ticket propio.
- Intentar acceder a un ticket de otro usuario.
- Intentar modificar un ticket de otro usuario.
- Intentar eliminar un ticket de otro usuario.
- Validación de los datos de los tickets.
- Cierre de sesión.
- Pruebas automáticas con `pytest`.

Las pruebas manuales documentadas en este archivo servirán posteriormente como referencia para crear las pruebas automáticas.


# PR-09 — Consultar tickets sin sesión

## Objetivo

Comprobar que un usuario no autenticado no puede consultar los tickets.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8081/api/items" `
    -Method GET
```

## Resultado esperado

Código HTTP:

```text
401 Unauthorized
```

Respuesta:

```json
{
  "error": "usuario no autenticado"
}
```

## Resultado obtenido

La API rechazó correctamente la petición al no existir una sesión activa.

**Estado: ✅ Superada**

---

# PR-10 — Consultar tickets con sesión y sin datos

## Objetivo

Comprobar que un usuario autenticado puede consultar sus tickets.

Después de registrar e iniciar sesión con el usuario `victor`, se guarda la sesión utilizando `-SessionVariable`.

## Login utilizado

```powershell
$body = @{
    username = "victor"
    password = "Clave-1234"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8081/api/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body `
    -SessionVariable novaSession
```

## Consulta de tickets

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8081/api/items" `
    -Method GET `
    -WebSession $novaSession
```

## Resultado esperado

Código HTTP:

```text
200 OK
```

Al no existir todavía tickets del usuario, la API devuelve una lista vacía:

```json
[]
```

## Resultado obtenido

La petición se realizó correctamente y no se devolvieron tickets.

**Estado: ✅ Superada**

---

# PR-11 — Crear un ticket correctamente

## Objetivo

Comprobar que un usuario autenticado puede crear una nueva incidencia.

## Datos utilizados

```powershell
$ticket = @{
    title = "No funciona la VPN"
    text = "No consigo conectarme desde casa"
    category = "Red"
    priority = "Alta"
} | ConvertTo-Json
```

## Petición

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8081/api/items" `
    -Method POST `
    -ContentType "application/json" `
    -Body $ticket `
    -WebSession $novaSession
```

## Resultado esperado

Código HTTP:

```text
201 Created
```

El ticket debe crearse automáticamente con:

- Un identificador único.
- El usuario autenticado como propietario.
- Estado inicial `Abierta`.
- Fecha de creación.
- Fecha de modificación.

## Resultado obtenido

Se creó correctamente el ticket:

```text
id         : 1
title      : No funciona la VPN
text       : No consigo conectarme desde casa
category   : Red
priority   : Alta
status     : Abierta
```

Las fechas `created_at` y `updated_at` fueron generadas automáticamente.

**Estado: ✅ Superada**

---

# PR-12 — Listar tickets después de crear uno

## Objetivo

Comprobar que el ticket creado aparece posteriormente al consultar las incidencias del usuario autenticado.

## Comando utilizado

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8081/api/items" `
    -Method GET `
    -WebSession $novaSession
```

## Resultado esperado

Código HTTP:

```text
200 OK
```

La respuesta debe incluir el ticket creado anteriormente.

## Resultado obtenido

La API devolvió correctamente el ticket con `id = 1`.

**Estado: ✅ Superada**

---

# PR-13 — Crear ticket con categoría no válida

## Objetivo

Comprobar que el backend rechaza categorías que no forman parte de las opciones permitidas.

## Ejemplo utilizado

```powershell
$ticket = @{
    title = "Problema de prueba"
    text = "Ticket con categoría incorrecta"
    category = "Patatas"
    priority = "Alta"
} | ConvertTo-Json
```

## Resultado esperado

Código HTTP:

```text
400 Bad Request
```

Respuesta:

```json
{
  "error": "categoría no válida"
}
```

**Estado: ✅ Superada**

---

# PR-14 — Crear ticket con prioridad no válida

## Objetivo

Comprobar que la API únicamente acepta las prioridades definidas por la aplicación.

## Ejemplo utilizado

```powershell
$ticket = @{
    title = "Problema de prueba"
    text = "Ticket con prioridad incorrecta"
    category = "Red"
    priority = "Urgentísima"
} | ConvertTo-Json
```

## Resultado esperado

Código HTTP:

```text
400 Bad Request
```

Respuesta:

```json
{
  "error": "prioridad no válida"
}
```

**Estado: ✅ Superada**

---

# PR-15 — Crear ticket con campos obligatorios incompletos

## Objetivo

Comprobar que el servidor valida que todos los campos obligatorios estén presentes.

## Ejemplo utilizado

En esta prueba se omite el campo `text`.

```powershell
$ticket = @{
    title = "Problema de prueba"
    category = "Red"
    priority = "Alta"
} | ConvertTo-Json
```

## Resultado esperado

Código HTTP:

```text
400 Bad Request
```

Respuesta:

```json
{
  "error": "datos no válidos"
}
```

**Estado: ✅ Superada**

---

# Resumen actualizado

| ID | Prueba | Código esperado | Estado |
|---|---|---:|---|
| PR-09 | Consultar tickets sin sesión | 401 | ✅ |
| PR-10 | Consultar tickets con sesión | 200 | ✅ |
| PR-11 | Crear ticket válido | 201 | ✅ |
| PR-12 | Listar ticket creado | 200 | ✅ |
| PR-13 | Categoría no válida | 400 | ✅ |
| PR-14 | Prioridad no válida | 400 | ✅ |
| PR-15 | Campos obligatorios incompletos | 400 | ✅ |

## Estado actual del CRUD

Actualmente están implementadas y probadas las siguientes operaciones:

```text
GET  /api/items   ✅
POST /api/items   ✅
```

Quedan pendientes para la siguiente sesión:

```text
PUT    /api/items/{id}
DELETE /api/items/{id}
```

También queda pendiente comprobar el aislamiento completo entre usuarios, de forma que un usuario no pueda modificar ni eliminar tickets pertenecientes a otra cuenta.