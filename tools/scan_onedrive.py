import os

ONEDRIVE_PATH = r"C:\Users\Steve\OneDrive"
SUPPORTED_EXTENSIONS = (".pdf", ".docx", ".txt", ".md", ".jpg", ".jpeg", ".png")

def scan_onedrive(root=ONEDRIVE_PATH):
    matches = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith(SUPPORTED_EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                matches.append(full_path)
    return matches

if __name__ == "__main__":
    files = scan_onedrive()
    print(f"🔍 Found {len(files)} supported files.\n")
    for f in files[:25]:
        print(f)
