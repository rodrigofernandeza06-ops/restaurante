@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creando entorno virtual .venv ...
  py -3.12 -m venv .venv
  if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual. Verifica Python 3.12+.
    pause
    exit /b 1
  )
)

call ".venv\Scripts\activate"
echo [INFO] Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [INFO] Ejecutando juego...
python -m src.main
pause
