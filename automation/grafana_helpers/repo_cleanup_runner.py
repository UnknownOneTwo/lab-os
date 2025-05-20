import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # assumes script is 2 levels deep (e.g., automation/grafana_helpers/)
ARCHIVE = ROOT / ".archive"
TOOLS = ROOT / "tools"
DOCS = ROOT / "docs"

# Ensure target folders exist
ARCHIVE.mkdir(exist_ok=True)
TOOLS.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)

# Items to archive
archive_items = [
    "vault",
    "public_output",
    "logs"
]

# Move legacy folders to .archive/
for item in archive_items:
    src = ROOT / item
    dst = ARCHIVE / item
    if src.exists():
        print(f"📦 Archiving: {src} → {dst}")
        shutil.move(str(src), str(dst))

# Move unused .bat scripts and temp files to tools/
tools_targets = [
    "run_weekly_sync.bat",
    "sync_to_public.bat",
    "sanitize_for_public.py",
    "automation/grafana_helpers/New Text Document.txt",
]

for target in tools_targets:
    src = ROOT / target
    dst = TOOLS / Path(target).name
    if src.exists():
        print(f"🛠️ Moving: {src} → {dst}")
        shutil.move(str(src), str(dst))

# Move cleanup plan doc to docs/
cleanup_doc = ROOT / "proxmox_homelab_folder_cleanup_plan.md"
if cleanup_doc.exists():
    print(f"📑 Moving cleanup plan to docs/")
    shutil.move(str(cleanup_doc), str(DOCS / cleanup_doc.name))

print("\n✅ Cleanup complete. Repository is now organized.")