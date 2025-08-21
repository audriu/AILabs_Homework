import requests

# Initialize Ollama client
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:32b"

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

    # Use smaller, more focused excerpt
    if len(full_document) > 100000:
        # Try to find relevant section first
        question_lower = question.lower()
        best_start = 0
        for keyword in question_lower.split():
            pos = full_document.lower().find(keyword)
            if pos > 0:
                best_start = max(0, pos - 10000)
                break
        
        doc_excerpt = full_document[best_start:best_start + 100000]
        print(f"Using excerpt from position {best_start}")
    else:
        doc_excerpt = full_document

    prompt = f"""<|system|>SVARBU: Atsakyk TIK lietuvių kalba!
Tu esi Lietuvos darbo teisės ekspertas. Atsakyk TIKSLIAI į klausimą remdamasis tik pateiktu dokumentu. Jei atsakymo nėra dokumente, pasakyk "Informacijos nėra dokumente".

<|document|>
{doc_excerpt}

<|user|>
{question}

<|assistant|>
Atsakymas lietuvių kalba remiantis dokumentu:"""

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_ctx": 8192
            }
        }
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get('response', 'No response generated')
    except Exception as e:
        return f"Error generating response: {str(e)}"
