# NoVa — Requisitos funcionales

## 1. Objetivo

Este documento define las funcionalidades que deberá implementar la aplicación NoVa.

Los requisitos se utilizarán como referencia durante el desarrollo, las pruebas y la posterior revisión de seguridad de la aplicación.

---

## 2. Gestión de usuarios

### RF-01 — Registro de usuarios

El sistema permitirá crear una nueva cuenta mediante un nombre de usuario y una contraseña.

El servidor deberá comprobar que los datos recibidos son válidos antes de crear la cuenta.

No se permitirá registrar dos usuarios con el mismo nombre.

---

### RF-02 — Almacenamiento seguro de contraseñas

La contraseña del usuario no se almacenará directamente en la base de datos.

El sistema guardará únicamente un hash seguro de la contraseña.

---

### RF-03 — Inicio de sesión

El usuario podrá iniciar sesión introduciendo su nombre de usuario y contraseña.

Si las credenciales son correctas, el servidor creará una sesión válida para el usuario.

Si son incorrectas, el acceso será rechazado.

---

### RF-04 — Cierre de sesión

El usuario podrá cerrar su sesión desde la aplicación.

Al cerrar sesión, la credencial o sesión utilizada deberá dejar de ser válida.

---

## 3. Gestión de incidencias

### RF-05 — Consultar incidencias

Un usuario autenticado podrá consultar una lista con todas sus incidencias.

Únicamente deberán mostrarse las incidencias pertenecientes al usuario que ha iniciado sesión.

---

### RF-06 — Crear incidencias

Un usuario autenticado podrá crear una nueva incidencia.

Cada incidencia pertenecerá automáticamente al usuario que la haya creado.

---

### RF-07 — Datos de una incidencia

Cada incidencia podrá almacenar:

- Título.
- Descripción.
- Categoría.
- Prioridad.
- Estado.
- Fecha de creación.
- Fecha de última modificación.

---

### RF-08 — Categorías

Inicialmente las incidencias podrán utilizar las siguientes categorías:

- Hardware.
- Software.
- Red.
- Acceso y cuentas.
- Otros.

---

### RF-09 — Prioridades

Una incidencia podrá tener una de las siguientes prioridades:

- Baja.
- Media.
- Alta.
- Crítica.

---

### RF-10 — Estados

Una incidencia podrá encontrarse en uno de los siguientes estados:

- Abierta.
- En progreso.
- Resuelta.
- Cerrada.

---

### RF-11 — Modificar incidencias

Un usuario autenticado podrá modificar una incidencia siempre que sea el propietario de la misma.

El sistema deberá actualizar la fecha de modificación cuando se realice un cambio.

---

### RF-12 — Eliminar incidencias

Un usuario autenticado podrá eliminar una de sus propias incidencias.

Antes de realizar la operación, el servidor deberá comprobar que la incidencia pertenece al usuario.

---

## 4. Control de acceso

### RF-13 — Protección de incidencias entre usuarios

Un usuario nunca podrá consultar, modificar ni eliminar una incidencia perteneciente a otro usuario.

La comprobación se realizará en el servidor y no dependerá únicamente de la interfaz web.

---

### RF-14 — Acceso mediante sesión

Las operaciones relacionadas con incidencias requerirán que el usuario haya iniciado sesión.

Las peticiones realizadas sin una sesión válida deberán ser rechazadas.

---

## 5. Validación de datos

### RF-15 — Validación en el servidor

El servidor validará todos los datos recibidos antes de procesarlos o almacenarlos.

Se comprobarán, como mínimo:

- Campos obligatorios.
- Tipo de dato.
- Longitud máxima.
- Valores permitidos.
- Datos vacíos o incorrectos.

La aplicación no confiará únicamente en las comprobaciones realizadas por JavaScript en el navegador.

---

## 6. API

La comunicación entre el cliente web y el servidor se realizará mediante una API utilizando JSON.

La aplicación implementará como mínimo:

| Método | Ruta | Función |
|---|---|---|
| POST | `/api/register` | Registrar usuario |
| POST | `/api/login` | Iniciar sesión |
| GET | `/api/items` | Consultar incidencias propias |
| POST | `/api/items` | Crear incidencia |
| PUT | `/api/items/{id}` | Modificar incidencia propia |
| DELETE | `/api/items/{id}` | Eliminar incidencia propia |

Internamente, los elementos (`items`) representan las incidencias o tickets de NoVa.

---

## 7. Interfaz

### RF-16 — Interfaz web

NoVa dispondrá de una interfaz desarrollada mediante HTML, CSS y JavaScript.

El cliente se comunicará con la API utilizando `fetch()`.

---

### RF-17 — Adaptación a dispositivos móviles

La interfaz deberá poder utilizarse correctamente tanto desde un ordenador como desde un dispositivo móvil.

El diseño será responsive y deberá seguir siendo utilizable en pantallas de aproximadamente 360 píxeles de ancho.

---

## 8. Gestión de errores

### RF-18 — Respuestas de error

La aplicación deberá informar correctamente cuando una operación no pueda realizarse.

Los errores mostrados al usuario no deberán revelar:

- Consultas SQL.
- Contraseñas.
- Rutas internas.
- Trazas completas del servidor.
- Información sensible de configuración.

---

## 9. Pruebas

### RF-19 — Pruebas automáticas

Las funcionalidades principales deberán disponer de pruebas automáticas.

Se probarán tanto operaciones correctas como situaciones de error, incluyendo:

- Registro correcto.
- Usuario duplicado.
- Login correcto.
- Login incorrecto.
- Acceso sin sesión.
- Creación de incidencias.
- Consulta de incidencias.
- Modificación de incidencias propias.
- Intento de modificación de incidencias ajenas.
- Eliminación de incidencias propias.
- Intento de eliminación de incidencias ajenas.
- Validación de datos incorrectos.

---

## 10. Funcionalidades futuras

Cuando las funcionalidades principales estén terminadas y probadas podrán estudiarse ampliaciones como:

- Diferentes roles de usuario.
- Técnicos.
- Asignación de incidencias.
- Comentarios.
- Archivos adjuntos.
- Historial de cambios.
- Notificaciones.
- Búsqueda y filtros.
- Estadísticas.
- Panel de administración.

Estas funcionalidades no forman parte de los requisitos iniciales obligatorios de NoVa.