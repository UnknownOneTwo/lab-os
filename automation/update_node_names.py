# (reposting the script here for quick copy-paste)
import os
import argparse

REPLACEMENTS = {
    "node-core-01": "node-core-01",
    "node-game-01": "node-game-01"
}

def replace_in_file(filepath, preview=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        return  # skip binary or unreadable files

    replaced = False
    for old, new in REPLACEMENTS.items():
        if old in content:
            replaced = True
            content = content.replace(old, new)

    if replaced:
        if preview:
            print(f"[PREVIEW] Would update: {filepath}")
        else:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"[UPDATED] {filepath}")

def walk_and_replace(directory, preview=False):
    for root, _, files in os.walk(directory):
        for name in files:
            if name.endswith(('.md', '.py', '.sh', '.txt', '.csv', '.yml', '.json')):
                filepath = os.path.join(root, name)
                replace_in_file(filepath, preview=preview)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace legacy node names with new ones.")
    parser.add_argument("path", help="Root directory to scan")
    parser.add_argument("--preview", action="store_true", help="Preview changes only, don't write")
    args = parser.parse_args()

    walk_and_replace(args.path, preview=args.preview)
