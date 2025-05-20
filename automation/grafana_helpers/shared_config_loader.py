import json
from pathlib import Path

# Load shared configuration
CONFIG_PATH = Path(__file__).parent / "obsidian_helpers_config.json"

def load_config():
    with CONFIG_PATH.open("r") as f:
        return json.load(f)

cfg = load_config()

# You can now use cfg["vault_root"], cfg["projects_folder"], etc.
vault_root = Path(cfg["vault_root"])
projects_dir = vault_root / cfg["projects_folder"]
changelog_path = vault_root / cfg["changelog_path"]

# Now your scripts are consistent across helpers