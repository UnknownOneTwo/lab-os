import os
import re

SUMMARY_FOLDER = r"C:\Users\Steve\Documents\ObsidianVaults\MainVault\onedrive-insights"

# Basic keyword-to-tag logic
TAG_KEYWORDS = {
    "census": "census",
    "death": "death",
    "birth": "birth",
    "marriage": "marriage",
    "divorce": "divorce",
    "draft": "military",
    "wwi": "military",
    "wwii": "military",
    "navy": "military",
    "index": "index",
    "obit": "obituary",
    "tree": "image",
}

def generate_tags(filename):
    base = filename.lower()
    tags = {"summary"}
    for keyword, tag in TAG_KEYWORDS.items():
        if keyword in base:
            tags.add(tag)
    return sorted(tags)

def extract_source_file(filename):
    return re.sub(r"-summary\.md$", ".jpg", filename)

def has_frontmatter(text):
    return text.strip().startswith("---")

def add_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if has_frontmatter(content):
        print(f"⚠️ Skipped (already has frontmatter): {os.path.basename(path)}")
        return

    filename = os.path.basename(path)
    tags = generate_tags(filename)
    source = extract_source_file(filename)

    frontmatter = f"""---
tags: [{', '.join(tags)}]
source_file: {source}
generated_by: ollama
---

"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    print(f"✅ Added frontmatter: {filename}")

def main():
    for file in os.listdir(SUMMARY_FOLDER):
        if file.endswith("-summary.md"):
            add_frontmatter(os.path.join(SUMMARY_FOLDER, file))

if __name__ == "__main__":
    main()
