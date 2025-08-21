import requests

# Initialize Ollama client
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:27b"

# Store full document content
full_document = ""


def load_pdf(file_path):
    global full_document

    import PyPDF2
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    full_document = text
    return f"Loaded full document from {file_path} ({len(text)} characters)"


def generate_answer(question):
    if not full_document:
        load_pdf("aktai/Darbo_Kodeksas.pdf")

    # Truncate document to 128k to avoid overwhelming the model
    if len(full_document) > 500000:
        doc_excerpt = full_document[:500000]
        print(f"!!! Document truncated !!! original size {len(full_document)}")
    else:
        doc_excerpt = full_document

    prompt = f"""SVARBU: Atsakyk TIK lietuvių kalba!

Tu esi Vadovybės Apsaugos Tarnybos tesininkas. Atsakyk į klausimą lietuvių kalba remdamasis dokumentu.

Dokumento turinys:
{doc_excerpt}

Klausimas: {question}

Atsakymas lietuvių kalba:"""

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get('response', 'No response generated')
    except Exception as e:
        return f"Error generating response: {str(e)}"
