from typing import Optional

import gradio

import roop.choices
import roop.globals
from roop.uis import core as ui
from roop.uis.typing import Update

FACE_ANALYSER_DIRECTION_DROPDOWN: Optional[gradio.Dropdown] = None
FACE_ANALYSER_AGE_DROPDOWN: Optional[gradio.Dropdown] = None
FACE_ANALYSER_GENDER_DROPDOWN: Optional[gradio.Dropdown] = None


def render() -> None:
    global FACE_ANALYSER_DIRECTION_DROPDOWN
    global FACE_ANALYSER_AGE_DROPDOWN
    global FACE_ANALYSER_GENDER_DROPDOWN

    with gradio.Box():
        with gradio.Row():
            FACE_ANALYSER_DIRECTION_DROPDOWN = gradio.Dropdown(
                label='FACE ANALYSER DIRECTION',
                choices=roop.choices.face_analyser_direction,
                value=roop.globals.face_analyser_direction
            )
            FACE_ANALYSER_AGE_DROPDOWN = gradio.Dropdown(
                label='FACE ANALYSER AGE',
                choices=['none'] + roop.choices.face_analyser_age,
                value=roop.globals.face_analyser_age or 'none'
            )
            FACE_ANALYSER_GENDER_DROPDOWN = gradio.Dropdown(
                label='FACE ANALYSER GENDER',
                choices=['none'] + roop.choices.face_analyser_gender,
                value=roop.globals.face_analyser_gender or 'none'
            )
        ui.register_component('face_analyser_direction_dropdown', FACE_ANALYSER_DIRECTION_DROPDOWN)
        ui.register_component('face_analyser_age_dropdown', FACE_ANALYSER_AGE_DROPDOWN)
        ui.register_component('face_analyser_gender_dropdown', FACE_ANALYSER_GENDER_DROPDOWN)


def listen() -> None:
    FACE_ANALYSER_DIRECTION_DROPDOWN.select(lambda value: update_dropdown('face_analyser_direction', value), inputs=FACE_ANALYSER_DIRECTION_DROPDOWN, outputs=FACE_ANALYSER_DIRECTION_DROPDOWN)
    FACE_ANALYSER_AGE_DROPDOWN.select(lambda value: update_dropdown('face_analyser_age', value), inputs=FACE_ANALYSER_AGE_DROPDOWN, outputs=FACE_ANALYSER_AGE_DROPDOWN)
    FACE_ANALYSER_GENDER_DROPDOWN.select(lambda value: update_dropdown('face_analyser_gender', value), inputs=FACE_ANALYSER_GENDER_DROPDOWN, outputs=FACE_ANALYSER_GENDER_DROPDOWN)


def update_dropdown(name: str, value: str) -> Update:
    if value == 'none':
        setattr(roop.globals, name, None)
    else:
        setattr(roop.globals, name, value)
    return gradio.update(value=value)
