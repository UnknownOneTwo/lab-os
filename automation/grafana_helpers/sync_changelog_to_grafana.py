import sys
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent))
from shared_config_loader import load_config

# Load configuration
load_dotenv()
cfg = load_config()

vault_root = Path(cfg["vault_root"])
changelog_file = vault_root / cfg["changelog_path"]

# Load content
changelog_md = changelog_file.read_text(encoding='utf-8')

# Env values
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://192.168.10.102:3000")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY")
DASHBOARD_UID = "femc0eni2fb40a"
PANEL_ID = 102  # 📝 Changelog

if not GRAFANA_API_KEY:
    print("❌ Missing GRAFANA_API_KEY in environment.")
    sys.exit(1)

# Step 1: Get current dashboard
headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json"
}
res = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}", headers=headers)
if res.status_code != 200:
    print(f"❌ Failed to fetch dashboard: {res.status_code} – {res.text}")
    sys.exit(1)

dashboard_data = res.json()
dashboard = dashboard_data["dashboard"]

# Step 2: Update panel content
panel_found = False
for panel in dashboard["panels"]:
    if panel["id"] == PANEL_ID:
        panel["options"]["content"] = changelog_md
        panel_found = True
        break

if not panel_found:
    print(f"❌ Panel ID {PANEL_ID} not found in dashboard.")
    sys.exit(1)

# Step 3: Push updated dashboard
update_payload = {
    "dashboard": dashboard,
    "folderId": dashboard_data["meta"]["folderId"],
    "overwrite": True
}
put_res = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=headers, json=update_payload)

if put_res.status_code == 200:
    print("✅ Changelog successfully synced to Grafana.")
else:
    print(f"❌ Failed to update Grafana: {put_res.status_code} – {put_res.text}")