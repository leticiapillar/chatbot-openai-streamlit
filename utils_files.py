
import re
import pickle
from pathlib import Path
from unidecode import unidecode

PATH_MESSAGES = Path(__file__).parent/"messages"
PATH_MESSAGES.mkdir(exist_ok=True)

def get_message_name(messages):
    for m in messages:
        if m["role"] == "user":
            name = m["content"][:30]
            break
    return name

def encode_message_name(message_name):
    name = unidecode(message_name)
    return re.sub("\W+", "", name).lower()

def save_messages_file(messages):
    if len(messages) == 0:
        return
    
    message_name = get_message_name(messages)
    file_name = encode_message_name(message_name)
    file = {"file_name": file_name,
            "message_name": message_name,
            "messages": messages}
    with open(PATH_MESSAGES/file_name, "wb") as f:
        pickle.dump(file, f)

def load_messages_files():
    files = list(PATH_MESSAGES.glob("*"))
    files = sorted(files, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [f.stem for f in files]


def decode_file_name(file_name, key="message_name"):
    with open(PATH_MESSAGES/file_name, "rb") as f:
        messages = pickle.load(f)
    return messages[key]

def load_messages_by_file_name(file_name, key="messages"):
    with open(PATH_MESSAGES/file_name, "rb") as f:
        messages = pickle.load(f)
    return messages[key]
