import subprocess
import json
import os
import requests
import argparse
import platform
from datetime import datetime

# === PLATFORM DETECTION ===
IS_WINDOWS = platform.system() == "Windows"

# === CONFIGURATION ===
REPO_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHANGELOG_GIT = os.path.join(REPO_PATH, "docs", "changelog.md")
CHANGELOG_LOCAL = (
    os.path.expanduser("C:/Users/Steve/Documents/github/proxmox-homelab/logs/lab-tag-history/changelog.txt")
    if IS_WINDOWS else
    "/root/lab-tag-history/changelog.txt"
)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# === GIT FUNCTIONS ===
def get_git_diff():
    return subprocess.check_output(["git", "diff", "--cached"], cwd=REPO_PATH).decode("utf-8")

def get_git_status():
    return subprocess.check_output(["git", "status"], cwd=REPO_PATH).decode("utf-8")

# === OLLAMA REQUEST ===
def ask_ollama(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "system": "You are a helpful assistant that summarizes git diffs as changelog entries for a system administrator.",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, headers=headers, data=json.dumps(data))
    return response.json().get("response", "").strip()

# === CHANGELOG WRITER ===
def append_to_file(filepath, entry):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"## {timestamp}\n\n{entry}\n\n---\n")

# === MAIN FUNCTION ===
def main():
    parser = argparse.ArgumentParser(description="Ollama-enhanced changelog writer")
    parser.add_argument('--note', type=str, help="Manual changelog note (bypasses AI)")
    args = parser.parse_args()

    if args.note:
        print("📝 Manual note mode activated.")
        entry = args.note
    else:
        print("🔍 Reading Git staged changes...")
        diff = get_git_diff()
        status = get_git_status()

        if not diff.strip():
            print("⚠️ No staged changes detected. Please run 'git add' first.")
            return

        print("🧠 Asking Ollama to generate a changelog entry...")
        prompt = f"Here is the git status:\n{status}\n\nAnd the diff:\n{diff}\n\nPlease write a clear changelog entry summarizing what was changed and why."
        entry = ask_ollama(prompt)
        print("\n📝 Changelog Entry:\n")
        print(entry)

    print("📥 Appending to changelogs...")
    append_to_file(CHANGELOG_GIT, entry)
    append_to_file(CHANGELOG_LOCAL, entry)

    print("✅ Changelog updated:")
    print(f"   - {CHANGELOG_GIT}")
    print(f"   - {CHANGELOG_LOCAL}")

    print("\n👉 You can now commit the changelog with:")
    print(f'cd "{REPO_PATH}"')
    print('git add docs/changelog.md')
    print('git commit -m "📝 Update changelog"')
    print('git push origin main')

if __name__ == "__main__":
    main()
