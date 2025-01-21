import streamlit as st
from utils_messages import load_messages, chat_user_message, chat_assistant_message
from utils_files import save_messages_file, load_messages_files, decode_file_name, get_content_of_file, save_api_key, load_api_key

def init():
    if not "messages" in st.session_state:
        st.session_state.messages = []
    if not "model" in st.session_state:
        st.session_state.model = "gpt-4o-mini"
    if not "api_key" in st.session_state:
        st.session_state.api_key = load_api_key()
    if not "current_chat" in st.session_state:
        st.session_state.current_chat = ""

def tab_chat(tab):
    tab.button("💬 New Chat", 
                  type="secondary", 
                  use_container_width=True,
                  on_click=load_chat, 
                  args=("", ))

    tab.markdown("")
    files = load_messages_files()
    for file_name in files:
        name_decode = decode_file_name(file_name)
        tab.button(name_decode, 
                   type="tertiary", 
                   use_container_width=True,
                   on_click=load_chat,
                   args=(file_name, ),
                   disabled=file_name==st.session_state["current_chat"])

def load_chat(file_name):
    if file_name == "":
        st.session_state['messages'] = []
    else:
        messages = get_content_of_file(file_name)
        st.session_state['messages'] = messages
    st.session_state["current_chat"] = file_name

def tab_configs(tab):
    model_selected = tab.selectbox("Model", 
                                   ["gpt-4o", "gpt-4o-mini"])
    st.session_state["model"] = model_selected

    api_key = tab.text_input("Add your api key", value=st.session_state["api_key"])
    if api_key != st.session_state["api_key"]:
        st.session_state["api_key"] = api_key
        save_api_key(api_key)
        tab.success("API Key saved")

def chat_page():
    messages = st.session_state['messages']
    load_messages(messages)
    if prompt := st.chat_input("Say something"):
        chat_user_message(prompt, messages)
        chat_assistant_message(messages)
    st.session_state['messages'] = messages
    save_messages_file(messages)

def main():
    st.title("🤖 Personal Chatbot 🤖")
    st.subheader("by Asimov Academy Courses")
    st.divider()

    init()
    chat_page()


    tab1, tab2 = st.sidebar.tabs(["Chats", "Configs"])
    tab_chat(tab1)
    tab_configs(tab2)


if __name__ == '__main__':
    main()