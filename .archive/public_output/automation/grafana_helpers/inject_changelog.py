import requests
import json
import argparse
import os

# === CONFIGURATION ===
GRAFANA_URL = "http://192.168.10.102:3000"
API_KEY = "glsa_Ib4dLIPwkcTgq9gcJuVfYKo3qmUEN0qA_2538a69b"
LOG_DIR = "monitoring/changelog"
PANEL_TITLE = "📝 Changelog"

def get_dashboard(uid):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{GRAFANA_URL}/api/dashboards/uid/{uid}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def update_changelog_panel(dashboard_json, uid, changelog_text):
    dashboard = dashboard_json["dashboard"]
    existing_panels = dashboard.get("panels", [])

    # Find or create the changelog panel
    changelog_panel = next((p for p in existing_panels if p.get("title") == PANEL_TITLE), None)

    if changelog_panel:
        changelog_panel["options"]["content"] = changelog_text
    else:
        panel_id = max((p["id"] for p in existing_panels), default=0) + 1
        new_panel = {
            "id": panel_id,
            "type": "text",
            "title": PANEL_TITLE,
            "gridPos": {"h": 10, "w": 24, "x": 0, "y": 0},
            "options": {
                "content": changelog_text,
                "mode": "markdown",
                "scroll": True
            },
            "transparent": False
        }
        dashboard["panels"].append(new_panel)

    payload = {
        "dashboard": dashboard,
        "folderId": dashboard_json.get("meta", {}).get("folderId", 0),
        "overwrite": True,
        "message": "Auto-updated changelog panel"
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{GRAFANA_URL}/api/dashboards/db"
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def main(uid):
    log_path = os.path.join(LOG_DIR, f"grafana_{uid}_log.md")
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"No changelog file found at {log_path}")

    with open(log_path, "r", encoding="utf-8-sig", errors="replace") as f:
        changelog_md = f.read()

    print("📥 Fetching dashboard...")
    dashboard_json = get_dashboard(uid)

    print("📤 Injecting changelog into panel...")
    update_changelog_panel(dashboard_json, uid, changelog_md)
    print("✅ Changelog panel updated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject Grafana changelog into text panel.")
    parser.add_argument("--uid", required=True, help="Dashboard UID")
    args = parser.parse_args()
    main(args.uid)
