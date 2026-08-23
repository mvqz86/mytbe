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
