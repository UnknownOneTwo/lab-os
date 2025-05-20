import os
import shutil
from pathlib import Path

# === CONFIGURATION ===
source_dir = Path("C:/Users/Steve/OneDrive")
target_dir = Path("C:/Users/Steve/Documents/ObsidianVaults/MainVault/onedrive-sync")

# === FUNCTION ===
def sync_folders(src, dst):
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dst, rel_path)
        os.makedirs(dest_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_path, file)

            try:
                if not os.path.exists(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    shutil.copy2(src_file, dst_file)
                    print(f"✅ Copied: {file}")
            except PermissionError as e:
                print(f"⚠️ Skipped (in use): {src_file}")
            except Exception as e:
                print(f"❌ Error with {src_file}: {e}")

# === RUN ===
sync_folders(source_dir, target_dir)
print("🎉 Sync complete.")
