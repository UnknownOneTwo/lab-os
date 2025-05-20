from docx import Document
from pathlib import Path

file_path = Path(r"C:\Users\Steve\OneDrive\Documents\THE NEWS.docx")

def extract_docx_text(path: Path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

if __name__ == "__main__":
    print(f"🔍 Reading: {file_path.name}\n")
    text = extract_docx_text(file_path)
    print(text[:1500] + ("\n..." if len(text) > 1500 else ""))  # Print preview
