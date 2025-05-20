import subprocess
import json
import os
import requests
import argparse
from datetime import datetime

# === CONFIGURATION ===
NODE_IP = "192.168.10.100"
NODE_USER = "root"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
LOG_FILE = "automation/ollama_helpers/proxmox_status_log.md"

def ssh_command(cmd):
    full_cmd = ["ssh", f"{NODE_USER}@{NODE_IP}", cmd]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception as e:
        return f"Error running SSH command: {cmd}\n{str(e)}"

def ask_ollama(prompt, system="You are a helpful assistant summarizing Proxmox VM and container activity."):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    return response.json().get("response", "").strip()

def save_log(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a") as f:
        f.write(f"## {timestamp}\n\n{content}\n\n---\n")

def main(log_output=False, alerts_only=False):
    print("📡 Connecting to Proxmox node...")

    qm = ssh_command("qm list")
    pct = ssh_command("pct list")
    uptime = ssh_command("uptime")
    df = ssh_command("df -h /")
    pveperf = "" if alerts_only else ssh_command("pveperf")

    prompt = (
        "Remote Proxmox cluster status:\n\n"
        + f"VM List (qm list):\n{qm}\n\n"
        + f"Container List (pct list):\n{pct}\n\n"
        + f"System Uptime:\n{uptime}\n\n"
        + f"Disk Usage:\n{df}\n\n"
        + f"Performance (pveperf):\n{pveperf}\n\n"
    )
    if alerts_only:
        prompt += "Only include alerts or issues.\n"

    print("🤖 Asking Ollama to summarize system state...")
    summary = ask_ollama(prompt)

    print("\n🧠 AI Summary:\n")
    print(summary)

    if log_output:
        save_log(summary)
        print(f"✅ Logged to {LOG_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remote Proxmox VM/LXC status summarizer using Ollama")
    parser.add_argument("--log", action="store_true", help="Save the summary to a Markdown log file")
    parser.add_argument("--alerts", action="store_true", help="Focus only on errors or concerns")
    args = parser.parse_args()

    main(log_output=args.log, alerts_only=args.alerts)
