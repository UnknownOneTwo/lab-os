from datetime import datetime
from pathlib import Path

now = datetime.now()
timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

# Create badge markdown with timestamp
badge = f"![Last Sync](https://img.shields.io/badge/last--sync-{timestamp.replace(' ', '--').replace(':', '%3A')}-blue?style=flat-square&logo=grafana)"

# Save to file
badge_path = Path("automation/grafana_helpers/last_sync_status.md")
badge_path.parent.mkdir(parents=True, exist_ok=True)
badge_path.write_text(badge)

print(f"✅ Badge written to: {badge_path}")