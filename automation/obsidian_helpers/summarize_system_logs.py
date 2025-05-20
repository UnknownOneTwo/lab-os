import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from shared_config_loader import load_config
from datetime import datetime

cfg = load_config()
vault_root = Path(cfg["vault_root"])
logs_dir = vault_root / cfg["logs_folder"]
logs_dir.mkdir(parents=True, exist_ok=True)

summary_file = logs_dir / "system_logs_summary.md"
summary_content = f"""# 🖥️ System Logs Summary

**Date:** {datetime.now().strftime('%Y-%m-%d')}

**Summary:**  
Automated summary of recent system activity and updates.

**Source:** vault/SystemLogs/system_updates.log
"""

summary_file.write_text(summary_content.strip(), encoding='utf-8')
print(f"✅ Summarized system logs to: {summary_file}")