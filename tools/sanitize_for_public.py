import os
import shutil

IGNORE_FILE = ".publicignore"
SOURCE_DIR = os.getcwd()
DEST_DIR = os.path.join(SOURCE_DIR, "public_output")

def load_ignore_patterns():
    if not os.path.exists(IGNORE_FILE):
        return []
    with open(IGNORE_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def should_ignore(path, patterns):
    from fnmatch import fnmatch
    return any(fnmatch(path, pat) for pat in patterns)

def sanitize():
    ignore_patterns = load_ignore_patterns()
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR, exist_ok=True)

    for root, dirs, files in os.walk(SOURCE_DIR):
        if DEST_DIR in root or ".git" in root:
            continue
        rel_root = os.path.relpath(root, SOURCE_DIR)
        for file in files:
            rel_path = os.path.normpath(os.path.join(rel_root, file))
            if should_ignore(rel_path, ignore_patterns):
                continue
            src_path = os.path.join(root, file)
            dst_path = os.path.join(DEST_DIR, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
    print("✅ Sanitization complete. Files saved to 'public_output/'.")

if __name__ == "__main__":
    sanitize()
