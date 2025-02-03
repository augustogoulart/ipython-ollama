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
    def explain(self, search):
        # I can access the shell's history. Now how do I make it readable into ollama?
        pattern = "*"
        if search:
            pattern = "*" + search + "*"

        shell_context = "\n".join(
            f"{i}" for _, _, i in self.shell.history_manager.get_range_by_str("")
        )

        stream: ChatResponse = chat(
            model="llama3.2:1b",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        This is a Python REPL context: {shell_context}.
                        Try to understand what the user is doing and provide fixes for any errors you encounter.
                        Assume you response is going to be used during a debugging session, so be short on your
                        answers.
                        """,
                },
            ],
        )
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
