import os
import sys
import requests
import json
import subprocess
from datetime import datetime
import re
from pathlib import Path

try:
    import pyperclip
except ImportError:
    pyperclip = None

# === CONFIGURATION ===
BASE_PATH = os.path.dirname(os.path.abspath(__file__)).split("automation")[0]
VAULT_PATH = os.path.expanduser("C:/Users/Steve/Documents/ObsidianVaults/MainVault/onedrive-insights")
QA_LOG_PATH = os.path.join(BASE_PATH, "docs")  # Log inside repo for git compatibility
ROLLING_LOG = os.path.join(QA_LOG_PATH, "qa-log.md")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:latest"

def slugify(text):
    return re.sub(r'[^\w\-]+', '-', text.lower()).strip('-')[:50]

def parse_args():
    args = sys.argv[1:]
    question_parts = [a for a in args if not a.startswith("--")]
    flags = {k.lstrip("--"): v for k, v in zip(args, args[1:] + [""]) if k.startswith("--")}
    question = " ".join(question_parts)
    return question, flags

def load_summaries(tag_filter=None):
    combined = ""
    for file in os.listdir(VAULT_PATH):
        if file.endswith("-summary.md"):
            if tag_filter and tag_filter.lower() not in file.lower():
                continue
            with open(os.path.join(VAULT_PATH, file), "r", encoding="utf-8") as f:
                text = f.read()
                combined += f"\n\n### {file}\n{text}"
    return combined.strip()

def save_qna_file(question, answer, filename=None):
    os.makedirs(QA_LOG_PATH, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(question)
    fullpath = os.path.join(QA_LOG_PATH, filename) if filename else os.path.join(QA_LOG_PATH, f"{date}-{slug}.md")

    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(f"# Q: {question}\n\n")
        f.write("## A:\n")
        f.write(answer.strip() + "\n")

    print(f"\n💾 Saved Q&A to: {fullpath}")
    return fullpath

def append_qna(question, answer):
    os.makedirs(QA_LOG_PATH, exist_ok=True)
    with open(ROLLING_LOG, "a", encoding="utf-8") as f:
        f.write(f"\n---\n\n# Q: {question}\n\n## A:\n{answer.strip()}\n")
    print(f"\n📝 Appended Q&A to: {ROLLING_LOG}")
    return ROLLING_LOG

def is_in_repo(filepath):
    try:
        repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding="utf-8").strip()
        return os.path.abspath(filepath).startswith(repo_root)
    except:
        return False

def push_to_git(filepath):
    if not is_in_repo(filepath):
        print("⚠️ Git push skipped — file not in repository.")
        return
    try:
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", f"🧠 Q&A saved: {os.path.basename(filepath)}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Git push successful!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git error: {e}")

def main():
    question, flags = parse_args()
    if not question:
        print("❌ Usage: python query_obsidian_with_ollama_http.py \"Your question\" [--flag value]")
        return

    tag = flags.get("tag")
    save_log = flags.get("log", "on").lower() != "off"
    append_mode = "append" in flags
    output_file = flags.get("out")
    copy_md = "md" in flags
    push_git = "push" in flags

    context = load_summaries(tag_filter=tag)
    if not context:
        print("⚠️ No summaries found.")
        return

    print(f"🤖 Asking Ollama (HTTP): {question}")
    if tag:
        print(f"🔍 Tag filter: {tag}")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant answering questions about historical document summaries from an Obsidian vault."},
            {"role": "user", "content": f"Here are the summaries:\n{context}\n\nQuestion: {question}"}
        ],
        "stream": True
    }

    full_answer = ""

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            print("\n🧠 Answer:\n")
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        chunk = data.get('message', {}).get('content', '')
                        print(chunk, end="", flush=True)
                        full_answer += chunk
                    except json.JSONDecodeError:
                        pass
    except requests.exceptions.RequestException as e:
        print(f"\n❌ HTTP request failed: {e}")
        return

    saved_path = None
    if save_log:
        if append_mode:
            saved_path = append_qna(question, full_answer)
        else:
            saved_path = save_qna_file(question, full_answer, filename=output_file)
    else:
        print("\n⚠️ Skipped saving to Obsidian (log disabled)")

    if copy_md and pyperclip:
        md_output = f"# Q: {question}\n\n## A:\n{full_answer.strip()}"
        pyperclip.copy(md_output)
        print("\n📋 Copied markdown to clipboard.")
    elif copy_md:
        print("\n⚠️ pyperclip not available — install it with: pip install pyperclip")

    if push_git and saved_path:
        push_to_git(saved_path)

if __name__ == "__main__":
    main()