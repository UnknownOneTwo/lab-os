import os
from datetime import datetime
import argparse

# === CONFIGURATION ===
CHANGELOG_PATH = "vault/CHANGELOG.md"

# === CLI ARGUMENTS ===
parser = argparse.ArgumentParser(description="📋 Append a new entry to the lab changelog.")
parser.add_argument("--note", required=True, help="The changelog entry text.")
parser.add_argument("--version", help="Optional version label (e.g., v1.2)")
args = parser.parse_args()

# === FORMAT ENTRY ===
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
version_label = f"## [{args.version}] — {timestamp}" if args.version else f"## {timestamp}"

entry = f"""\n{version_label}\n\n- {args.note.strip()}\n"""

# === APPEND TO FILE ===
try:
    with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print("✅ New changelog entry added.")
except Exception as e:
    print(f"❌ Failed to update changelog: {e}")
