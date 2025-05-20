import subprocess
import json
import os
import requests
import argparse
from datetime import datetime
import re

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

def get_latest_version(log_path):
    if not os.path.exists(log_path):
        return "v1.0"
    with open(log_path, "r") as f:
        versions = re.findall(r"## \[v(\d+\.\d+)\]", f.read())
    return f"v{versions[-1]}" if versions else "v1.0"

def bump_version(version, mode):
    major, minor = map(int, version[1:].split("."))
    if mode == "major":
        major += 1
        minor = 0
    elif mode == "patch":
        minor += 1
    return f"v{major}.{minor}"

def save_summary(uid, summary, version):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_path = os.path.join(LOG_DIR, f"grafana_{uid}_log.md")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(f"## [{version}] – {timestamp}\n\n{summary}\n\n---\n")
    return log_path

def git_commit(file_path, version):
    prompt = f"Write a concise Git commit message summarizing version {version} update to the Grafana dashboard changelog file at {file_path}."
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "system": "You are a DevOps assistant that writes clear and useful Git commit messages.",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    commit_msg = response.json().get("response", "").strip()
    subprocess.run(["git", "add", file_path])
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push", "origin", "main"])
    return commit_msg

def main(uid, tag_mode, custom_tag, do_commit):
    print(f"📡 Fetching dashboard UID: {uid}...")
    dashboard_json = fetch_dashboard(uid)
    readable_json = json.dumps(dashboard_json, indent=2)

    print("🧠 Sending to Ollama for summary...")
    summary = summarize_with_ollama(readable_json, uid)

    log_path = os.path.join(LOG_DIR, f"grafana_{uid}_log.md")
    current = get_latest_version(log_path)

    if custom_tag:
        version = custom_tag
    else:
        version = bump_version(current, tag_mode or "patch")

    print(f"📝 Saving as version: {version}")
    path = save_summary(uid, summary, version)
    print(f"✅ Logged to: {path}")

    if do_commit:
        print("📤 Committing to Git...")
        commit_msg = git_commit(path, version)
        print(f"✅ Git commit: {commit_msg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grafana Dashboard AI Summarizer + Version Logger")
    parser.add_argument("--uid", required=True, help="Grafana dashboard UID (e.g., dem0v6zlwt7nkb)")
    parser.add_argument("--tag", choices=["patch", "major"], help="Specify semantic version bump type")
    parser.add_argument("--custom", help="Use a custom version tag (e.g., v2.5)")
    parser.add_argument("--commit", action="store_true", help="Auto-commit the changelog")
    args = parser.parse_args()

    main(args.uid, args.tag, args.custom, args.commit)
