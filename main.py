from flask import Flask, render_template, request, jsonify
from chat_agent import ChatAgent

app = Flask(__name__)
agent = ChatAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    response = agent.chat(message)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
