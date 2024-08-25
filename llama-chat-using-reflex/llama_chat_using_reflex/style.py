import reflex as rx

# Common styles for questions and answers.
shadow = "rgba(100, 100, 250, 1) 2px 2px 10px"
chat_margin = "50%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)

# Set specific styles for questions and answers.
question_style = rx.Style(message_style | dict(
    background_color=rx.color("gray", 4),
    margin_left=chat_margin,
    margin_right=0,

))
answer_style = rx.Style(message_style | dict(
    background_color=rx.color("accent", 8),
    margin_right=chat_margin,
    margin_left=0
))

# Styles for the action bar.
input_style = rx.Style(dict(
    border="solid 1px #444",
    padding=".1em",
    box_shadow=shadow,
    width="90%",
    height="5em"
))
button_style = rx.Style(dict(
    background_color=rx.color("accent", 10),
    box_shadow=shadow,
    width="8em",
    height="5em"
))
