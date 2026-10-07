import json
from pathlib import Path


CONFIG_FILE = Path(__file__).parent / "config.json"


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    config = load_config()

    print(json.dumps(
        config,
        indent=2,
        ensure_ascii=False
    ))
