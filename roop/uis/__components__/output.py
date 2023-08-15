from typing import Tuple, Optional
import gradio

import roop.globals
from roop.core import start
from roop.uis.typing import Update
from roop.utilities import is_image, is_video, normalize_output_path

START_BUTTON: Optional[gradio.Button] = None
CLEAR_BUTTON: Optional[gradio.Button] = None
OUTPUT_IMAGE: Optional[gradio.Image] = None
OUTPUT_VIDEO: Optional[gradio.Video] = None


def render() -> None:
    global START_BUTTON
    global CLEAR_BUTTON
    global OUTPUT_IMAGE
    global OUTPUT_VIDEO

    with gradio.Column():
        with gradio.Row():
            START_BUTTON = gradio.Button('Start')
            CLEAR_BUTTON = gradio.Button('Clear')
        OUTPUT_IMAGE = gradio.Image(
            label='OUTPUT',
            visible=False
        )
        OUTPUT_VIDEO = gradio.Video(
            label='OUTPUT',
            visible=False
        )


def listen() -> None:
    START_BUTTON.click(update, outputs=[OUTPUT_IMAGE, OUTPUT_VIDEO])
    CLEAR_BUTTON.click(clear, outputs=[OUTPUT_IMAGE, OUTPUT_VIDEO])


def update() -> Tuple[Update, Update]:
    roop.globals.output_path = normalize_output_path(roop.globals.source_path, roop.globals.target_path, '..')
    if roop.globals.output_path:
        start()
        if is_image(roop.globals.output_path):
            return gradio.update(value=roop.globals.output_path, visible=True), gradio.update(value=None, visible=False)
        if is_video(roop.globals.output_path):
            return gradio.update(value=None, visible=False), gradio.update(value=roop.globals.output_path, visible=True)
    return gradio.update(value=None, visible=False), gradio.update(value=None, visible=False)


def clear() -> Tuple[Update, Update]:
    return gradio.update(value=None, visible=False), gradio.update(value=None, visible=False)
