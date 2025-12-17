from __future__ import annotations

_STRINGS = {
    "es": {
        "title": "Restaurante Tycoon — MVP",
        "menu_play": "JUGAR",
        "menu_options": "OPCIONES",
        "menu_exit": "SALIR",
        "options_title": "OPCIONES",
        "opt_language": "Idioma",
        "opt_difficulty": "Dificultad",
        "opt_music": "Música",
        "opt_volume": "Volumen",
        "opt_brightness": "Brillo",
        "opt_accent": "Color",
        "opt_back": "Volver",
        "no_interact": "No hay nada para interactuar.",
        "inv_empty": "Inventario vacío.",
        "inv_drop_all": "Soltaste todo el inventario.",
        "wrong_order": "Pedido incorrecto",
        "no_customer": "No hay cliente.",
        "no_plate": "No tienes un plato listo.",
        "correct": "¡Entrega correcta!",
        "need_ing": "Faltan ingredientes para una receta.",
        "arrived": "Llegó cliente",
    },
    "en": {
        "title": "Restaurant Tycoon — MVP",
        "menu_play": "PLAY",
        "menu_options": "OPTIONS",
        "menu_exit": "EXIT",
        "options_title": "OPTIONS",
        "opt_language": "Language",
        "opt_difficulty": "Difficulty",
        "opt_music": "Music",
        "opt_volume": "Volume",
        "opt_brightness": "Brightness",
        "opt_accent": "Color",
        "opt_back": "Back",
        "no_interact": "Nothing to interact.",
        "inv_empty": "Inventory empty.",
        "inv_drop_all": "Dropped everything.",
        "wrong_order": "Wrong order",
        "no_customer": "No customer.",
        "no_plate": "No ready dish.",
        "correct": "Correct delivery!",
        "need_ing": "Missing ingredients.",
        "arrived": "Customer arrived",
    }
}

def t(lang: str, key: str) -> str:
    lang = (lang or "es").lower()
    if lang not in _STRINGS:
        lang = "es"
    return _STRINGS[lang].get(key, key)
