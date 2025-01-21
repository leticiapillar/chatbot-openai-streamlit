from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def create_message(messages, api_key, model="gpt-4o-mini", max_tokens=1000, temperature=0, stream=False):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
    )
    return response

