from smolagents import (
    load_tool,
    CodeAgent,
    InferenceClientModel,
    GradioUI
)

from chat_agent import ChatAgent
agent = ChatAgent()

GradioUI(agent).launch()