# Pruebas automáticas con pytest — NoVa

## 1. Objetivo

Este documento describe las pruebas automáticas implementadas con `pytest` para la API de NoVa.

El objetivo de estas pruebas es verificar de forma automática el comportamiento esperado de los endpoints principales de autenticación y gestión de tickets, comprobando tanto los casos correctos como los errores de validación, autenticación y aislamiento entre usuarios.

Estas pruebas complementan las pruebas manuales recogidas en `PRUEBAS.md`.

---

## 2. Herramientas utilizadas

- Python
- Flask
- pytest
- Cliente de pruebas integrado de Flask (`app.test_client()`)

---

## 3. Alcance de las pruebas

Se han automatizado pruebas sobre los siguientes bloques:

- Estado de la API.
- Registro de usuarios.
- Inicio de sesión.
- Consulta de tickets.
- Creación de tickets.
- Modificación de tickets.
- Eliminación de tickets.
- Acceso sin autenticación.
- Aislamiento entre usuarios.

---

## 4. Ubicación de los tests

Los tests automáticos se encuentran en el directorio:

```text
tests/


