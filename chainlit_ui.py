from chat_agent import agent
import chainlit as cl


@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    response = agent.chat(user_input)
    await cl.Message(content=response).send()
