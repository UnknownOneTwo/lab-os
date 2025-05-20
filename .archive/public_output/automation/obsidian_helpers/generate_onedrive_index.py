import os
from collections import defaultdict

# Correct folders
SUMMARY_FOLDER = r"C:\Users\Steve\Documents\ObsidianVaults\MainVault\onedrive-insights"
OUTPUT_FILE = r"C:\Users\Steve\Documents\ObsidianVaults\MainVault\OneDrive Index.md"

CATEGORIES = {
    "Tree": "🌳 Tree Images",
    "Death": "⚰️ Death Records",
    "Marriage": "💍 Marriage Records",
    "Divorce": "💔 Divorce Records",
    "Draft": "🪖 Military Draft Records",
    "WWI": "🌍 WWI",
    "WWII": "🌍 WWII",
    "Navy": "⚓ Navy Records",
    "Obit": "📰 Obituaries",
    "Map": "🗺️ Maps & Locations",
    "Monogram": "🔤 Monograms & Icons",
    "Frame": "🖼️ Frames & Borders",
    "Flowers": "🌸 Floral/Designs",
    "Index": "📄 Indexes & Rolls",
    "Birth": "👶 Birth Records",
    "Headstone": "🪦 Headstones & Cemeteries",
    "Ship": "🚢 Boats & Ships",
    "Military": "🪖 Military Misc",
    "Census": "📊 Census Records",
}

def categorize(filename):
    for keyword, label in CATEGORIES.items():
        if keyword.lower() in filename.lower():
            return label
    return "📂 Other Files"

def main():
    index = defaultdict(list)
    print(f"📁 Scanning folder: {SUMMARY_FOLDER}\n")

    found = False
    for file in os.listdir(SUMMARY_FOLDER):
        if "-summary" in file and file.endswith(".md"):
            found = True
            base = file.replace(".md", "")
            category = categorize(base)
            index[category].append(base)
            print(f"✅ Found summary: {base} → {category}")

    if not found:
        print("⚠️ No summary files found. Check path or filenames.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# 🗂 OneDrive Summary Index\n\n")
        for category, files in sorted(index.items()):
            f.write(f"## {category}\n")
            for item in sorted(files):
                f.write(f"- [[onedrive-insights/{item}]]\n")
            f.write("\n")

    print(f"\n✅ OneDrive Index saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
