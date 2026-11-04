# NoVa — Descripción general de la aplicación

## 1. Descripción

**NoVa** es una aplicación web para la gestión de incidencias o tickets.

Su objetivo es permitir que cada usuario pueda registrar problemas o incidencias, consultar su estado y gestionar la información asociada a cada una de ellas desde una interfaz sencilla y adaptable tanto a ordenador como a dispositivos móviles.

La aplicación estará formada por una interfaz web, una API desarrollada en Python y una base de datos encargada de almacenar los usuarios y sus incidencias.

---

## 2. Objetivo de la aplicación

NoVa pretende ofrecer un sistema sencillo para registrar y gestionar incidencias.

Cada usuario dispondrá de su propio espacio dentro de la aplicación y únicamente podrá acceder a los tickets que le pertenezcan.

La primera versión del proyecto se centrará en implementar correctamente las funcionalidades básicas antes de añadir características adicionales.

---

## 3. Funcionalidades principales

La aplicación permitirá realizar las siguientes acciones:

- Registrar una nueva cuenta de usuario.
- Iniciar sesión.
- Cerrar sesión.
- Consultar las incidencias propias.
- Crear nuevas incidencias.
- Editar incidencias propias.
- Eliminar incidencias propias.
- Consultar la información de cada incidencia.
- Impedir que un usuario pueda acceder o modificar incidencias pertenecientes a otro usuario.

---

## 4. Información de los usuarios

Inicialmente cada usuario almacenará como mínimo:

- Identificador único.
- Nombre de usuario.
- Contraseña almacenada mediante hash.
- Fecha de creación de la cuenta.

Las contraseñas nunca se almacenarán directamente en texto plano.

---

## 5. Información de las incidencias

Cada incidencia contará inicialmente con los siguientes datos:

- Identificador de la incidencia.
- Usuario propietario.
- Título.
- Descripción.
- Categoría.
- Prioridad.
- Estado.
- Fecha de creación.
- Fecha de última modificación.

### Categorías iniciales

- Hardware.
- Software.
- Red.
- Acceso y cuentas.
- Otros.

### Prioridades

- Baja.
- Media.
- Alta.
- Crítica.

### Estados

- Abierta.
- En progreso.
- Resuelta.
- Cerrada.

---

## 6. Control de acceso

Uno de los requisitos principales de NoVa será garantizar que cada usuario solo pueda trabajar con sus propios datos.

Un usuario autenticado podrá crear, consultar, modificar y eliminar únicamente sus propias incidencias.

Si intenta acceder a una incidencia perteneciente a otro usuario, el servidor deberá impedir la operación.

Las comprobaciones de permisos se realizarán siempre en el servidor y no dependerán únicamente de la interfaz web.

---

## 7. Arquitectura general

La aplicación seguirá una arquitectura dividida en tres partes principales:

### Cliente web

Desarrollado utilizando:

- HTML.
- CSS.
- JavaScript.

Será responsable de mostrar la interfaz al usuario y comunicarse con el servidor.

### API

Desarrollada principalmente utilizando:

- Python.
- Flask.

Será responsable de:

- Recibir las peticiones del cliente.
- Validar los datos.
- Gestionar la autenticación.
- Aplicar las reglas de acceso.
- Consultar o modificar la base de datos.
- Devolver las respuestas al cliente.

### Base de datos

La base de datos almacenará principalmente:

- Usuarios.
- Incidencias.

La comunicación con la base de datos se realizará únicamente desde el backend.

---

## 8. Comunicación cliente-servidor

La interfaz web se comunicará con la API mediante peticiones HTTP utilizando JavaScript y `fetch()`.

La información entre cliente y servidor se intercambiará utilizando formato JSON.

La API deberá disponer como mínimo de las siguientes operaciones:

- Registro de usuarios.
- Inicio de sesión.
- Consulta de incidencias.
- Creación de incidencias.
- Modificación de incidencias.
- Eliminación de incidencias.

---

## 9. Diseño para dispositivos móviles

NoVa será inicialmente una aplicación web responsive.

La interfaz deberá poder utilizarse correctamente tanto desde un ordenador como desde la pantalla de un teléfono móvil.

En una fase posterior del proyecto, el cliente web podrá empaquetarse como aplicación Android.

---

## 10. Seguridad

La seguridad será una parte importante del desarrollo de NoVa.

Entre otros aspectos se tendrán en cuenta:

- Almacenamiento seguro de contraseñas.
- Validación de los datos recibidos.
- Gestión segura de sesiones.
- Control de acceso a las incidencias.
- Protección de información sensible.
- Gestión correcta de errores.
- Pruebas automáticas.
- Revisión posterior mediante herramientas de análisis de seguridad.

---

## 11. Primera versión de NoVa

La primera versión se centrará únicamente en conseguir que funcionen correctamente:

1. Registro.
2. Login.
3. Logout.
4. Creación de incidencias.
5. Consulta de incidencias.
6. Modificación de incidencias.
7. Eliminación de incidencias.
8. Control de acceso entre usuarios.
9. Interfaz adaptable a móvil.
10. Pruebas de las funciones principales.

Una vez que estas funciones estén implementadas y probadas, podrán añadirse características adicionales.

---

## 12. Posibles ampliaciones

Cuando la aplicación básica esté completamente funcional podrán estudiarse funcionalidades como:

- Usuarios con distintos roles.
- Técnicos encargados de resolver incidencias.
- Asignación de tickets.
- Comentarios.
- Archivos adjuntos.
- Historial de cambios.
- Notificaciones.
- Panel de administración.
- Estadísticas.
- Búsqueda y filtrado de incidencias.

Estas funcionalidades no forman parte inicialmente de la versión mínima del proyecto.