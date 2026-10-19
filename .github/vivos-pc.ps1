# Averigua los vivos de vivos-canales.json desde esta PC y sube vivos.json.
#
# Existe porque YouTube le contesta "no esta al aire" a los servidores de
# GitHub, y a una PC comun le dice cual es el vivo. Lo corre una tarea
# programada de Windows ("mytbe vivos").
#
# Trabaja sobre una copia aparte del repo, en AppData\Local\mytbe-vivos, para
# no tocar nunca lo que este a medio hacer en la carpeta de trabajo.

$ErrorActionPreference = 'Stop'
$git    = 'C:\Program Files\Git\cmd\git.exe'
$python = 'C:\Users\mvqz8\AppData\Local\Programs\Python\Python311\python.exe'
$copia  = Join-Path $env:LOCALAPPDATA 'mytbe-vivos'
$log    = Join-Path $copia '..\mytbe-vivos.log'

function Anotar($t){ "$(Get-Date -Format 'yyyy-MM-dd HH:mm') $t" | Add-Content -Path $log -Encoding utf8 }

try {
  if(-not (Test-Path (Join-Path $copia '.git'))){
    & $git clone -q https://github.com/mvqz86/mytbe.git $copia
  }
  Set-Location $copia
  & $git fetch -q origin
  & $git reset -q --hard origin/main

  $env:PYTHONIOENCODING = 'utf-8'
  $salida = & $python .github/vivos.py 2>&1 | Out-String
  Anotar ($salida.Trim() -replace "`r?`n", ' | ')

  if(& $git status --porcelain vivos.json){
    & $git add vivos.json
    & $git commit -q -m 'Vivos de la multivista'
    & $git push -q origin HEAD:main
    Anotar 'subido'
  }
} catch {
  Anotar "ERROR $($_.Exception.Message)"
  exit 1
}
