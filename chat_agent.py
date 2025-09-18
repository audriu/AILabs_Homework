from smolagents import ToolCallingAgent, LiteLLMModel
from rag_tool import rag_tool


class ChatAgent(ToolCallingAgent):
    def __init__(self, model, tools=[], system_prompt=""):
        super().__init__(tools=tools, model=model)
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def chat(self, message: str) -> str:
        self.history.append({"role": "user", "content": message})
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])
        try:
            response = self.run(prompt)
            self.history.append({"role": "assistant", "content": str(response)})
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"


model = LiteLLMModel(model_id=f"ollama/llama3.1:8b")
system_prompt = "Only if the user mentions connectivity issues, ask for their country and device before troubleshooting. Otherwise, respond normally."
agent = ChatAgent(model=model, tools=[rag_tool], system_prompt=system_prompt)
