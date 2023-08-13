from typing import List, Optional
import gradio

import roop.globals
from roop.processors.frame.core import list_frame_processors_names, load_frame_processor_module, clear_frame_processors_modules
from roop.uis import core as ui
from roop.uis.typing import Update

FRAME_PROCESSORS_CHECKBOX_GROUP: Optional[gradio.CheckboxGroup] = None


def render() -> None:
    global FRAME_PROCESSORS_CHECKBOX_GROUP

    with gradio.Box():
        FRAME_PROCESSORS_CHECKBOX_GROUP = gradio.CheckboxGroup(
            label='FRAME PROCESSORS',
            choices=sort_frame_processors(roop.globals.frame_processors),
            value=roop.globals.frame_processors
        )
        ui.register_component('frame_processors_checkbox_group', FRAME_PROCESSORS_CHECKBOX_GROUP)


def listen() -> None:
    FRAME_PROCESSORS_CHECKBOX_GROUP.change(update_frame_processors, inputs=FRAME_PROCESSORS_CHECKBOX_GROUP, outputs=FRAME_PROCESSORS_CHECKBOX_GROUP)


def update_frame_processors(frame_processors: List[str]) -> Update:
    clear_frame_processors_modules()
    roop.globals.frame_processors = frame_processors
    for frame_processor in roop.globals.frame_processors:
        frame_processor_module = load_frame_processor_module(frame_processor)
        frame_processor_module.pre_check()
    return gradio.update(value=frame_processors, choices=sort_frame_processors(frame_processors))


def sort_frame_processors(frame_processors: List[str]) -> list[str]:
    return sorted(list_frame_processors_names(), key=lambda frame_processor: frame_processors.index(frame_processor) if frame_processor in frame_processors else len(frame_processors))
