from smolagents import ToolCallingAgent
from smolagents.models import LiteLLMModel
from rag_tool import rag_tool

class ChatAgent:
    def __init__(self, model="llama3.1:8b"):
        self.name = "Tech support question"
        self.model = LiteLLMModel(model_id=f"ollama/{model}")
        self.agent = ToolCallingAgent(
            tools=[rag_tool],
            model=self.model
        )
        self.memory = self.agent.memory

    def chat(self, message: str) -> str:
        """Main chat function with smolagents"""
        try:
            response = self.agent.run(message)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"
