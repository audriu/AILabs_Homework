from smolagents import ToolCallingAgent, tool
from smolagents.models import LiteLLMModel
from improved_ragas import generate_answer


@tool
def lietuvos_darbo_kodeksas_tool(question: str) -> str:
    """Atsako į klausimus apie Lietuvos darbo kodeksą. Visus klausimus susijusius su Lietuvos darbo teise.
    
    Args:
        question: Klausimas apie Lietuvos darbo kodeksą
    """
    print(f" =========== question {question}")
    answer = generate_answer(question)
    print(f" =========== answer {answer}")
    return answer


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
