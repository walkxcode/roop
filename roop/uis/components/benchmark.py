from typing import Optional
import time
import gradio

import roop.globals
from roop.capturer import get_video_frame_total
from roop.core import start
from roop.uis.typing import Update
from roop.utilities import normalize_output_path, conditional_download

BENCHMARK_DATAFRAME: Optional[gradio.Dataframe] = None
BENCHMARK_BUTTON: Optional[gradio.Button] = None


def render() -> None:
    global BENCHMARK_DATAFRAME
    global BENCHMARK_BUTTON

    conditional_download('benchmark', [
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/source.jpg',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-240p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-360p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-540p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-720p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-1080p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-1440p.mp4',
        'https://huggingface.co/henryruhs/roop-benchmark/resolve/main/target-2160p.mp4'
    ])
    with gradio.Box():
        BENCHMARK_DATAFRAME = gradio.Dataframe(
            label='BENCHMARK DATA',
            headers=['target path', 'process time', 'relative fps'],
            col_count=(3, 'fixed'),
            row_count=(6, 'fixed'),
            datatype=['str', 'number', 'number']
        )
    BENCHMARK_BUTTON = gradio.Button('Benchmark')


def listen() -> None:
    BENCHMARK_BUTTON.click(update, outputs=BENCHMARK_DATAFRAME)


def update() -> Update:
    target_paths = [
        'benchmark/target-240p.mp4',
        'benchmark/target-360p.mp4',
        'benchmark/target-540p.mp4',
        'benchmark/target-720p.mp4',
        'benchmark/target-1440p.mp4',
        'benchmark/target-2160p.mp4'
    ]
    value = []
    total_runs = 3
    for target_path in target_paths:
        total_process_time = 0.0
        total_fps = 0.0
        for i in range(total_runs + 1):
            roop.globals.source_path = 'benchmark/source.jpg'
            roop.globals.target_path = target_path
            roop.globals.output_path = normalize_output_path(roop.globals.source_path, roop.globals.target_path, 'benchmark')
            video_frame_total = get_video_frame_total(roop.globals.target_path)
            if roop.globals.output_path:
                start_time = time.time()
                start()
                end_time = time.time()
                process_time = end_time - start_time
                fps = video_frame_total / process_time
                if i > 0:
                    total_process_time += process_time
                    total_fps += fps
        average_process_time = total_process_time / total_runs
        average_fps = total_fps / total_runs
        value.append([roop.globals.target_path, average_process_time, average_fps])
    return gradio.update(value=value)
