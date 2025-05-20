import os
import subprocess
from pathlib import Path
import pytesseract
from PIL import Image
import docx
import pdfplumber

# === CONFIGURATION ===
VAULT_ROOT = Path("C:/Users/Steve/Documents/ObsidianVaults/MainVault")
SYNC_DIR = VAULT_ROOT / "onedrive-sync"
OUTPUT_DIR = VAULT_ROOT / "onedrive-insights"
OUTPUT_DIR.mkdir(exist_ok=True)

# 🧠 Set exact path to Tesseract (since it's not in PATH)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === TEXT EXTRACTION FUNCTIONS ===
def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_text_from_image(path):
    return pytesseract.image_to_string(Image.open(path))

def extract_text(path):
    ext = path.suffix.lower()
    try:
        if ext == ".txt":
            return path.read_text(encoding='utf-8', errors='ignore')
        elif ext == ".docx":
            return extract_text_from_docx(path)
        elif ext == ".pdf":
            return extract_text_from_pdf(path)
        elif ext in [".jpg", ".jpeg", ".png"]:
            return extract_text_from_image(path)
    except Exception as e:
        print(f"❌ Failed to extract from {path.name}: {e}")
        return ""

# === OLLAMA SUMMARIZATION ===
def ask_ollama(text):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", f"Summarize this:\n\n{text[:4000]}"],
            capture_output=True,
            text=True,
            timeout=90
        )
        return result.stdout.strip()
    except Exception as e:
        return f"❌ Error summarizing: {e}"

# === MAIN LOOP ===
for path in SYNC_DIR.rglob("*"):
    if path.suffix.lower() not in [".txt", ".docx", ".pdf", ".jpg", ".jpeg", ".png"]:
        continue

    summary_file = OUTPUT_DIR / (path.stem + "-summary.md")
    if summary_file.exists():
        continue  # skip if already processed

    print(f"🔍 Processing: {path.name}")
    content = extract_text(path)
    if not content.strip():
        print(f"⚠️ No content found in {path.name}")
        continue

    summary = ask_ollama(content)
    summary_file.write_text(f"# Summary of {path.name}\n\n{summary}", encoding="utf-8")
    print(f"✅ Saved summary: {summary_file.name}")

print("🎉 All files processed.")
