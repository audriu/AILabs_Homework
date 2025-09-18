from flask import Flask, render_template, request, jsonify
from smolagents import AgentMemory, LiteLLMModel

from chat_agent import ChatAgent
from rag_tool import rag_tool

app = Flask(__name__)
model = LiteLLMModel(model_id=f"ollama/llama3.1:8b")
agent = ChatAgent(model=model, tools=[rag_tool])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    response = agent.chat(message)
    print("----------------------------------------------0")
    print(response)
    print("----------------------------------------------1")
    memory: AgentMemory = agent.memory
    print(memory.get_full_steps())
    print("----------------------------------------------2")
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
