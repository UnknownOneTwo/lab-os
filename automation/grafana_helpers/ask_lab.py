import subprocess
import requests
import json
import argparse

# === CONFIGURATION ===
NODE_IP = "192.168.10.100"
NODE_USER = "root"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def ssh_command(cmd):
    full_cmd = ["ssh", f"{NODE_USER}@{NODE_IP}", cmd]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception as e:
        return f"Error running SSH command: {cmd}\n{str(e)}"

def ask_ollama(question, system_context):
    headers = {"Content-Type": "application/json"}
    prompt = (
        "System status:\n\n"
        + system_context +
        "\n\nUser question: " + question + "\n\n"
        "Respond concisely and clearly."
    )
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    return response.json().get("response", "").strip()

def main(user_question):
    print("📡 Fetching minimal Proxmox system info...")
    qm = ssh_command("qm list")
    pct = ssh_command("pct list")
    uptime = ssh_command("uptime")

    system_context = (
        f"VM List (qm list):\n{qm}\n"
        f"Container List (pct list):\n{pct}\n"
        f"System Uptime:\n{uptime}"
    )

    print("🧠 Asking Ollama...")
    response = ask_ollama(user_question, system_context)
    print("\n🤖 Response:\n")
    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask your Proxmox system a natural language question.")
    parser.add_argument("question", type=str, help="The question to ask about your lab status")
    args = parser.parse_args()
    main(args.question)
