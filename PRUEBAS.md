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