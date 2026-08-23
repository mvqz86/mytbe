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

## Configuracion

1. Habilitar *YouTube Data API v3* en Google Cloud y crear una **clave de API**
   (datos publicos, no OAuth).
2. Abrir la app y tocar **clave** arriba a la derecha.

La clave queda solo en el navegador; no esta en el codigo.
Cuota: ~100 busquedas por dia.
