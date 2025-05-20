import os
import sys
import shutil
import requests
import json
from pathlib import Path
from datetime import datetime
import argparse
import re

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("❌ PyPDF2 not found. Install with: pip install PyPDF2")
    sys.exit(1)

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

# === CONFIGURATION ===
VAULT_PATH = os.path.expanduser("C:/Users/Steve/Documents/ObsidianVaults/MainVault/onedrive-insights")
SUMMARY_LOG = os.path.expanduser("C:/Users/Steve/Documents/ObsidianVaults/MainVault/OneDrive_Summary_Log.md")
ONEDRIVE_PATH = os.path.expanduser("C:/Users/Steve/OneDrive")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:latest"
EXTENSIONS = [".pdf", ".txt", ".md", ".docx", ".png", ".jpg", ".jpeg"]
SUMMARY_SUFFIX = "-summary.md"
LOG_FILE = os.path.expanduser("C:/Users/Steve/Documents/github/proxmox-homelab/logs/summarize_onedrive.log")

# === HELPERS ===
def guess_tags(text):
    tags = []
    if re.search(r'resume|employment|job', text, re.I):
        tags.append("resume")
    if re.search(r'census|ancestry|genealogy|family tree', text, re.I):
        tags.append("genealogy")
    if re.search(r'Grafana|Proxmox|VM|LXC|server', text, re.I):
        tags.append("homelab")
    return tags or ["untagged"]

def summarize_with_ollama(text):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You summarize text from historical or technical documents into concise markdown summaries."},
            {"role": "user", "content": text[:8000]}
        ],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")
    except Exception as e:
        print(f"⚠️ Failed to summarize: {e}")
        return ""

def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        return "\n".join([page.extract_text() or "" for page in reader.pages])
    except Exception as e:
        print(f"⚠️ PDF extraction error for {filepath}: {e}")
        return ""

def extract_text_from_txt(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ TXT read error for {filepath}: {e}")
        return ""

def extract_text_from_image(filepath):
    if not (Image and pytesseract):
        print(f"⚠️ Skipping image (OCR libs not available): {filepath}")
        return ""
    if not shutil.which("tesseract"):
        print(f"⚠️ OCR error for {filepath}: Tesseract not installed or not in PATH.\n📎 Visit: https://github.com/tesseract-ocr/tesseract/releases")
        return ""
    try:
        img = Image.open(filepath)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"⚠️ OCR error for {filepath}: {e}")
        return ""

def save_summary(original_path, summary_text, tags):
    basename = Path(original_path).stem
    summary_file = os.path.join(VAULT_PATH, f"{basename}{SUMMARY_SUFFIX}")
    try:
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"---\ntags: [{', '.join(tags)}]\n---\n\n")
            f.write(summary_text.strip())
        print(f"✅ Saved summary: {summary_file}")
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now().isoformat()} | {original_path} => {summary_file}\n")
        with open(SUMMARY_LOG, "a", encoding="utf-8") as vaultlog:
            vaultlog.write(f"### [{Path(summary_file).name}]({summary_file})\nTags: {' '.join('#'+tag for tag in tags)}\nPreview: {summary_text.strip()[:200]}...\n\n")
    except Exception as e:
        print(f"⚠️ Failed to save summary for {original_path}: {e}")

def clean_filename(filename):
    return re.sub(r'[\s\(\)]+', '-', filename).strip('-').lower()

def summarize_file(filepath, force=False):
    ext = Path(filepath).suffix.lower()
    if ext not in EXTENSIONS:
        return

    basename = Path(filepath).stem
    summary_file = os.path.join(VAULT_PATH, f"{basename}{SUMMARY_SUFFIX}")
    if not force and os.path.exists(summary_file):
        print(f"⏭️ Skipping existing summary: {summary_file}")
        return

    print(f"📄 Summarizing: {Path(filepath).name}")
    print(f"🕒 Waiting for Ollama to process {Path(filepath).name}...")

    if ext == ".pdf":
        content = extract_text_from_pdf(filepath)
    elif ext in [".txt", ".md"]:
        content = extract_text_from_txt(filepath)
    elif ext in [".png", ".jpg", ".jpeg"]:
        content = extract_text_from_image(filepath)
    else:
        print("⚠️ Unsupported file type for summarization (yet):", filepath)
        return

    if not content.strip():
        print("⚠️ No content to summarize.")
        return

    summary = summarize_with_ollama(content)
    if summary:
        tags = guess_tags(content)
        save_summary(filepath, summary, tags)

# === MAIN ===
def main():
    parser = argparse.ArgumentParser(description="Summarize text from OneDrive into Obsidian.")
    parser.add_argument("--force", action="store_true", help="Reprocess all files even if summary exists")
    parser.add_argument("--folder", type=str, help="Only summarize a specific subfolder inside OneDrive")
    parser.add_argument("--clean-names", action="store_true", help="Rename messy filenames")
    args = parser.parse_args()

    os.makedirs(VAULT_PATH, exist_ok=True)
    scan_path = os.path.join(ONEDRIVE_PATH, args.folder) if args.folder else ONEDRIVE_PATH
    print(f"🔍 Scanning OneDrive folder: {scan_path}\n")
    count = 0
    for root, dirs, files in os.walk(scan_path):
        for file in files:
            if Path(file).suffix.lower() in EXTENSIONS:
                full_path = os.path.join(root, file)
                if args.clean_names:
                    clean_name = clean_filename(file)
                    new_path = os.path.join(root, clean_name)
                    if file != clean_name:
                        os.rename(full_path, new_path)
                        full_path = new_path
                summarize_file(full_path, force=args.force)
                count += 1
    print(f"\n✅ Completed. Total files summarized: {count}")

if __name__ == "__main__":
    main()
