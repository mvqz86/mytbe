# mytbe

Interfaz previa a YouTube: busca, guarda en carpetas y dispara links,
sin suscribirse a canales ni activar el historial de la cuenta.

Pensada para lanzar radios en vivo como transmision de fondo.

## Como funciona

- Las busquedas van por la **YouTube Data API v3** con una clave propia,
  anonima: no pasan por tu cuenta y no alimentan tus recomendaciones.
- Las carpetas viven en el navegador (`localStorage`), no en Google.
- Al tocar un item se abre YouTube y reproduce ahi.

## Arriba a la derecha

Cuatro iconos, con el nombre en el tooltip: **luna/sol** cambia el tema,
**llave** es la clave de la API, **muñeco** es el perfil y **engranaje** abre
la configuracion, que es donde viven el respaldo y la sincronizacion. Cuando
la sincronizacion falla, el engranaje lleva un punto rojo.

## Resultados

Se piden 50 por busqueda y se ordenan **de mas reproducciones a menos**. Cada
uno muestra su duracion y cuantas veces se vio. Ninguno de los dos datos viene
con la busqueda: los dos salen de un pedido aparte a `videos.list`, que cuesta
1 unidad para los 50 juntos. Si ese pedido falla, los resultados se muestran
igual, sin numeros y en el orden de la API. Un vivo no lleva duracion: la API
la devuelve como `P0D`, que no es un largo sino "esto todavia no termino".

Los titulos de la API vienen escapados como HTML (`&quot;`, `&amp;`), asi que
se desarman antes de mostrarlos y antes de guardarlos.

## Modo lista

YouTube arma una lista temporal al vuelo con `watch_videos?video_ids=A,B,C`:
contesta un redirect a `watch?v=A&list=TLGG...` y de ahi en mas encadena solo,
con su propio reproductor. No hace falta ningun temporizador —una pagina en
segundo plano no puede abrir otra app ni tiene timers confiables— ni gasta
cuota: es una direccion.

- **▶** en el encabezado de una carpeta reproduce esa carpeta entera.
- **▶ reproducir**, en el pie, reproduce todo lo que se ve, en ese orden. Con
  el filtro puesto, reproduce lo filtrado: se arma una lista escribiendo tres
  letras.
- El boton **playlist**, al lado de *en vivo*, prende el modo de armado: las
  filas dejan de disparar y se marcan con un toque, numeradas en el orden en
  que las tocaste, que es el orden en que van a sonar. Vale mezclar carpetas,
  solapas y hasta lo que quedo en Recientes, y el filtro sigue andando
  mientras marcas: buscas, marcas, borras el filtro, buscas otra cosa y marcas
  de nuevo.
- Arriba aparece una barra con lo que llevas elegido y dos botones:
  **reproducir**, que lo manda entero a YouTube, y **guardar**, que lo deja
  como un item con nombre propio en la solapa o carpeta que elijas. Despues se
  toca y suena todo seguido.

Las radios quedan afuera: son canales y no tienen un id de video estable. El
tope es de unos 50 por lista; si hay mas, van los primeros 50 y se avisa. La
lista no queda guardada en la cuenta de YouTube.

En Android, una lista se abre en el navegador en vez de la app: watch_videos
es un redirect que el navegador sigue siempre y la app no necesariamente.

## Radios

Una radio se guarda como **canal**, no como video: el ID de un stream
muere cada vez que la transmision se reinicia. El boton apunta a
`youtube.com/channel/<ID>/live`, que siempre resuelve a lo que este al aire.

## Recientes

Lo que disparas queda anotado tres dias en la pestana **Recientes**, con su
miniatura y su hora. Es para volver a algo que pusiste ayer y no llegaste a
guardar, sin gastar otra busqueda. De un vivo se anota el canal, no el video.

## Solapas, carpetas y subcarpetas

Tres niveles con tres nombres, y el mismo nombre en toda la app:

- **Solapa**: las de arriba (Radios, Documentales, Musica). Se crean con el
  **+** de la fila de solapas.
- **Carpeta**: adentro de una solapa. Se crea desde el pie del panel, o con el
  **+** de la solapa en el cuadro de guardar.
- **Subcarpeta**: adentro de una carpeta, a cualquier profundidad. Se crea con
  el **+** del encabezado de ese grupo, o con el **+** de esa fila en el
  cuadro de guardar.

Por dentro son todas lo mismo: una lista plana donde cada una recuerda a su
madre. El nombre sale de que tan adentro esta, no de un campo aparte.

## Guardar

El cuadro de guardar muestra el **arbol** completo. Cada fila tiene tres
blancos distintos, de 34 de alto para no pisarse con el pulgar:

- el **triangulo** abre y cierra esa rama, y queda como la dejaste;
- el **nombre** guarda ahi;
- el **+** crea un nivel mas adentro y guarda ahi mismo: si la estas creando
  en ese momento es porque lo que tenes en la mano va adentro.

Abajo de todo, *+ solapa nueva*.

### Como se ve una carpeta

Hay una sola vista y es la lista. Todo lo que cuelga de la carpeta aparece de
una tirada y cada subcarpeta es un encabezado, que se queda pegado arriba
mientras se scrollea, en vez de un lugar al que entrar y del que volver.

- Los grupos se pliegan de a uno con un toque y quedan asi para la proxima.
- Cuando hay mas de seis elementos aparece un campo para filtrar por titulo o
  canal, sin tildes ni mayusculas: "clasica" encuentra "Clásica". Mira solo lo
  guardado, no toca internet.
- Con el filtro puesto los grupos plegados se abren solos: si escribiste algo,
  lo que buscas no puede quedar escondido.
- Lo suelto de la propia carpeta va al final, en su propio grupo.
- *Ordenar* mueve cada cosa dentro de su grupo, con flechas.
- Una carpeta sin subcarpetas se ve como una lista comun, sin encabezados.

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
2. Abrir la app y tocar la **llave** arriba a la derecha.

La clave queda solo en el navegador; no esta en el codigo.
Cuota: ~100 busquedas por dia.
