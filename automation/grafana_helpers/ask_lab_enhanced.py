import subprocess
import requests
import json
import argparse
import os
from datetime import datetime

# === CONFIGURATION ===
NODE_IP = "192.168.10.100"
NODE_USER = "root"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
BACKUP_LOG_PATH = "automation/ollama_helpers/proxmox_status_log.md"
CACHE_FILE = "automation/grafana_helpers/cache_lab.json"
QALOG_FILE = "automation/grafana_helpers/lab_qa_log.md"

def ssh_command(cmd):
    full_cmd = ["ssh", f"{NODE_USER}@{NODE_IP}", cmd]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception as e:
        return f"[ERROR] SSH '{cmd}': {str(e)}"

def fetch_live_data():
    return {
        "vm": ssh_command("qm list"),
        "ct": ssh_command("pct list"),
        "uptime": ssh_command("uptime"),
        "free": ssh_command("free -m"),
        "df": ssh_command("df -h /"),
    }

def read_backup_log():
    if os.path.exists(BACKUP_LOG_PATH):
        with open(BACKUP_LOG_PATH, "r", encoding="utf-8-sig", errors="ignore") as f:
            return f.read()
    return "No backup log found."

def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

def ask_ollama(question, system_context):
    headers = {"Content-Type": "application/json"}
    prompt = (
        "System status summary based on the following:\n\n"
        + system_context +
        "\n\nUser question: " + question + "\n\n"
        "Answer clearly and briefly. Use bullet points if helpful."
    )
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    return response.json().get("response", "").strip()

def log_qa(question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(QALOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"### {timestamp}\n\n**Q:** {question}\n\n**A:**\n{answer}\n\n---\n")

def main(question, use_cache, log_q):
    print("📡 Gathering system info..." if not use_cache else "💾 Using cached system info...")
    data = load_cache() if use_cache else fetch_live_data()

    if not use_cache:
        save_cache(data)

    backup_summary = read_backup_log()

    system_context = (
        f"VM List:\n{data['vm']}\n"
        f"Container List:\n{data['ct']}\n"
        f"Uptime:\n{data['uptime']}\n"
        f"Memory (free -m):\n{data['free']}\n"
        f"Disk (df -h):\n{data['df']}\n"
        f"Backup Log:\n{backup_summary}\n"
    )

    print("🧠 Asking Ollama...")
    answer = ask_ollama(question, system_context)

    print("\n🤖 Response:\n")
    print(answer)

    if log_q:
        log_qa(question, answer)
        print(f"\n📝 Logged to: {QALOG_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask your Proxmox system a natural language question.")
    parser.add_argument("question", type=str, help="The question to ask about your lab status")
    parser.add_argument("--cache", action="store_true", help="Use cached system data instead of live SSH")
    parser.add_argument("--log", action="store_true", help="Log the question and answer to markdown")
    args = parser.parse_args()
    main(args.question, args.cache, args.log)
