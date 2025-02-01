"""
This module defines the ``%explain`` IPython magic.

"""

import sys

from IPython.core.magic import Magics, magics_class, line_magic

from ollama import chat
from ollama import ChatResponse


@magics_class
class LLMMagics(Magics):
    @line_magic
    def explain(self, line):
        if not line:
            line = sys.last_value

        stream: ChatResponse = chat(
            model="llama3.2:1b",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": f"You are a pragmatic software engineer. Explain what is {line}",
                },
            ],
        )
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
