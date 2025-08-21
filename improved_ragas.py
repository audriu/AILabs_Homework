import requests
import re
from typing import List, Tuple

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"

class DocumentChunker:
    def __init__(self, chunk_size=2000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
    
    def chunk_document(self, text: str) -> List[str]:
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text.strip())
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = text.rfind('.', start, end)
                if last_period > start + self.chunk_size // 2:
                    end = last_period + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.overlap
        
        self.chunks = chunks
        return chunks
    
    def find_relevant_chunks(self, question: str, top_k=3) -> List[str]:
        # Simple keyword matching - could be improved with embeddings
        question_words = set(question.lower().split())
        
        scored_chunks = []
        for i, chunk in enumerate(self.chunks):
            chunk_words = set(chunk.lower().split())
            score = len(question_words.intersection(chunk_words))
            scored_chunks.append((score, i, chunk))
        
        # Sort by score and return top chunks
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        return [chunk for _, _, chunk in scored_chunks[:top_k]]

chunker = DocumentChunker()

def load_pdf(file_path):
    import PyPDF2
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    chunks = chunker.chunk_document(text)
    return f"Loaded and chunked document: {len(chunks)} chunks"

def generate_answer(question):
    if not chunker.chunks:
        load_pdf("aktai/Darbo_Kodeksas.pdf")
    
    # Get most relevant chunks
    relevant_chunks = chunker.find_relevant_chunks(question, top_k=3)
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""<|system|>
Tu esi Lietuvos darbo teisės ekspertas. Atsakyk TIKSLIAI į klausimą remdamasis TIKTAI pateiktu kontekstu. 
Jei atsakymo nėra kontekste, pasakyk "Informacijos nėra pateiktame kontekste".
Atsakyk lietuvių kalba.

<|context|>
{context}

<|user|>
{question}

<|assistant|>"""

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
        return f"Error: {str(e)}"