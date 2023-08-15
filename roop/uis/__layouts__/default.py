import gradio

from roop.uis.__components__ import processor, execution, temp_frame, settings, source, target, preview, trim_frame, face_analyser, face_selector, output_settings, output


def render() -> gradio.Blocks:
    with gradio.Blocks() as layout:
        with gradio.Row():
            with gradio.Column(scale=2):
                processor.render()
                execution.render()
                temp_frame.render()
                settings.render()
            with gradio.Column(scale=2):
                source.render()
                target.render()
                output_settings.render()
                output.render()
            with gradio.Column(scale=3):
                preview.render()
                trim_frame.render()
                face_selector.render()
                face_analyser.render()
    return layout


def listen() -> None:
    processor.listen()
    execution.listen()
    settings.listen()
    temp_frame.listen()
    source.listen()
    target.listen()
    preview.listen()
    trim_frame.listen()
    face_selector.listen()
    face_analyser.listen()
    output_settings.listen()
    output.listen()
