"""Averigua que video esta al aire en cada canal de vivos-canales.json y lo
deja en vivos.json, que la Multivista lee desde el sitio. Lo corre la PC
(vivos-pc.ps1): a los servidores de GitHub YouTube les contesta que no hay
nada al aire.

Existe porque algunos canales (CNN, La Nacion) no se dejan reproducir con el
reproductor por canal, y la API no encuentra su vivo. La pagina /live del
canal si lo dice, en el canonical, pero un navegador no puede leerla desde
otra web. Este script si.
"""
import datetime, json, re, sys, urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126 Safari/537.36')

canales = json.load(open('vivos-canales.json', encoding='utf-8'))
try:
    viejo = json.load(open('vivos.json', encoding='utf-8'))
except Exception:
    viejo = {}

vivos, problemas = {}, []
for x in canales:
    req = urllib.request.Request('https://www.youtube.com/channel/%s/live' % x['c'],
                                 headers={'User-Agent': UA, 'Accept-Language': 'es-AR,es;q=0.9',
                                          'Cookie': 'CONSENT=YES+1'})
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    except Exception as e:
        problemas.append('%s: %s' % (x['t'], e)); continue
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    v = canon and re.search(r'watch\?v=([\w-]{11})', canon.group(1))
    if v:
        vivos[x['c']] = v.group(1)
        print('%-20s %s' % (x['t'], v.group(1)))
    else:
        # Sin canonical a un video: o no esta al aire, o YouTube nos freno.
        # Se anota que vio, para poder distinguir una cosa de la otra.
        titulo = re.search(r'<title>([^<]*)', html)
        motivo = ('canonical al canal: no esta al aire' if canon
                  else 'sin canonical; titulo: %s' % (titulo.group(1)[:80] if titulo else '-'))
        problemas.append('%s: %s' % (x['t'], motivo))
        # Una corrida que falla no borra lo que se sabia: el vivo de un canal de
        # 24 horas suele seguir siendo el mismo.
        if viejo.get('vivos', {}).get(x['c']):
            vivos[x['c']] = viejo['vivos'][x['c']]

for p in problemas:
    print('AVISO', p)

if vivos == viejo.get('vivos') and problemas == viejo.get('avisos'):
    print('sin cambios'); sys.exit(0)
json.dump({'vivos': vivos, 'avisos': problemas,
           'actualizado': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')},
          open('vivos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('vivos.json actualizado')
