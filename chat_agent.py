from smolagents import ToolCallingAgent, tool
from smolagents.models import LiteLLMModel

@tool
def lietuvos_darbo_kodeksas_tool(question: str) -> str:
    """Atsako į klausimus apie Lietuvos darbo kodeksą
    
    Args:
        question: Klausimas apie Lietuvos darbo kodeksą
    """
    return f"Bandomasis atsakymas į Lietuvos darbo kodekso klausimą: '{question}' - Čia būtų pateikta reikiama informacija iš darbo kodekso."

class ChatAgent:
    def __init__(self, model="alibayram/erurollm-9b-instruct"):
        self.model = LiteLLMModel(model_id=f"ollama/{model}")
        self.agent = ToolCallingAgent(
            tools=[lietuvos_darbo_kodeksas_tool],
            model=self.model
        )
    
    def chat(self, message: str) -> str:
        """Main chat function with smolagents"""
        system_prompt = f"""Tu esi Vadovybės Apsaugos Tarnybos tesininkas robotas, kuris atsako į klausimus apie tarnybos nuostatus ir teises.
        Atsakyk į klausimą remdamasis pateikta informacija. Naudotojas paklausė šio klausimo: {message}"""

        try:
            response = self.agent.run(system_prompt)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"