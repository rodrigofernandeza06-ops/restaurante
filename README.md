# Restaurante Tycoon — Niveles + Opciones (v3)

## Cambios (pedido)
- **Nivel 1** ahora termina en **200 puntos**.
- **Nivel 2**: más ingredientes + **más recetas (incluye recetas de 3 ingredientes)** + **2 estaciones de preparación extra** (3 en total).
- Se añadió fondo de **suelo**: `assets/images/floor.png` (tile).

## Ejecutar (Windows / VS Code)
```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```
O doble click: `run_game.bat`

## Android (APK - Debug) usando WSL2 + Buildozer (Windows)

Este proyecto es Python + Pygame. Para generar APK en Windows se usa **WSL2 (Ubuntu)** + **Buildozer**.

1) Instala WSL2 (PowerShell admin):
- `wsl --install -d Ubuntu`

2) En Windows, ejecuta:
- `build_android.bat`

El script copiará el proyecto a `C:\android_build\restaurant_game` (sin caracteres raros) y compilará el APK.

Salida:
- `C:\android_build\restaurant_game\bin\*.apk`

> Nota: Pygame en Android puede fallar compilación según entorno. Si falla, la alternativa estable es portar la capa de UI/ventana a **Kivy** manteniendo la lógica del juego.
