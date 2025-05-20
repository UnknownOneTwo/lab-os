import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# === CONFIGURATION ===
INFLUXDB_URL = "http://192.168.10.100:8086/query"
DATABASE = "telegraf"
GRAFANA_UPDATE = True  # Set to False if you don’t want to push to Grafana

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# === GRAFANA PANEL ===
GRAFANA_URL = "http://192.168.10.102:3000"
DASHBOARD_UID = "dem0v6zlwt7nkb"
PANEL_ID = 2  # 🧠 AI Insight panel (Markdown Text)
GRAFANA_TOKEN = os.getenv("GRAFANA_API_KEY")

def query_influx(q):
    params = {
        "db": DATABASE,
        "q": q
    }
    r = requests.get(INFLUXDB_URL, params=params)
    r.raise_for_status()
    return r.json()

def summarize_with_ollama(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"].strip()

def update_grafana_panel(summary_text):
    headers = {"Authorization": f"Bearer {GRAFANA_TOKEN}"}
    get_url = f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}"
    dashboard = requests.get(get_url, headers=headers).json()

    # Inject summary into panel
    for panel in dashboard["dashboard"]["panels"]:
        if panel["id"] == PANEL_ID:
            panel["options"]["content"] = f"### 🧠 AI Summary ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n{summary_text}"

    payload = {
        "dashboard": dashboard["dashboard"],
        "folderId": 0,
        "message": f"AI Insight updated at {datetime.now()}",
        "overwrite": True
    }
    post_url = f"{GRAFANA_URL}/api/dashboards/db"
    r = requests.post(post_url, json=payload, headers=headers)
    r.raise_for_status()

def append_to_changelog(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("vault/CHANGELOG.md", "a") as f:
        f.write(f"\n## {timestamp}\n{text}\n")

# === MAIN QUERY + SUMMARY ===
cpu = query_influx("SELECT mean(usage_user) FROM cpu WHERE time > now() - 10m")
mem = query_influx("SELECT last(used_percent) FROM mem")
sys = query_influx("SELECT last(load1) FROM system")

summary_prompt = f"""
System Metrics Overview (last 10 minutes):

- CPU usage (mean user): {json.dumps(cpu, indent=2)}
- Memory usage (last %): {json.dumps(mem, indent=2)}
- System load (last 1m): {json.dumps(sys, indent=2)}

Summarize these for a technical report. Highlight spikes, anomalies, or issues. Be concise.
"""

print("🧠 Sending metrics to Ollama...")
summary = summarize_with_ollama(summary_prompt)
print("✅ Summary:\n", summary)

append_to_changelog(summary)
if GRAFANA_UPDATE:
    update_grafana_panel(summary)
