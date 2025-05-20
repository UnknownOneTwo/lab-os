import os
import csv
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ONEDRIVE_ROOT = os.getenv("ONEDRIVE_PATH", "C:/Users/Steve/OneDrive")
INDEX_FILE = "automation/obsidian_helpers/onedrive_index.csv"
VAULT_OUTPUT = "C:/Users/Steve/Documents/ObsidianVaults/MainVault/ResumeSearch"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

PROMPT_TEMPLATE = """
You are an intelligent assistant. Analyze the following text.

1. Is this file a resume, CV, or job-related professional document?
2. Is it about Steven Vik (or someone with a matching name)?
3. If YES, give a short summary of experience in bullet points.

Only answer YES or NO for relevance.
Then give a 2–3 line reason and the summary.
"""

def load_index(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def read_file_content(filepath):
    try:
        if filepath.endswith(".pdf"):
            import fitz  # PyMuPDF
            doc = fitz.open(filepath)
            return "\n".join([page.get_text() for page in doc])
        elif filepath.endswith(".docx"):
            from docx import Document
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        return f"[ERROR READING FILE]: {e}"
    return ""

def ask_ollama(prompt, content):
    full_prompt = PROMPT_TEMPLATE + "\n\n" + content[:3000]  # Truncate for speed
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=full_prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[OLLAMA ERROR]: {e}"

def save_summary(file_meta, summary):
    filename = Path(file_meta["full_path"]).stem
    safe_filename = filename.replace(" ", "_").replace(".", "_")
    out_path = Path(VAULT_OUTPUT) / f"steven-resume-summary-{safe_filename}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Summary of: {file_meta['name']}\n\n")
        f.write(f"**Original Path**: `{file_meta['full_path']}`\n\n")
        f.write(summary)

def main():
    files = load_index(INDEX_FILE)
    resume_candidates = [
        f for f in files
        if any(f["name"].lower().endswith(ext) for ext in [".pdf", ".docx", ".txt"])
    ]

    print(f"🔍 Scanning {len(resume_candidates)} documents...")

    for f in resume_candidates:
        full_path = os.path.join(ONEDRIVE_ROOT, f["full_path"])
        text = read_file_content(full_path)
        if not text or text.startswith("[ERROR"):
            continue

        print(f"🤖 Analyzing: {f['name']}")
        summary = ask_ollama(PROMPT_TEMPLATE, text)

        if summary.startswith("YES") or "Steven Vik" in summary:
            print(f"✅ Match found: {f['name']}")
            save_summary(f, summary)
        else:
            print(f"❌ Skipped: {f['name']}")

if __name__ == "__main__":
    main()
