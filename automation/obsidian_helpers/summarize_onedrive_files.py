import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from shared_config_loader import load_config
from datetime import datetime

# Load config
cfg = load_config()
vault_root = Path(cfg["vault_root"])
projects_dir = vault_root / cfg["projects_folder"]

# Output summary
project_name = "onedrive_summary"
summary_file = projects_dir / f"{project_name}.md"
summary_content = f"""# 📂 Project: OneDrive File Summary

**Created:** {datetime.now().strftime('%Y-%m-%d')}

**Summary:**  
Automated summary of files extracted from OneDrive folder using AI tools (Ollama, Tesseract, etc.).

**Location:** C:/Users/Steve/OneDrive/
"""

projects_dir.mkdir(parents=True, exist_ok=True)
summary_file.write_text(summary_content.strip(), encoding='utf-8')

print(f"✅ Updated summary: {summary_file}")