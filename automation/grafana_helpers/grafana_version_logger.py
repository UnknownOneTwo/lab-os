import subprocess
import json
import os
import requests
import argparse
from datetime import datetime

# === CONFIGURATION ===
GRAFANA_URL = "http://192.168.10.102:3000"
API_KEY = "glsa_Ib4dLIPwkcTgq9gcJuVfYKo3qmUEN0qA_2538a69b"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
LOG_DIR = "monitoring/changelog"

def fetch_dashboard(uid):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    url = f"{GRAFANA_URL}/api/dashboards/uid/{uid}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch dashboard UID {uid}: {response.text}")
    return response.json()

def summarize_with_ollama(content, uid):
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"Here is a Grafana dashboard JSON for UID '{uid}'. "
        + "Summarize the purpose, any recent changes, and notable panels or layout features:\n\n"
        + content
    )
    data = {
        "model": MODEL,
        "prompt": prompt,
        "system": "You are a Grafana expert helping document dashboard changes for system administrators.",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    return response.json().get("response", "").strip()

def save_summary(uid, summary):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_path = os.path.join(LOG_DIR, f"grafana_{uid}_log.md")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"## {timestamp}\n\n{summary}\n\n---\n")
    return log_path

def main(uid):
    print(f"📡 Fetching dashboard UID: {uid}...")
    dashboard_json = fetch_dashboard(uid)
    readable_json = json.dumps(dashboard_json, indent=2)

    print("🧠 Sending to Ollama for summary...")
    summary = summarize_with_ollama(readable_json, uid)

    print("\n📋 Summary:")
    print(summary)

    log_file = save_summary(uid, summary)
    print(f"✅ Logged to: {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grafana Dashboard AI Summarizer")
    parser.add_argument("--uid", required=True, help="Grafana dashboard UID (e.g., proxmox-metrics-overview)")
    args = parser.parse_args()
    main(args.uid)
