import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
GRAFANA_URL = "http://192.168.10.102:3000"
NEW_TITLE = "System Performance Monitor v1.1"
GRAFANA_TOKEN = os.getenv("GRAFANA_API_KEY")
HEADERS = {"Authorization": f"Bearer {GRAFANA_TOKEN}", "Content-Type": "application/json"}
DATASOURCE_NAME = "influxDB"

# === Static Markdown Panel ===
SERVER_OVERVIEW_MARKDOWN = """
# 🖥️ Proxmox Cluster Overview

## 🧩 Nodes

- **LAB-NODE-01**
  ▸ 🏷️ Role: Infrastructure  
  ▸ 💽 Disk: 1TB NVMe  
  ▸ 🧠 RAM: 62 GB  
  ▸ 🔌 IP: `192.168.10.100`  
  ▸ 📦 Services: InfluxDB, Grafana, Backups

- **GAME-NODE-01**
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
def make_influx_panel(title, query, panel_id, grid_pos, unit="percent"):
    return {
        "id": panel_id,
        "type": "timeseries",
        "title": title,
        "gridPos": grid_pos,
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
                    ]
                },
                "mappings": []
            },
            "overrides": []
        },
        "targets": [{
            "refId": "A",
            "rawQuery": True,
            "query": query,
            "datasource": DATASOURCE_NAME
        }]
    }

# === Build Clean Dashboard ===
dashboard = {
    "title": NEW_TITLE,
    "id": None,
    "uid": None,
    "timezone": "browser",
    "schemaVersion": 36,
    "version": 0,
    "refresh": "5s",
    "panels": []
}

# Add static overview panel
panel_id = 100
dashboard["panels"].append({
    "id": panel_id,
    "type": "text",
    "title": "🖥️ Server Overview",
    "gridPos": {"x": 0, "y": 0, "w": 12, "h": 4},
    "options": {"mode": "markdown", "content": SERVER_OVERVIEW_MARKDOWN.strip()},
    "fieldConfig": {"defaults": {}, "overrides": []},
    "pluginVersion": "11.4.0"
})

# Add metrics panels
panel_id += 1
dashboard["panels"].append(make_influx_panel("🔥 CPU Usage", 'SELECT mean("usage_user") FROM "cpu" WHERE time > now() - 5m', panel_id, {"x": 0, "y": 4, "w": 6, "h": 6}))
panel_id += 1
dashboard["panels"].append(make_influx_panel("🧠 Memory Usage", 'SELECT last("used_percent") FROM "mem"', panel_id, {"x": 6, "y": 4, "w": 6, "h": 6}))
panel_id += 1
dashboard["panels"].append(make_influx_panel("💽 Disk Usage (/)", 'SELECT last("used_percent") FROM "disk" WHERE "path" = "/"', panel_id, {"x": 0, "y": 10, "w": 6, "h": 6}))
panel_id += 1
dashboard["panels"].append(make_influx_panel("🌐 Network In/Out", 'SELECT derivative(mean("bytes_recv"), 1s), derivative(mean("bytes_sent"), 1s) FROM "net" WHERE "interface" = \'eno1\' AND time > now() - 10m GROUP BY time(10s)', panel_id, {"x": 6, "y": 10, "w": 6, "h": 6}))
panel_id += 1
dashboard["panels"].append(make_influx_panel("⚙️ System Load (1m)", 'SELECT last("load1") FROM "system"', panel_id, {"x": 0, "y": 16, "w": 12, "h": 4}))

# === Push to Grafana ===
payload = {
    "dashboard": dashboard,
    "folderId": 0,
    "message": f"Created clean {NEW_TITLE}",
    "overwrite": False
}

print("\n📦 Sending clean dashboard payload to Grafana...\n")
response = requests.post(f"{GRAFANA_URL}/api/dashboards/db", headers=HEADERS, json=payload)
try:
    response.raise_for_status()
    new_uid = response.json()["uid"]
    print(f"✅ Dashboard created successfully! UID: {new_uid}")
except Exception as e:
    print(f"❌ Failed to create dashboard: {e}")
