import os
import sys
import ollama

VAULT_PATH = r"C:\Users\Steve\Documents\ObsidianVaults\MainVault\onedrive-insights"
MODEL = "llama3:latest"

def load_summaries():
    combined = ""
    for file in os.listdir(VAULT_PATH):
        if file.endswith("-summary.md"):
            with open(os.path.join(VAULT_PATH, file), "r", encoding="utf-8") as f:
                text = f.read()
                combined += f"\n\n### {file}\n{text}"
    return combined

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python query_obsidian_with_ollama.py \"Your question here\"")
        return

    question = sys.argv[1]
    context = load_summaries()

    print(f"🤖 Asking Ollama: {question}\n")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert researcher helping analyze historical record summaries from OneDrive."},
            {"role": "user", "content": f"Here are the records:\n{context}\n\nQuestion: {question}"}
        ]
    )

    print("\n🧠 Answer:\n" + response['message']['content'])

if __name__ == "__main__":
    main()
