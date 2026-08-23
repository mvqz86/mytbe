# mytbe

Interfaz previa a YouTube: busca, guarda en carpetas y dispara links,
sin suscribirse a canales ni activar el historial de la cuenta.

Pensada para lanzar radios en vivo como transmision de fondo.

## Como funciona

- Las busquedas van por la **YouTube Data API v3** con una clave propia,
  anonima: no pasan por tu cuenta y no alimentan tus recomendaciones.
- Las carpetas viven en el navegador (`localStorage`), no en Google.
- Al tocar un item se abre YouTube y reproduce ahi.

## Radios

Una radio se guarda como **canal**, no como video: el ID de un stream
muere cada vez que la transmision se reinicia. El boton apunta a
`youtube.com/channel/<ID>/live`, que siempre resuelve a lo que este al aire.

## Recientes

Lo que disparas queda anotado tres dias en la pestana **Recientes**, con su
miniatura y su hora. Es para volver a algo que pusiste ayer y no llegaste a
guardar, sin gastar otra busqueda. De un vivo se anota el canal, no el video.

## Carpetas y subcarpetas

Las pestanas de arriba son las carpetas de primer nivel. Adentro de cualquiera
se pueden crear subcarpetas —*subcarpeta nueva*, en el pie del panel— y
anidarlas cuanto haga falta. Las subcarpetas aparecen como filas con carpetita
al principio de la lista, con la cuenta de todo lo que llevan adentro, y un
rastro de migas arriba para volver.

Las de adentro no se suman a las pestanas: es lo que evita que la fila de
arriba crezca hasta que no se pueda leer. Con doce carpetas en una tablet solo
se veian tres y media.

Las carpetas siguen siendo una lista plana y cada una recuerda a su madre. Eso
mantiene simple la fusion entre dispositivos, que empareja por id.

### Vista lista

Una carpeta con subcarpetas puede verse de dos formas, y se acuerda de cual
elegiste: *vista: carpetas / lista*, en el pie del panel.

En **lista**, todo lo que cuelga de esa carpeta aparece de una sola tirada y
cada subcarpeta pasa a ser un encabezado, que se queda pegado arriba mientras
se scrollea. Los grupos se pliegan de a uno con un toque y quedan asi para la
proxima. Arriba hay un campo para filtrar por titulo o canal —sin tildes y sin
mayusculas, "clasica" encuentra "Clásica"— que solo mira lo que ya esta
guardado y no toca internet. Con el filtro puesto los grupos plegados se abren
solos: si escribiste algo, lo que buscas no puede quedar escondido.

Los elementos sueltos de la propia carpeta van al final, en su propio grupo.

## Perfiles

Dos personas en un mismo aparato, cada una con sus carpetas y sus recientes.
Se maneja desde **perfil**, arriba a la derecha.

No es un login: no hay servidor que valide nada. Es **cifrado real**. Un
perfil con contrasena guarda su JSON cifrado con AES-GCM y una llave derivada
con PBKDF2 (150.000 vueltas); sin la contrasena, en el navegador solo se ve
ruido. La llave vive en memoria mientras el perfil esta abierto y no se guarda
en ningun lado, asi que cerrar y volver la pide de nuevo.

Si se olvida la contrasena, esos datos no los recupera nadie.

Un perfil tambien puede no tener contrasena: se guarda en claro y entra
directo. Mientras haya un solo perfil sin contrasena, la app abre como
siempre y no pregunta nada.

La clave de la API es del aparato y la comparten los dos perfiles. El token de
sincronizacion, en cambio, vive adentro del perfil: si el perfil esta cifrado,
el token tambien.

## Sincronizacion entre dispositivos

Las carpetas y los recientes se pueden compartir entre la tablet, la compu y
el telefono usando un **gist privado** de tu cuenta de GitHub.

1. Crear un token clasico con el permiso `gist` y nada mas:
   github.com/settings/tokens -> *Generate new token (classic)* -> marcar solo
   **gist**.
2. En la app, pie de pagina: *sincronizacion -> configurar*, pegar el token y
   tocar **Conectar**. Si la cuenta todavia no tiene un gist de mytbe, se crea
   solo.
3. En los otros dispositivos, el **mismo token** en el mismo cuadro: la app
   busca en la cuenta y se engancha al gist que ya existe. Tambien sirve
   *Copiar enlace para otro dispositivo* y abrirlo alla una vez.

La fusion es por elemento y no por archivo: guardar en un dispositivo y
borrar en otro conviven sin pisarse, porque cada item lleva su hora y cada
borrado deja una marca. Sincroniza al abrir y unos segundos despues de cada
cambio.

El enlace del punto 3 lleva el token adentro: es comodo y es delicado, no lo
publiques ni lo dejes en un chat.

## Configuracion

1. Habilitar *YouTube Data API v3* en Google Cloud y crear una **clave de API**
   (datos publicos, no OAuth).
2. Abrir la app y tocar **clave** arriba a la derecha.

La clave queda solo en el navegador; no esta en el codigo.
Cuota: ~100 busquedas por dia.
