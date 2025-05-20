import requests
from pathlib import Path
from docx import Document

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def extract_docx_text(path: Path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def send_to_ollama(text: str, prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{prompt}\n\n{text}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "").strip()

if __name__ == "__main__":
    path = Path(r"C:\Users\Steve\OneDrive\Documents\THE NEWS.docx")
    doc_text = extract_docx_text(path)
    
    prompt = "You're a professional comedy writer. Suggest punch-ups or edits to this sketch:"
    print("🤖 Sending to Ollama...")
    result = send_to_ollama(doc_text, prompt)

    print("\n📝 AI Response:\n")
    print(result)
