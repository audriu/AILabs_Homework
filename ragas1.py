import os
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize model
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
llm = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

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
    
    system_prompt = "Tu esi Vadovybės Apsaugos Tarnybos tesininkas robotas, kuris atsako į klausimus apie tarnybos nuostatus ir teises. Atsakyk į klausimą remdamasis pateikta informacija."
    
    prompt = f"{system_prompt}\n\nDocument Content:\n{full_document}\n\nQuestion:\n{question}\n\nAnswer:"
    
    try:
        response = llm.generate_content(prompt)
        print(f"-----response {response}")
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"