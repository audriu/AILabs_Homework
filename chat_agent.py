from smolagents import ToolCallingAgent


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
