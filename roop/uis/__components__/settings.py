from typing import List, Optional
import gradio
import onnxruntime

import roop.globals
from roop.processors.frame.core import list_frame_processors_names, load_frame_processor_module, clear_frame_processors_modules
from roop.uis import core as ui
from roop.uis.typing import Update

FRAME_PROCESSORS_CHECKBOX_GROUP: Optional[gradio.CheckboxGroup] = None
EXECUTION_PROVIDERS_CHECKBOX_GROUP: Optional[gradio.CheckboxGroup] = None
EXECUTION_THREAD_COUNT_SLIDER: Optional[gradio.Slider] = None
EXECUTION_QUEUE_COUNT_SLIDER: Optional[gradio.Slider] = None
KEEP_FPS_CHECKBOX: Optional[gradio.Checkbox] = None
KEEP_TEMP_CHECKBOX: Optional[gradio.Checkbox] = None
SKIP_AUDIO_CHECKBOX: Optional[gradio.Checkbox] = None


def render() -> None:
    global FRAME_PROCESSORS_CHECKBOX_GROUP
    global EXECUTION_PROVIDERS_CHECKBOX_GROUP
    global EXECUTION_THREAD_COUNT_SLIDER
    global EXECUTION_QUEUE_COUNT_SLIDER
    global KEEP_FPS_CHECKBOX
    global KEEP_TEMP_CHECKBOX
    global SKIP_AUDIO_CHECKBOX

    with gradio.Column():
        with gradio.Box():
            FRAME_PROCESSORS_CHECKBOX_GROUP = gradio.CheckboxGroup(
                label='FRAME PROCESSORS',
                choices=sort_frame_processors(roop.globals.frame_processors),
                value=roop.globals.frame_processors
            )
            ui.register_component('frame_processors_checkbox_group', FRAME_PROCESSORS_CHECKBOX_GROUP)
        with gradio.Box():
            EXECUTION_PROVIDERS_CHECKBOX_GROUP = gradio.CheckboxGroup(
                label='EXECUTION PROVIDERS',
                choices=onnxruntime.get_available_providers(),
                value=roop.globals.execution_providers
            )
            EXECUTION_THREAD_COUNT_SLIDER = gradio.Slider(
                label='EXECUTION THREAD COUNT',
                value=roop.globals.execution_thread_count,
                step=1,
                minimum=1,
                maximum=128
            )
            EXECUTION_QUEUE_COUNT_SLIDER = gradio.Slider(
                label='EXECUTION QUEUE COUNT',
                value=roop.globals.execution_queue_count,
                step=1,
                minimum=1,
                maximum=16
            )
        with gradio.Box():
            KEEP_FPS_CHECKBOX = gradio.Checkbox(
                label='KEEP FPS',
                value=roop.globals.keep_fps
            )
            KEEP_TEMP_CHECKBOX = gradio.Checkbox(
                label='KEEP TEMP',
                value=roop.globals.keep_fps
            )
            SKIP_AUDIO_CHECKBOX = gradio.Checkbox(
                label='SKIP AUDIO',
                value=roop.globals.skip_audio
            )


def listen() -> None:
    FRAME_PROCESSORS_CHECKBOX_GROUP.change(update_frame_processors, inputs=FRAME_PROCESSORS_CHECKBOX_GROUP, outputs=FRAME_PROCESSORS_CHECKBOX_GROUP)
    EXECUTION_PROVIDERS_CHECKBOX_GROUP.change(update_execution_providers, inputs=EXECUTION_PROVIDERS_CHECKBOX_GROUP, outputs=EXECUTION_PROVIDERS_CHECKBOX_GROUP)
    EXECUTION_THREAD_COUNT_SLIDER.change(update_execution_thread_count, inputs=EXECUTION_THREAD_COUNT_SLIDER, outputs=EXECUTION_THREAD_COUNT_SLIDER)
    EXECUTION_QUEUE_COUNT_SLIDER.change(update_execution_queue_count, inputs=EXECUTION_QUEUE_COUNT_SLIDER, outputs=EXECUTION_QUEUE_COUNT_SLIDER)
    KEEP_FPS_CHECKBOX.change(lambda value: update_checkbox('keep_fps', value), inputs=KEEP_FPS_CHECKBOX, outputs=KEEP_FPS_CHECKBOX)
    KEEP_TEMP_CHECKBOX.change(lambda value: update_checkbox('keep_temp', value), inputs=KEEP_TEMP_CHECKBOX, outputs=KEEP_TEMP_CHECKBOX)
    SKIP_AUDIO_CHECKBOX.change(lambda value: update_checkbox('skip_audio', value), inputs=SKIP_AUDIO_CHECKBOX, outputs=SKIP_AUDIO_CHECKBOX)


def update_frame_processors(frame_processors: List[str]) -> Update:
    clear_frame_processors_modules()
    roop.globals.frame_processors = frame_processors
    for frame_processor in roop.globals.frame_processors:
        frame_processor_module = load_frame_processor_module(frame_processor)
        frame_processor_module.pre_check()
    return gradio.update(value=frame_processors, choices=sort_frame_processors(frame_processors))


def sort_frame_processors(frame_processors: List[str]) -> list[str]:
    frame_processor_key = lambda frame_processor: frame_processors.index(frame_processor) if frame_processor in frame_processors else len(frame_processors)
    return sorted(list_frame_processors_names(), key=frame_processor_key)


def update_execution_providers(execution_providers: List[str]) -> Update:
    roop.globals.execution_providers = execution_providers
    return gradio.update(value=execution_providers)


def update_execution_thread_count(execution_thread_count: int = 1) -> Update:
    roop.globals.execution_thread_count = execution_thread_count
    return gradio.update(value=execution_thread_count)


def update_execution_queue_count(execution_queue_count: int = 1) -> Update:
    roop.globals.execution_queue_count = execution_queue_count
    return gradio.update(value=execution_queue_count)


def update_checkbox(name: str, value: bool) -> Update:
    setattr(roop.globals, name, value)
    return gradio.update(value=value)
