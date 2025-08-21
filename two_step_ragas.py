import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:4b"

full_document = ""

def load_pdf(file_path):
    global full_document
    import PyPDF2
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    full_document = text
    return f"Loaded document ({len(text)} characters)"

def find_relevant_sections(question):
    """First step: Find relevant sections in the document"""
    
    # Split document into sections (by articles, chapters, etc.)
    sections = re.split(r'\n(?=\d+\s*straipsnis|SKYRIUS)', full_document)
    
    search_prompt = f"""Iš šių dokumento sekcijų, kurios 3 labiausiai susijusios su klausimu: "{question}"?
Atsakyk tik sekcijų numeriais (pvz: 1, 3, 7):

{chr(10).join([f"{i+1}. {section[:200]}..." for i, section in enumerate(sections[:20])])}"""

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": search_prompt,
            "stream": False,
            "options": {"temperature": 0}
        }
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json().get('response', '')
        
        # Extract section numbers
        numbers = re.findall(r'\b(\d+)\b', result)
        relevant_sections = []
        for num in numbers[:3]:
            idx = int(num) - 1
            if 0 <= idx < len(sections):
                relevant_sections.append(sections[idx])
        
        return relevant_sections
    except:
        return sections[:3]  # Fallback

def generate_answer(question):
    if not full_document:
        load_pdf("aktai/Darbo_Kodeksas.pdf")
    
    # Step 1: Find relevant sections
    relevant_sections = find_relevant_sections(question)
    context = "\n\n".join(relevant_sections)
    
    # Step 2: Answer based on relevant sections
    prompt = f"""<|system|>
Tu esi Lietuvos darbo teisės ekspertas. Atsakyk į klausimą remdamasis tik pateiktu kontekstu.
Jei atsakymo nėra, pasakyk "Informacijos nėra pateiktame kontekste".

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
            "options": {"temperature": 0.1}
        }
        response = requests.post(OLLAMA_URL, json=payload)
        return response.json().get('response', 'No response generated')
    except Exception as e:
        return f"Error: {str(e)}"