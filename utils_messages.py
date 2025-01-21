import streamlit as st
from utils_openai import create_message

def load_messages(messages):
    for message in messages:
        chat = st.chat_message(message["role"])
        chat.markdown(message['content'])

def chat_user_message(prompt, messages):
    new_message = {"role": "user", "content": prompt}
    chat = st.chat_message(new_message["role"])
    chat.markdown(new_message['content'])
    messages.append(new_message)

def chat_assistant_message(messages):
    response = ""

    chat = st.chat_message("assistant")
    placeholder = chat.empty()
    stream = create_message(messages,
                            api_key=st.session_state["api_key"],
                            model=st.session_state["model"],
                            stream=True)
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
            placeholder.markdown(response)
    placeholder.markdown(response)
    messages.append({"role": "assistant", "content": response})
