import streamlit as st
from utils_messages import load_messages, chat_user_message, chat_assistant_message
from utils_files import save_messages_file, load_messages_files, decode_file_name, load_messages_by_file_name

def init():
    if not "messages" in st.session_state:
        st.session_state.messages = []

def tab_chat(tab):
    if tab.button("New Chat", type="secondary", use_container_width=True):
        tab.write("new chat ...")

    files = load_messages_files()
    for file_name in files:
        name_decode = decode_file_name(file_name)
        tab.button(name_decode, 
                   type="tertiary", 
                   use_container_width=True,
                   on_click=load_chat(file_name))

def load_chat(file_name):
    messages = load_messages_by_file_name(file_name)
    st.session_state['messages'] = messages

def main():
    st.title("🤖 Personal Chatbot 🤖")
    st.subheader("by Asimov Academy Courses")
    st.divider()

    init()

    messages = st.session_state['messages']
    load_messages(messages)
    if prompt := st.chat_input("Say something"):
        chat_user_message(prompt, messages)
        chat_assistant_message(messages)
    st.session_state['messages'] = messages
    save_messages_file(messages)

    tab1, tab2 = st.sidebar.tabs(["Chats", "Configs"])
    tab_chat(tab1)


if __name__ == '__main__':
    main()