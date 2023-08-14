import importlib
import sys
from typing import Dict, Optional, List, Any

import cv2
import gradio

import roop.globals
import roop.metadata
from roop.typing import Frame
from roop.uis.typing import Component, ComponentName
from roop.utilities import list_module_names

COMPONENTS: Dict[ComponentName, Component] = {}
UI_LAYOUT_METHODS = [
    'render',
    'listen'
]


def init() -> None:
    with gradio.Blocks(theme=get_theme(), title=roop.metadata.name) as ui:
        for ui_layout in roop.globals.ui_layouts:
            ui_layout_module = load_ui_layout_module(ui_layout)
            ui_layout_module.render()
            ui_layout_module.listen()
    ui.launch(inbrowser=True, show_api=False)


def load_ui_layout_module(ui_layout: str) -> Any:
    try:
        ui_layout_module = importlib.import_module(f'roop.uis.__layouts__.{ui_layout}')
        for method_name in UI_LAYOUT_METHODS:
            if not hasattr(ui_layout_module, method_name):
                raise NotImplementedError
    except ModuleNotFoundError:
        sys.exit(f'UI layout {ui_layout} could be not loaded.')
    except NotImplementedError:
        sys.exit(f'UI layout {ui_layout} not implemented correctly.')
    return ui_layout_module


def get_theme() -> gradio.Theme:
    return gradio.themes.Soft(
        primary_hue=gradio.themes.colors.red,
        secondary_hue=gradio.themes.colors.gray,
        font=gradio.themes.GoogleFont('Inter')
    ).set(
        background_fill_primary='*neutral_50',
        block_label_text_size='*text_sm',
        block_title_text_size='*text_sm'
    )


def get_component(name: ComponentName) -> Optional[Component]:
    if name in COMPONENTS:
        return COMPONENTS[name]
    return None


def register_component(name: ComponentName, component: Component) -> None:
    COMPONENTS[name] = component


def list_ui_layouts_names() -> Optional[List[str]]:
    return list_module_names('roop/uis/__layouts__')


def normalize_frame(frame: Frame) -> Frame:
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
