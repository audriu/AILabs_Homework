"""
Custom function for Open WebUI to handle Lithuanian Labor Code questions
Place this in Open WebUI's functions directory
"""

import requests
from typing import Dict, Any

class Function:
    def __init__(self):
        self.name = "lietuvos_darbo_kodeksas"
        self.description = "Answers questions about Lithuanian Labor Code"
    
    def pipe(self, user_message: str, model_id: str, messages: list, body: Dict[str, Any]) -> str:
        # Check if message is about Lithuanian Labor Code
        if "darbo kodekas" in user_message.lower() or "labor code" in user_message.lower():
            return f"Mock answer for Lithuanian Labor Code question: '{user_message}' - This would contain relevant information from the labor code."
        
        # Pass through to regular model if not labor code related
        return None