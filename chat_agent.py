from smolagents import ToolCallingAgent


class ChatAgent(ToolCallingAgent):
    def __init__(self, model, tools=[]):
        super().__init__(
            tools=tools,
            model=model
        )

    def chat(self, message: str) -> str:
        """Main chat function with smolagents"""
        try:
            response = self.run(message)
            return str(response)
        except Exception as e:
            return f"Error: {str(e)}"
