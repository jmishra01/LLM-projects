import reflex as rx
from rxconfig import config

from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser

MODEL = "llama3"

class Chat:
    def __init__(self) -> None:
        self.model = Ollama(model=MODEL) | StrOutputParser()

    def inference(self, prompt):
        return self.model.invoke(prompt)


class State(rx.State):
    sample: str = """Consider you are a database expert. You have a database, have retail table in it.
    Table container column mention below.

    * Sales
    * Region
    * Ship Mode
    * Channel

    You have to create Only SQL query without description for user prompt.

    # User prompt
    Fetch total sales by region with following condition

    * Total Sales of region is greater than Average of total Sales by Ship Mode
    * Region start with 'st' characters
    """
    value: str = ""
    text: str = "**Inference will be shown here.**"
    prompt: str = ""

    def set_value(self):
        self.clear()
        self.value = self.sample
        self.prompt = self.value

    def set_text(self, prompt):
        self.prompt = prompt

    def inference(self):
        chat: Chat = Chat()
        print(self.prompt)

        if self.prompt:
            self.prompt += """

            * If response is SQL than give response in below format
            ```sql
            # mention sql query here
            ```
            """
            self.text = chat.inference(self.prompt)
        print('-'*30)
        print(self.text)

    def clear(self):
        self.text = ""
        self.value = ""
        self.prompt = ""

def inference_area():
    return rx.container(
        rx.scroll_area(
            rx.text(rx.markdown(State.text), width="100%")
        ),
        width="100%", height="20em")

def prompt_area():
    return rx.vstack(
        rx.text_area(
            value=State.value,
            width="100%", height="18em",
            on_change=State.set_text, margin="1px"),
        rx.hstack(
            rx.button("Submit", on_click=State.inference),
            rx.button("Sample", on_click=State.set_value),
            rx.button("Clear", on_click=State.clear),
            margin="2px"
        ),
        width="100%",
        margin="3px",
        border="solid 1px #333"
    )


def index():
    return rx.container(
        rx.vstack(
            rx.heading("Llama UI", 
                       align="center",
                       margin_left="22em"
                       ),
            prompt_area(),
            inference_area()
        ),
        size="4"
    )


app = rx.App()
app.add_page(index)
