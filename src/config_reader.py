# src/config_reader.py
import yaml

def read_inputs_yaml(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            y = yaml.safe_load(f) or {}
        return (y.get("defaults") or {}) if isinstance(y, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception:
        # fallback to empty; run.py prints what it uses
        return {}
