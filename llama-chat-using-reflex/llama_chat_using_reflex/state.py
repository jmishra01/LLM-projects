# state.py
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms.ollama import Ollama

import reflex as rx

MODEL = "llama3"


class TutorialState(rx.State):

    # The current question being asked.
    question: str = """Consider you are a vertica database query expert,
    have table retails in the database, with four columns,
    Sales, profit, Region and Ship Mode.

    Write a query to fetch total sales by region where total sales is
    greator than average of total sales of ship mode.
    """

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    def set_question(self, question):
        self.question = question

    async def answer(self):

        model = Ollama(model=MODEL) | StrOutputParser()
        # Add to the answer as the chatbot responds.
        answer = ""

        if self.question == "clean":
            self.question = ""
            self.chat_history = []
            yield
        else:

            self.chat_history.append((self.question, answer))

            # Clear the question input.
            self.question = ""
            # Yield here to clear the frontend input before continuing.
            yield

            question = """
            # New User query
            ----------------
            {}
            """.format(self.chat_history[-1][0]) + """
            # Understand the context of user query using past conversation. If past conversation is not provided than 
            kindly ignore.

            """ + "\n\n".join(
                """
                user query
                -------------
                {}

                Model response
                --------------
                {}

                """.format(q, a)
                    for q, a in self.chat_history[:-1])

            answer = model.invoke(question)

            self.chat_history[-1] = (self.chat_history[-1][0], answer)
            yield  rx.scroll_to("ask button")

