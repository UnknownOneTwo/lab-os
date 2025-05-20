import requests
import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# === CONFIGURATION ===
GRAFANA_URL = "http://192.168.10.102:3000"  # Update if needed
DASHBOARD_UID = "dem0v6zlwt7nkb"
PANEL_ID = 2  # 📝 Changelog panel
API_KEY = f"Bearer {os.getenv('GRAFANA_API_KEY')}"
print(f"🔍 Loaded API Key (first 10 chars): {os.getenv('GRAFANA_API_KEY')[:10]}")

CHANGELOG_PATH = "vault/CHANGELOG.md"

# === LOAD MOST RECENT SECTION ONLY ===
def extract_latest_entry(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    entries = content.strip().split("\n## ")
    if len(entries) < 2:
        return content  # fallback: entire file

    latest = "## " + entries[-1].strip()
    return latest

if not os.path.exists(CHANGELOG_PATH):
    print(f"❌ File not found: {CHANGELOG_PATH}")
    exit(1)

latest_entry = extract_latest_entry(CHANGELOG_PATH)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
markdown = f"## 📅 Last Sync: {timestamp}\n\n{latest_entry}"

# === FETCH DASHBOARD JSON ===
headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}
response = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}", headers=headers)
if response.status_code != 200:
    print(f"❌ Failed to fetch dashboard: {response.status_code} {response.text}")
    exit(1)

dashboard = response.json()["dashboard"]

# === UPDATE PANEL CONTENT ===
found = False
for panel in dashboard["panels"]:
    if panel["id"] == PANEL_ID:
        panel["options"]["content"] = markdown
        found = True
        break

if not found:
    print(f"❌ Panel ID {PANEL_ID} not found in dashboard UID {DASHBOARD_UID}")
    exit(1)

# === PUSH BACK TO GRAFANA ===
payload = {
    "dashboard": dashboard,
    "folderId": 0,
    "overwrite": True
}
push = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=headers, json=payload)

if push.status_code == 200:
    print("✅ Changelog updated in Grafana successfully!")
else:
    print(f"❌ Failed to update Grafana: {push.status_code} {push.text}")
