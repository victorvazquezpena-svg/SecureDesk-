// ======================================================
// NoVa - JavaScript del frontend
// ======================================================
//
// Este archivo se carga desde varias páginas HTML:
//
// - registro.html
// - login.html
// - tickets.html
// - tickets-formulario.html
//
// La idea es tener un único archivo JavaScript común
// para toda la aplicación.
//
// De momento SOLO vamos a programar:
//
// 1. Registro de usuarios.
// 2. Inicio de sesión.
//
// Más adelante añadiremos:
// - Logout.
// - Listado de tickets.
// - Crear tickets.
// - Editar tickets.
// - Eliminar tickets.
//
// ======================================================


// ======================================================
// 1. REGISTRO DE USUARIO
// ======================================================
//
// Endpoint del backend:
//
// POST /api/register
//
// Flask espera recibir un JSON parecido a:
//
// {
//     "username": "victor",
//     "password": "1234"
// }
//
// ======================================================


// Buscamos en la página un elemento con id="form-registro".
//
// Ese formulario solamente existe en registro.html.
//
// Si estamos, por ejemplo, en login.html:
//
// document.getElementById("form-registro")
//
// devolverá null porque ese elemento no existe en esa página.
console.log("app.js cargado correctamente");
const formRegistro = document.getElementById("form-registro");


// Comprobamos que el formulario realmente exista.
//
// Esto es importante porque app.js se carga desde varias páginas.
//
// Si estamos en registro.html, formRegistro tendrá el formulario.
//
// Si estamos en otra página, será null y este bloque simplemente
// no se ejecutará.
if (formRegistro) {

    // addEventListener sirve para "escuchar" eventos.
    //
    // En este caso estamos escuchando el evento "submit",
    // es decir, cuando el usuario pulsa el botón Registrarse.
    formRegistro.addEventListener("submit", async function (evento) {

        // Por defecto, cuando se envía un formulario HTML,
        // el navegador intenta recargar o cambiar de página.
        //
        // Nosotros NO queremos eso porque vamos a enviar los datos
        // mediante JavaScript usando fetch().
        //
        // preventDefault() evita el comportamiento normal del formulario.
        evento.preventDefault();


        // --------------------------------------------------
        // Recoger los datos escritos por el usuario
        // --------------------------------------------------

        // Buscamos el input cuyo id es "usuario".
        //
        // .value obtiene el texto que el usuario ha escrito.
        const username = document.getElementById("usuario").value;


        // Hacemos lo mismo con la contraseña.
        const password = document.getElementById("contrasena").value;


        // Buscamos la caja HTML donde mostraremos los mensajes
        // de error si el registro falla.
        const mensajeError = document.getElementById("mensaje-error");


        // La ocultamos al empezar.
        //
        // Esto sirve por si anteriormente apareció un error.
        mensajeError.classList.add("oculto");


        // --------------------------------------------------
        // Comunicación con Flask
        // --------------------------------------------------

        try {

            // fetch() sirve para hacer peticiones HTTP desde JavaScript.
            //
            // Es parecido a cuando nosotros probábamos la API con
            // Invoke-RestMethod o curl, pero ahora lo hace el navegador.
            //
            // Aquí estamos llamando a:
            //
            // POST /api/register
            //
            const respuesta = await fetch("/api/register", {

                // Indicamos que queremos hacer una petición POST.
                method: "POST",


                // Indicamos al backend que estamos enviando JSON.
                headers: {
                    "Content-Type": "application/json"
                },


                // body contiene los datos que vamos a enviar.
                //
                // JavaScript trabaja con objetos como:
                //
                // {
                //     username: username,
                //     password: password
                // }
                //
                // Pero HTTP necesita enviarlo como texto JSON.
                //
                // JSON.stringify() convierte el objeto JavaScript
                // en una cadena JSON.
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });


            // --------------------------------------------------
            // Registro correcto
            // --------------------------------------------------

            // Nuestro backend devuelve HTTP 201 cuando crea
            // correctamente un usuario.
            if (respuesta.status === 201) {

                // Si el registro funciona, enviamos al usuario
                // a la pantalla de login.
                window.location.href = "login.html";


                // return termina aquí la ejecución de esta función.
                //
                // Así evitamos continuar con el código de errores
                // que aparece debajo.
                return;
            }


            // --------------------------------------------------
            // Registro incorrecto
            // --------------------------------------------------

            // Si Flask ha respondido con un error como:
            //
            // 400 Bad Request
            // 409 Conflict
            //
            // nuestro backend devuelve normalmente un JSON parecido a:
            //
            // {
            //     "error": "el usuario ya existe"
            // }
            //
            // .json() convierte la respuesta HTTP en un objeto
            // JavaScript que podamos utilizar.
            const datos = await respuesta.json();


            // Cambiamos el texto de la caja de error.
            //
            // Si Flask ha enviado datos.error, mostramos ese mensaje.
            //
            // Si por algún motivo no existe datos.error,
            // mostramos nuestro mensaje genérico.
            mensajeError.textContent =
                datos.error || "No se ha podido registrar el usuario.";


            // Quitamos la clase "oculto".
            //
            // Al quitarla, el mensaje aparece en pantalla.
            mensajeError.classList.remove("oculto");

        } catch (error) {

            // --------------------------------------------------
            // Error de conexión
            // --------------------------------------------------
            //
            // Este bloque no se ejecuta porque el usuario haya
            // escrito mal la contraseña.
            //
            // Se ejecutaría, por ejemplo, si:
            //
            // - Flask está apagado.
            // - No podemos conectar con el servidor.
            // - Existe algún problema de red.
            //

            mensajeError.textContent =
                "No se ha podido conectar con el servidor.";


            // Mostramos el mensaje en pantalla.
            mensajeError.classList.remove("oculto");


            // console.error() muestra información del error
            // en la consola del navegador.
            //
            // Es útil para nosotros durante el desarrollo.
            console.error("Error durante el registro:", error);
        }

    });
}


// ======================================================
// 2. INICIO DE SESIÓN
// ======================================================
//
// Endpoint del backend:
//
// POST /api/login
//
// Flask espera:
//
// {
//     "username": "victor",
//     "password": "1234"
// }
//
// Si las credenciales son correctas:
//
// Flask guarda el usuario en la sesión.
//
// Después podremos acceder a:
//
// GET /api/items
//
// usando esa misma sesión.
//
// ======================================================


// Buscamos el formulario del login.
//
// Este elemento solamente existe en login.html.
const formLogin = document.getElementById("form-login");


// Solo ejecutamos este código si estamos realmente
// en la página de login.
if (formLogin) {

    // Escuchamos el envío del formulario.
    formLogin.addEventListener("submit", async function (evento) {

        // Evitamos que el formulario haga su comportamiento
        // tradicional y recargue la página.
        evento.preventDefault();


        // --------------------------------------------------
        // Recoger credenciales
        // --------------------------------------------------

        // Obtenemos el usuario escrito en el formulario.
        const username = document.getElementById("usuario").value;


        // Obtenemos la contraseña.
        const password = document.getElementById("contrasena").value;


        // Obtenemos la caja donde se mostrarán errores.
        const mensajeError = document.getElementById("mensaje-error");


        // Ocultamos posibles errores anteriores.
        mensajeError.classList.add("oculto");


        // --------------------------------------------------
        // Enviar login a Flask
        // --------------------------------------------------

        try {

            // Enviamos una petición HTTP al endpoint de login.
            const respuesta = await fetch("/api/login", {

                // Nuestra API define el login como POST.
                method: "POST",


                // Informamos de que enviamos JSON.
                headers: {
                    "Content-Type": "application/json"
                },


                // Convertimos usuario y contraseña a JSON.
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });


            // --------------------------------------------------
            // Login correcto
            // --------------------------------------------------

            // respuesta.ok significa que Flask ha respondido
            // con un código HTTP correcto, normalmente 200-299.
            //
            // En nuestro caso el login correcto devuelve 200.
            if (respuesta.ok) {

                // En este momento Flask ya habrá creado
                // la sesión del usuario.
                //
                // Ahora podemos mandarlo a la página de tickets.
                window.location.href = "tickets.html";


                // Terminamos aquí la función.
                return;
            }


            // --------------------------------------------------
            // Login incorrecto
            // --------------------------------------------------

            // Si llegamos aquí significa que Flask ha respondido
            // con algún error.
            //
            // Por ejemplo:
            //
            // 400 -> faltan datos.
            // 401 -> usuario o contraseña incorrectos.
            //
            const datos = await respuesta.json();


            // Mostramos el mensaje enviado por el backend.
            mensajeError.textContent =
                datos.error || "Nombre de usuario o contraseña incorrectos.";


            // Hacemos visible la caja de error.
            mensajeError.classList.remove("oculto");

        } catch (error) {

            // --------------------------------------------------
            // Error comunicándose con Flask
            // --------------------------------------------------

            mensajeError.textContent =
                "No se ha podido conectar con el servidor.";


            mensajeError.classList.remove("oculto");


            // Mostramos el error técnico en la consola
            // para poder depurarlo nosotros.
            console.error("Error durante el login:", error);
        }

    });
}

// ======================================================
// 3. CERRAR SESIÓN
// ======================================================
//
// Endpoint:
// POST /api/logout
//
// Flask elimina el usuario de la sesión.
// Después volvemos al login.
// ======================================================


// Buscamos el botón de cerrar sesión.
//
// Este botón existe en:
// - tickets.html
// - tickets-formulario.html
//
// En login.html y registro.html no existe,
// por eso comprobamos primero si se ha encontrado.
const botonLogout = document.getElementById("boton-logout");


// Solo ejecutamos este código si el botón existe.
if (botonLogout) {

    // Escuchamos el clic sobre "Cerrar sesión".
    botonLogout.addEventListener("click", async function () {

        try {

            // Llamamos al endpoint del backend encargado
            // de eliminar la sesión del usuario.
            const respuesta = await fetch("/api/logout", {
                method: "POST"
            });


            // Nuestro backend devuelve 204 cuando
            // el logout se realiza correctamente.
            if (respuesta.ok) {

                // Una vez cerrada la sesión,
                // volvemos a la pantalla de login.
                window.location.href = "login.html";

                return;
            }


            // Si Flask responde con algún error inesperado,
            // lo mostramos en la consola.
            console.error(
                "No se ha podido cerrar la sesión."
            );

        } catch (error) {

            // Si no podemos comunicarnos con Flask,
            // mostramos el error técnico en la consola.
            console.error(
                "Error al cerrar sesión:",
                error
            );
        }

    });
}

// ======================================================
// 4. CARGAR Y MOSTRAR LOS TICKETS DEL USUARIO
// ======================================================
//
// Endpoint:
// GET /api/items
//
// El backend devuelve solamente los tickets que pertenecen
// al usuario que tiene la sesión iniciada.
//
// Ejemplo de respuesta:
//
// [
//     {
//         "id": 1,
//         "title": "Problema con la VPN",
//         "text": "No puedo conectarme",
//         "category": "Red",
//         "priority": "Alta",
//         "status": "Abierta"
//     }
// ]
//
// ======================================================


// Buscamos el contenedor de tickets.
//
// Este elemento solamente existe en tickets.html:
//
// <section id="lista-incidencias">
//
const listaIncidencias = document.getElementById("lista-incidencias");


// Si existe, significa que estamos en tickets.html.
if (listaIncidencias) {

    // Llamamos a la función que carga los tickets.
    cargarTickets();
}



// ======================================================
// FUNCIÓN cargarTickets()
// ======================================================
//
// Esta función:
// 1. Hace GET /api/items.
// 2. Comprueba que el usuario tenga sesión.
// 3. Recibe los tickets.
// 4. Los muestra en la página.
//
async function cargarTickets() {

    try {

        // Pedimos al backend los tickets del usuario conectado.
        const respuesta = await fetch("/api/items");


        // --------------------------------------------------
        // USUARIO SIN SESIÓN
        // --------------------------------------------------

        // Si Flask devuelve 401 significa que el usuario
        // no ha iniciado sesión.
        if (respuesta.status === 401) {

            // Lo enviamos al login.
            window.location.href = "login.html";

            return;
        }


        // --------------------------------------------------
        // OTRO ERROR
        // --------------------------------------------------

        // Si ocurre cualquier otro error HTTP:
        if (!respuesta.ok) {

            console.error(
                "Error al obtener las incidencias."
            );

            return;
        }


        // --------------------------------------------------
        // CONVERTIR RESPUESTA JSON
        // --------------------------------------------------

        // Flask devuelve una lista JSON.
        //
        // Con .json() la convertimos en un array JavaScript.
        const tickets = await respuesta.json();


        // Limpiamos el listado antes de introducir los tickets.
        listaIncidencias.innerHTML = "";


        // --------------------------------------------------
        // USUARIO SIN TICKETS
        // --------------------------------------------------

        if (tickets.length === 0) {

            const mensaje = document.createElement("p");

            mensaje.textContent =
                "Todavía no tienes ninguna incidencia.";

            listaIncidencias.appendChild(mensaje);

            return;
        }


        // --------------------------------------------------
        // MOSTRAR CADA TICKET
        // --------------------------------------------------

        // Recorremos todos los tickets recibidos.
        tickets.forEach(function (ticket) {

            // Creamos la tarjeta principal.
            const tarjeta = document.createElement("article");

            tarjeta.className = "tarjeta-incidencia";


            // ----------------------------------------------
            // ZONA DE DATOS
            // ----------------------------------------------

            const datos = document.createElement("div");

            datos.className = "datos-incidencia";


            // Título del ticket.
            const titulo = document.createElement("h2");

            titulo.className = "titulo-incidencia";

            // Usamos textContent en lugar de meter HTML directamente.
            //
            // Así el texto introducido por el usuario se trata como
            // texto y no como código HTML.
            titulo.textContent = ticket.title;


            // Contenedor de las etiquetas.
            const etiquetas = document.createElement("div");

            etiquetas.className = "etiquetas-incidencia";


            // ----------------------------------------------
            // ESTADO
            // ----------------------------------------------

            const estado = document.createElement("span");

            estado.className =
                "etiqueta " + obtenerClaseEstado(ticket.status);

            estado.textContent =
                "Estado: " + ticket.status;


            // ----------------------------------------------
            // PRIORIDAD
            // ----------------------------------------------

            const prioridad = document.createElement("span");

            prioridad.className =
                "etiqueta " + obtenerClasePrioridad(ticket.priority);

            prioridad.textContent =
                "Prioridad: " + ticket.priority;


            // ----------------------------------------------
            // CATEGORÍA
            // ----------------------------------------------

            const categoria = document.createElement("span");

            categoria.className =
                "etiqueta categoria-incidencia";

            categoria.textContent =
                "Categoría: " + ticket.category;


            // Metemos las etiquetas dentro de su contenedor.
            etiquetas.appendChild(estado);

            etiquetas.appendChild(prioridad);

            etiquetas.appendChild(categoria);


            // Metemos título y etiquetas en la zona de datos.
            datos.appendChild(titulo);

            datos.appendChild(etiquetas);


            // ----------------------------------------------
            // BOTONES
            // ----------------------------------------------

            const acciones = document.createElement("div");

            acciones.className = "acciones-incidencia";


            // Botón Editar.
            const botonEditar = document.createElement("a");

            botonEditar.className =
                "boton boton-secundario boton-pequeno";

            botonEditar.textContent = "Editar";

            // Ejemplo:
            //
            // tickets-formulario.html?id=3
            //
            botonEditar.href =
                "tickets-formulario.html?id=" + ticket.id;


            // Botón Eliminar.
            //
            // Todavía NO vamos a programar su funcionamiento.
            const botonEliminar = document.createElement("button");

            botonEliminar.type = "button";

            botonEliminar.className =
                "boton boton-peligro boton-pequeno";

            botonEliminar.textContent = "Eliminar";


            // Añadimos los botones.
            acciones.appendChild(botonEditar);

            acciones.appendChild(botonEliminar);


            // ----------------------------------------------
            // CONSTRUIR TARJETA COMPLETA
            // ----------------------------------------------

            tarjeta.appendChild(datos);

            tarjeta.appendChild(acciones);


            // Finalmente metemos la tarjeta dentro
            // del listado de incidencias.
            listaIncidencias.appendChild(tarjeta);

        });

    } catch (error) {

        console.error(
            "Error al cargar las incidencias:",
            error
        );
    }
}



// ======================================================
// CLASE CSS SEGÚN ESTADO
// ======================================================

function obtenerClaseEstado(estado) {

    if (estado === "Abierta") {
        return "estado-abierta";
    }

    if (estado === "En progreso") {
        return "estado-en-progreso";
    }

    if (estado === "Resuelta") {
        return "estado-resuelta";
    }

    if (estado === "Cerrada") {
        return "estado-cerrada";
    }

    return "";
}



// ======================================================
// CLASE CSS SEGÚN PRIORIDAD
// ======================================================

function obtenerClasePrioridad(prioridad) {

    if (prioridad === "Baja") {
        return "prioridad-baja";
    }

    if (prioridad === "Media") {
        return "prioridad-media";
    }

    if (prioridad === "Alta") {
        return "prioridad-alta";
    }

    if (prioridad === "Crítica") {
        return "prioridad-critica";
    }

    return "";
}

// ======================================================
// 5. CREAR UNA INCIDENCIA
// ======================================================
//
// Este código trabaja con el formulario que existe en:
//
// tickets-formulario.html
//
// Cuando estamos creando un ticket nuevo utilizaremos:
//
// POST /api/items
//
// Flask espera recibir:
//
// {
//     "title": "...",
//     "text": "...",
//     "category": "...",
//     "priority": "..."
// }
//
// El estado NO lo enviamos al crear el ticket porque
// nuestro backend establece automáticamente:
//
// status = "Abierta"
//
// ======================================================


// Buscamos el formulario de creación/edición de tickets.
//
// Si estamos en otra página, como tickets.html,
// este elemento no existe y formTicket será null.
const formTicket = document.getElementById("form-ticket");


// Solo ejecutamos este código si estamos realmente
// en tickets-formulario.html.
if (formTicket) {

    // Escuchamos cuándo el usuario pulsa el botón "Guardar".
    formTicket.addEventListener("submit", async function (evento) {

        // Evitamos que el navegador envíe el formulario
        // de la forma tradicional y recargue la página.
        evento.preventDefault();


        // --------------------------------------------------
        // RECOGER DATOS DEL FORMULARIO
        // --------------------------------------------------

        // Obtenemos el título introducido por el usuario.
        const title =
            document.getElementById("titulo").value;


        // Obtenemos la descripción.
        //
        // En nuestro backend este campo se llama "text".
        const text =
            document.getElementById("descripcion").value;


        // Obtenemos la categoría seleccionada.
        const category =
            document.getElementById("categoria").value;


        // Obtenemos la prioridad.
        const priority =
            document.getElementById("prioridad").value;


        // Caja donde mostraremos posibles errores.
        const mensajeError =
            document.getElementById("mensaje-error");


        // Ocultamos posibles errores anteriores.
        mensajeError.classList.add("oculto");


        // --------------------------------------------------
        // COMUNICACIÓN CON FLASK
        // --------------------------------------------------

        try {

            // Enviamos una petición POST al endpoint
            // encargado de crear tickets.
            const respuesta = await fetch("/api/items", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                // Convertimos los datos del formulario
                // en JSON.
                body: JSON.stringify({

                    title: title,

                    text: text,

                    category: category,

                    priority: priority

                })

            });


            // --------------------------------------------------
            // USUARIO SIN SESIÓN
            // --------------------------------------------------

            // Si Flask responde 401 significa que la sesión
            // no existe o ha caducado.
            if (respuesta.status === 401) {

                // Mandamos al usuario nuevamente al login.
                window.location.href = "login.html";

                return;
            }


            // --------------------------------------------------
            // TICKET CREADO CORRECTAMENTE
            // --------------------------------------------------

            // Nuestro backend devuelve 201 cuando crea
            // correctamente una incidencia.
            if (respuesta.status === 201) {

                // Una vez creado el ticket volvemos
                // al listado de incidencias.
                window.location.href = "tickets.html";

                return;
            }


            // --------------------------------------------------
            // ERROR AL CREAR EL TICKET
            // --------------------------------------------------

            // Si Flask responde, por ejemplo:
            //
            // 400 Bad Request
            //
            // intentamos leer el mensaje de error.
            const datos = await respuesta.json();


            mensajeError.textContent =
                datos.error ||
                "No se ha podido crear la incidencia.";


            // Mostramos el mensaje.
            mensajeError.classList.remove("oculto");


        } catch (error) {

            // Este bloque se ejecutará si hay algún problema
            // comunicándose con Flask.

            mensajeError.textContent =
                "No se ha podido conectar con el servidor.";


            mensajeError.classList.remove("oculto");


            console.error(
                "Error al crear la incidencia:",
                error
            );
        }

    });
}