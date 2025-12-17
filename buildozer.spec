[app]
title = Restaurante Tycoon
package.name = restaurante
package.domain = org.pampeno
source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,json,wav,ogg,ttf,txt,md
source.exclude_dirs = .venv,__pycache__,build,bin,dist,.git,.vscode
version = 0.1.0
requirements = python3,pygame
# OJO: pygame en Android a veces falla compilación según tu entorno.
# Si falla, la alternativa estable es portar entrada a Kivy (sin cambiar la lógica).
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.archs = arm64-v8a,armeabi-v7a
# Bootstrap SDL2 es el más compatible con pygame en python-for-android
p4a.bootstrap = sdl2
# Ventana
orientation = landscape
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
