import streamlit as st
from utils_messages import load_message, chat_user_message, chat_assistant_message
from utils_files import save_messages_file

def init():
    if not "messages" in st.session_state:
        st.session_state.messages = []

def main():
    st.title("🤖 Personal Chatbot 🤖")
    st.subheader("by Asimov Academy Courses")
    st.divider()

    init()

    messages = st.session_state['messages']
    load_message(messages)
    if prompt := st.chat_input("Say something"):
        chat_user_message(prompt, messages)
        chat_assistant_message(messages)
    st.session_state['messages'] = messages
    save_messages_file(messages)

if __name__ == '__main__':
    main()