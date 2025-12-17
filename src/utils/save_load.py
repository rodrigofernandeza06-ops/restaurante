from __future__ import annotations
import json
from utils.paths import project_root

def load_json(rel_path: str, default: dict | None = None) -> dict:
    p = project_root() / rel_path
    if not p.exists():
        return default or {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default or {}

def save_json(rel_path: str, data: dict) -> None:
    p = project_root() / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
