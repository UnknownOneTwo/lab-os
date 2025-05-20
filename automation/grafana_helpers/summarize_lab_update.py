import argparse
import requests
import os

# === CONFIG ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
PROMPT_TEMPLATE = """
You are an expert DevOps assistant. Your task is to analyze the following technical change or system log, and summarize it as a clear and concise changelog entry. Use past tense. One paragraph. Do not include labels, bullet points, or extra explanation.

=== BEGIN INPUT ===
{input}
=== END INPUT ===
"""

# === ARGPARSE ===
parser = argparse.ArgumentParser(description="🧠 Summarize system updates with Ollama for changelog entry.")
parser.add_argument("--source", type=str, help="Path to input file (e.g. logs or config)")
parser.add_argument("--text", type=str, help="Direct input text (overrides --source)")
args = parser.parse_args()

# === LOAD TEXT ===
if args.text:
    input_text = args.text.strip()
elif args.source and os.path.exists(args.source):
    with open(args.source, "r", encoding="utf-8") as f:
        input_text = f.read().strip()
else:
    print("❌ You must provide --text or a valid --source file.")
    exit(1)

# === GENERATE PROMPT ===
prompt = PROMPT_TEMPLATE.format(input=input_text)

# === SEND TO OLLAMA ===
response = requests.post(OLLAMA_URL, json={
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False
})

if response.status_code != 200:
    print(f"❌ Ollama request failed: {response.status_code} {response.text}")
    exit(1)

result = response.json()["response"]
print("\n✅ Changelog suggestion:\n")
print(result.strip())
