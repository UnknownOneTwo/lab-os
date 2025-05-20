import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
GRAFANA_URL = "http://192.168.10.102:3000"
SOURCE_UID = "dem0v6zlwt7nkb"
NEW_TITLE = "System Performance Monitor vNext"
GRAFANA_TOKEN = os.getenv("GRAFANA_API_KEY")
HEADERS = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
DATASOURCE_NAME = "influxDB"  # Confirmed Grafana datasource

# === Static Markdown for Server Overview ===
SERVER_OVERVIEW_MARKDOWN = """
# 🖥️ Proxmox Cluster Overview

## 🧩 Nodes

- **node-core-01**
  ▸ 🏷️ Role: Infrastructure  
  ▸ 💽 Disk: 1TB NVMe  
  ▸ 🧠 RAM: 62 GB  
  ▸ 🔌 IP: `192.168.10.100`  
  ▸ 📦 Services: InfluxDB, Grafana, Backups

- **node-game-01**
  ▸ 🏷️ Role: Game Server  
  ▸ 💽 Disk: 480 GB NVMe  
  ▸ 🧠 RAM: 31 GB  
  ▸ 🔌 IP: `192.168.10.200`  
  ▸ 🎮 Services: Minecraft (ATM10), Docker

---

## 🧠 AI Integration

- 🔎 **Ollama**: Local LLaMA3 (RTX 3080)  
- 📄 **Changelog**: Auto-generated from system summaries  
- 📊 **Grafana**: Powered by InfluxDB v1.11

---

## 🌐 Lab Infrastructure

- 🔐 Subnet: VLAN10 / `192.168.10.0/24`  
- 🔄 Versioning: GitHub + `vault/CHANGELOG.md`  
- 📋 Status updates: Triggered on AI summarization runs
"""

# === Panel Builder ===
def make_influx_panel(title, query, panel_id, grid_pos, unit="percent", panel_type="timeseries"):
    return {
        "datasource": DATASOURCE_NAME,
        "fieldConfig": {
            "defaults": {
                "unit": unit,
                "thresholds": {
                    "mode": "absolute",
                    "steps": [
                        {"color": "green", "value": None},
                        {"color": "yellow", "value": 70},
                        {"color": "red", "value": 90}
                    ],
                },
                "mappings": [],
            },
            "overrides": [],
        },
        "gridPos": grid_pos,
        "id": panel_id,
        "title": title,
        "type": panel_type,
        "targets": [{
            "refId": "A",
            "rawQuery": True,
            "query": query,
            "datasource": DATASOURCE_NAME,
        }],
    }

# === Get and Clone Dashboard ===
r = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/{SOURCE_UID}", headers=HEADERS)
r.raise_for_status()
dashboard = r.json()["dashboard"]

dashboard["title"] = NEW_TITLE
dashboard.pop("uid", None)
dashboard["id"] = None

existing_ids = [p["id"] for p in dashboard["panels"]]
next_id = max(existing_ids) + 100 if existing_ids else 100  # ✅ Safe ID range
overview_panel_id = next_id
metric_start_id = next_id + 1

# === Static Overview Panel ===
overview_panel = {
    "id": overview_panel_id,
    "type": "text",
    "title": "🖥️ Server Overview",
    "gridPos": {"x": 0, "y": 0, "w": 12, "h": 4},
    "options": {
        "mode": "markdown",
        "content": SERVER_OVERVIEW_MARKDOWN.strip()
    },
    "fieldConfig": {"defaults": {}, "overrides": []},
    "pluginVersion": "11.4.0"
}

# === Add Metric Panels
panels_to_add = [
    make_influx_panel("🔥 CPU Usage",
                      'SELECT mean("usage_user") FROM "cpu" WHERE time > now() - 5m',
                      metric_start_id, {"x": 0, "y": 4, "w": 6, "h": 6}),
    make_influx_panel("🧠 Memory Usage",
                      'SELECT last("used_percent") FROM "mem"',
                      metric_start_id+1, {"x": 6, "y": 4, "w": 6, "h": 6}),
    make_influx_panel("💽 Disk Usage (/)",
                      'SELECT last("used_percent") FROM "disk" WHERE "path" = "/"',
                      metric_start_id+2, {"x": 0, "y": 10, "w": 6, "h": 6}),
    make_influx_panel("🌐 Network In/Out",
                      'SELECT derivative(mean("bytes_recv"), 1s), derivative(mean("bytes_sent"), 1s) '
                      'FROM "net" WHERE "interface" = \'eno1\' AND time > now() - 10m GROUP BY time(10s)',
                      metric_start_id+3, {"x": 6, "y": 10, "w": 6, "h": 6}),
    make_influx_panel("⚙️ System Load (1m)",
                      'SELECT last("load1") FROM "system"',
                      metric_start_id+4, {"x": 0, "y": 16, "w": 12, "h": 4}),
]

dashboard["panels"].extend([overview_panel] + panels_to_add)

# === Build and Push Payload
payload = {
    "dashboard": dashboard,
    "folderId": 0,
    "message": f"Created {NEW_TITLE}",
    "overwrite": False
}

print("\n📦 Previewing JSON payload being sent to Grafana...\n")
print(json.dumps(payload, indent=2)[:5000])  # Truncated for display

try:
    response = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=HEADERS, json=payload)
    response.raise_for_status()
    new_uid = response.json()["uid"]
except requests.exceptions.HTTPError as err:
    print(f"❌ Failed to create dashboard: {err}")
    exit(1)

# === Log to CHANGELOG.md
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
log_text = f"\n## {timestamp}\n🆕 Created `{NEW_TITLE}` with UID `{new_uid}`: includes static overview + 5 live metric panels.\n"

try:
    with open("vault/CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write(log_text)
    print(f"\n✅ Dashboard created successfully! UID: {new_uid}")
except Exception as e:
    print(f"⚠️ Dashboard created, but failed to log changelog: {e}")
