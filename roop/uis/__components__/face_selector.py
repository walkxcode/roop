from typing import List, Optional
from time import sleep

import cv2
import gradio

import roop.globals
from roop.capturer import get_video_frame
from roop.face_analyser import get_many_faces
from roop.face_reference import clear_face_reference
from roop.uis import core as ui
from roop.uis.typing import ComponentName, Update
from roop.utilities import is_image, is_video

REFERENCE_FACE_POSITION_GALLERY: Optional[gradio.Gallery] = None
SIMILAR_FACE_DISTANCE_SLIDER: Optional[gradio.Slider] = None


def render() -> None:
    global REFERENCE_FACE_POSITION_GALLERY
    global SIMILAR_FACE_DISTANCE_SLIDER

    with gradio.Box():
        reference_face_gallery_args = {
            'label': 'REFERENCE FACE',
            'height': 120,
            'object_fit': 'cover',
            'columns': 10,
            'allow_preview': False,
            'visible': True
        }
        faces = []
        if is_image(roop.globals.target_path):
            reference_frame = cv2.imread(roop.globals.target_path)
            faces = get_many_faces(reference_frame)
        if is_video(roop.globals.target_path):
            reference_frame = get_video_frame(roop.globals.target_path, roop.globals.reference_frame_number)
            faces = get_many_faces(reference_frame)
        if faces:
            value = []
            for face in faces:
                start_x, start_y, end_x, end_y = map(int, face['bbox'])
                crop_frame = reference_frame[start_y:end_y, start_x:end_x]
                value.append(ui.normalize_frame(crop_frame))
            reference_face_gallery_args['value'] = value
        else:
            reference_face_gallery_args['value'] = []
        REFERENCE_FACE_POSITION_GALLERY = gradio.Gallery(**reference_face_gallery_args)
        SIMILAR_FACE_DISTANCE_SLIDER = gradio.Slider(
            label='SIMILAR FACE DISTANCE',
            value=roop.globals.similar_face_distance,
            maximum=2,
            step=0.05
        )
        ui.register_component('reference_face_position_gallery', REFERENCE_FACE_POSITION_GALLERY)
        ui.register_component('similar_face_distance_slider', SIMILAR_FACE_DISTANCE_SLIDER)


def listen() -> None:
    REFERENCE_FACE_POSITION_GALLERY.select(clear_and_update_face_reference_position, outputs=REFERENCE_FACE_POSITION_GALLERY)
    SIMILAR_FACE_DISTANCE_SLIDER.change(update_similar_face_distance, inputs=SIMILAR_FACE_DISTANCE_SLIDER)
    component_names: List[ComponentName] = [
        'target_file',
        'preview_frame_slider'
    ]
    for component_name in component_names:
        component = ui.get_component(component_name)
        if component:
            component.change(update_face_reference_position, outputs=REFERENCE_FACE_POSITION_GALLERY)


def clear_and_update_face_reference_position(event: gradio.SelectData) -> Update:
    clear_face_reference()
    return update_face_reference_position(event.index)


def update_face_reference_position(reference_face_position: int = 0) -> Update:
    sleep(0.2)
    roop.globals.reference_face_position = reference_face_position
    faces = []
    if is_image(roop.globals.target_path):
        reference_frame = cv2.imread(roop.globals.target_path)
        faces = get_many_faces(reference_frame)
    if is_video(roop.globals.target_path):
        reference_frame = get_video_frame(roop.globals.target_path, roop.globals.reference_frame_number)
        faces = get_many_faces(reference_frame)
    if faces:
        value = []
        for face in faces:
            start_x, start_y, end_x, end_y = map(int, face['bbox'])
            crop_frame = reference_frame[start_y:end_y, start_x:end_x]
            value.append(ui.normalize_frame(crop_frame))
        return gradio.update(value=value)
    return gradio.update(value=None)


def update_similar_face_distance(similar_face_distance: float) -> Update:
    roop.globals.similar_face_distance = similar_face_distance
    return gradio.update(value=similar_face_distance)
