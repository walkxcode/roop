import gradio

from roop.uis.components import processor, execution, benchmark


def render() -> gradio.Blocks:
    with gradio.Blocks() as layout:
        with gradio.Row():
            with gradio.Column(scale=2):
                processor.render()
                execution.render()
            with gradio.Column(scale=5):
                benchmark.render()
    return layout


def listen() -> None:
    processor.listen()
    execution.listen()
    benchmark.listen()
