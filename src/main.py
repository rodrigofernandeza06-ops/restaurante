from __future__ import annotations
import sys
from pathlib import Path

def _ensure_src_on_path() -> None:
    src_dir = Path(__file__).resolve().parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

_ensure_src_on_path()

from core.game import Game  # noqa: E402

def main() -> None:
    Game().run()

if __name__ == "__main__":
    main()
