import argparse

import ollama
from ollama._types import Message, ResponseError

from typing import List

import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

from rich.console import Console
from rich.markdown import Markdown


def pretty_json(resp):
    js_str = json.dumps(resp, indent=4, sort_keys=True)
    print(highlight(js_str, JsonLexer(), TerminalFormatter()))

def print_context(resp):
    content = resp["message"]["content"]
    console = Console()
    console.print(Markdown(content))


parser = argparse.ArgumentParser()

parser.add_argument("-f", default="nofull" ,type=str, help="Print content with JSON response received from LLM model.")
parser.add_argument("-l", default="Python" ,type=str, help="Pass programming lang name.")
parser.add_argument("-m", default="llama3" ,type=str, help="Pass LLM model name.")
arg = parser.parse_args()

lang = arg.l
model = arg.m

messages: List[Message] = [Message(role="system", content=f"Consider you are a {lang} programmer."),
                                  Message(role="user", content="Write a Fibonacci series code.")]
try:
    response = ollama.chat(
        model=model,
        messages=messages
    )
    if arg.f == 'full':
        pretty_json(response)
    print_context(response)
except ResponseError:
    model_list = [i["name"] for i in ollama.list()["models"]]
    print("List of models:")
    pretty_json(model_list)
    if not model_list:
        print("Kindly visit Ollama website to know the list of models available.")
