import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from shared_config_loader import load_config

cfg = load_config()
vault_root = Path(cfg["vault_root"])
projects_dir = vault_root / cfg["projects_folder"]
index_file = projects_dir / "_Project_Index.md"

index_lines = ["# 📂 Project Index\n"]

for md_file in sorted(projects_dir.glob("*.md")):
    name = md_file.stem.replace("_", " ").title()
    rel_path = md_file.name
    index_lines.append(f"- [{name}](./{rel_path})")

index_file.write_text("\n".join(index_lines), encoding='utf-8')
print(f"✅ Generated project index at: {index_file}")