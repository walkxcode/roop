import gradio

from roop.uis.__components__ import processors, execution, settings, source, target, preview, trim_frame, face_analyser, face_selector, output


def render() -> gradio.Blocks:
    with gradio.Blocks() as layout:
        with gradio.Row():
            with gradio.Column(scale=2):
                processors.render()
                execution.render()
                settings.render()
            with gradio.Column(scale=1):
                source.render()
                target.render()
            with gradio.Column(scale=3):
                preview.render()
                trim_frame.render()
                face_selector.render()
                face_analyser.render()
        with gradio.Row():
            output.render()
    return layout


def listen() -> None:
    processors.listen()
    execution.listen()
    settings.listen()
    source.listen()
    target.listen()
    preview.listen()
    trim_frame.listen()
    face_selector.listen()
    face_analyser.listen()
    output.listen()
