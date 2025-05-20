from .shared_config_loader import load_config
from pathlib import Path
from datetime import datetime

# Load vault configuration
cfg = load_config()
vault_root = Path(cfg["vault_root"])
projects_dir = vault_root / cfg["projects_folder"]

# Simulate a project name
project_name = "web_portfolio"

# Create summary file
summary_file = projects_dir / f"{project_name}.md"
summary_content = f"""# 🌐 Project: {project_name.replace('_', ' ').title()}

**Overview:**  
Cyberpunk-themed portfolio website with AI integration and custom HTML/CSS.

**Created:** {datetime.now().strftime('%Y-%m-%d')}

**Path:** proxmox-homelab/{project_name}/
"""

projects_dir.mkdir(parents=True, exist_ok=True)
summary_file.write_text(summary_content.strip(), encoding='utf-8')

print(f"✅ Updated summary: {summary_file}")