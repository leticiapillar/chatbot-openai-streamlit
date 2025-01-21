
import re
import pickle
from pathlib import Path
from unidecode import unidecode

PATH_MESSAGES = Path(__file__).parent/"messages"
PATH_MESSAGES.mkdir(exist_ok=True)
PATH_CONFIGS = Path(__file__).parent/"configs"
PATH_CONFIGS.mkdir(exist_ok=True)
CACHE_FILE_NAMES = {}

def get_message_name(messages):
    for m in messages:
        if m["role"] == "user":
            name = m["content"][:30]
            break
    return name

def encode_file_name(message_name):
    name = unidecode(message_name)
    return re.sub("\W+", "", name).lower()

def decode_file_name(file_name):
    if not file_name in CACHE_FILE_NAMES:
       message_name = get_content_of_file(file_name, key="message_name")
       CACHE_FILE_NAMES[file_name] = message_name
    return CACHE_FILE_NAMES[file_name]

def save_messages_file(messages):
    if len(messages) == 0:
        return
    
    message_name = get_message_name(messages)
    file_name = encode_file_name(message_name)
    file = {"file_name": file_name,
            "message_name": message_name,
            "messages": messages}
    with open(PATH_MESSAGES/file_name, "wb") as f:
        pickle.dump(file, f)

def load_messages_files():
    files = list(PATH_MESSAGES.glob("*"))
    files = sorted(files, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [f.stem for f in files]

def get_content_of_file(file_name, key="messages"):
    with open(PATH_MESSAGES/file_name, "rb") as f:
        messages = pickle.load(f)
    return messages[key]

def save_api_key(api_key):
    with open(PATH_CONFIGS/"key", "wb") as f:
        pickle.dump(api_key,f)

def load_api_key():
    if (PATH_CONFIGS/"key").exists():
        with open(PATH_CONFIGS/"key", "rb") as f:
            return pickle.load(f)
    return ""
