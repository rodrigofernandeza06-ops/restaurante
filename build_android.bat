\
@echo off
setlocal enabledelayedexpansion

REM =============================================================
REM build_android.bat
REM Genera APK (debug) usando WSL2 + Ubuntu + Buildozer.
REM
REM IMPORTANTE:
REM 1) Evita carpetas con "ñ", espacios raros o símbolos. 
REM    Recomendado: C:\android_build\restaurant_game
REM 2) La primera vez puede tardar MUCHO (descargas SDK/NDK/Gradle).
REM 3) Si Buildozer falla con pygame, la alternativa estable es portar UI a Kivy.
REM =============================================================

echo [INFO] Verificando WSL...
where wsl >nul 2>&1
if errorlevel 1 (
  echo [ERROR] No tienes WSL instalado. Instala con: wsl --install -d Ubuntu
  pause
  exit /b 1
)

REM Carpeta de build ASCII (sin ñ)
set BUILD_ROOT=C:\android_build\restaurant_game
set SRC_DIR=%~dp0

echo [INFO] Copiando proyecto a %BUILD_ROOT% (sin .venv / cache) ...
if exist "%BUILD_ROOT%" rmdir /s /q "%BUILD_ROOT%"
mkdir "%BUILD_ROOT%"

REM robocopy devuelve codigos >0 aunque sea OK, por eso no lo tratamos como error fatal
robocopy "%SRC_DIR%" "%BUILD_ROOT%" /E /XD ".venv" "__pycache__" "build" "bin" "dist" ".git" ".vscode" >nul

echo [INFO] Preparando Ubuntu + Buildozer dentro de WSL...
REM Nota: usamos bash -lc para correr todo en una sola sesión
wsl bash -lc "set -e; \
  sudo apt update -y; \
  sudo apt install -y python3 python3-pip git zip openjdk-17-jdk build-essential \
    libffi-dev libssl-dev libsqlite3-dev zlib1g-dev libbz2-dev libreadline-dev libncurses5-dev \
    libgdbm-dev liblzma-dev libstdc++6 libgl1-mesa-dev libgles2-mesa-dev; \
  python3 -m pip install --user --upgrade pip; \
  python3 -m pip install --user buildozer cython; \
  cd /mnt/c/android_build/restaurant_game; \
  ~/.local/bin/buildozer -v android debug"

if errorlevel 1 (
  echo [ERROR] Fallo la compilacion. Mira el log arriba.
  echo         Tipico: dependencias de pygame. Si pasa, te doy el plan B (Kivy UI).
  pause
  exit /b 1
)

echo.
echo [OK] APK generado. Busca en:
echo      %BUILD_ROOT%\bin\
echo.
pause
