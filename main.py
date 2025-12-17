# main.py (root)
# Entrypoint compatible con buildozer/python-for-android.
# En Windows seguimos usando: python -m src.main
from __future__ import annotations

def main() -> None:
    from src.main import main as app_main
    app_main()

if __name__ == "__main__":
    main()
