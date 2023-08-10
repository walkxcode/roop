from typing import Literal, Dict, Any
import gradio

Component = gradio.File or gradio.Image or gradio.Video or gradio.Slider
ComponentName = Literal[
    'source_file',
    'target_file',
    'preview_frame_slider',
    'reference_face_position_gallery',
    'similar_face_distance_slider',
    'frame_processors_checkbox_group',
    'many_faces_checkbox'
]
Update = Dict[Any, Any]
