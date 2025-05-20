import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from shared_config_loader import load_config
from datetime import datetime

cfg = load_config()
vault_root = Path(cfg["vault_root"])
logs_folder = vault_root / cfg["logs_folder"]
logs_folder.mkdir(parents=True, exist_ok=True)

index_file = logs_folder / "onedrive_file_index.log"
index_content = f"""# OneDrive File Index
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
[Placeholder for OneDrive file path indexing results]
"""

index_file.write_text(index_content.strip(), encoding='utf-8')
print(f"✅ Generated index log: {index_file}")