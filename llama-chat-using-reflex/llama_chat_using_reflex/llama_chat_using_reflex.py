# chatapp.py
import reflex as rx
from reflex.components.el.elements.inline import Br
from reflex.components.radix.themes.base import theme

from . import style
from .state import TutorialState


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(rx.text(rx.markdown(question), text_align="left"), style=style.question_style),
        rx.box(rx.text(rx.markdown(answer), text_align="left"), style=style.answer_style),
        class_name="conv"
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            TutorialState.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.text_area(
            placeholder="Ask a question",
            value=TutorialState.question,
            on_change=TutorialState.set_question,
            style=style.input_style,
            id="ask button"
        ),
        rx.button("Ask", on_click=TutorialState.answer, style=style.button_style),
        width="50em"
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(), action_bar(),
            align="center",
        )
    )


app = rx.App()
app.add_page(index)


