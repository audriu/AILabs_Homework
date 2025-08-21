from smolagents import ToolCallingAgent, tool
from smolagents.models import LiteLLMModel

@tool
def lietuvos_darbo_kodeksas_tool(question: str) -> str:
    """Answers questions about Lithuanian Labor Code (Lietuvos darbo kodeksas)
    
    Args:
        question: The question about Lithuanian Labor Code
    """
    return f"Mock answer for Lithuanian Labor Code question: '{question}' - This would contain relevant information from the labor code."

class ChatAgent:
    def __init__(self, model="alibayram/erurollm-9b-instruct"):
        self.model = LiteLLMModel(model_id=f"ollama/{model}")
        self.agent = ToolCallingAgent(
            tools=[lietuvos_darbo_kodeksas_tool],
            model=self.model
        )
    
    def chat(self, message: str) -> str:
        """Main chat function with smolagents"""
        try:
            response = self.agent.run(message)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"