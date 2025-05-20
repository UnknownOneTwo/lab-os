import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from shared_config_loader import load_config
from datetime import datetime

# Load config
cfg = load_config()
vault_root = Path(cfg["vault_root"])
projects_dir = vault_root / cfg["projects_folder"]

# Project name
project_name = "web_portfolio"
summary_file = projects_dir / f"{project_name}.md"

# Content
summary_content = f"""# 🌐 Project: {project_name.replace('_', ' ').title()}

**Overview:**  
Cyberpunk-themed portfolio website with AI integration and custom HTML/CSS.

**Created:** {datetime.now().strftime('%Y-%m-%d')}

**Path:** proxmox-homelab/{project_name}/
"""

projects_dir.mkdir(parents=True, exist_ok=True)
summary_file.write_text(summary_content.strip(), encoding='utf-8')

print(f"✅ Updated summary: {summary_file}")