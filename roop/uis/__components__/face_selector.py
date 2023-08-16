from typing import List, Optional, Tuple, Any, Dict
from time import sleep

import cv2
import gradio

import roop.choices
import roop.globals
from roop.capturer import get_video_frame
from roop.face_analyser import get_many_faces
from roop.face_reference import clear_face_reference
from roop.typing import Frame, FaceRecognition
from roop.uis import core as ui
from roop.uis.typing import ComponentName, Update
from roop.utilities import is_image, is_video

FACE_RECOGNITION_DROPDOWN: Optional[gradio.Dropdown] = None
REFERENCE_FACE_POSITION_GALLERY: Optional[gradio.Gallery] = None
REFERENCE_FACE_DISTANCE_SLIDER: Optional[gradio.Slider] = None


def render() -> None:
    global FACE_RECOGNITION_DROPDOWN
    global REFERENCE_FACE_POSITION_GALLERY
    global REFERENCE_FACE_DISTANCE_SLIDER

    with gradio.Box():
        reference_face_gallery_args: Dict[str, Any] = {
            'label': 'REFERENCE FACE',
            'height': 120,
            'object_fit': 'cover',
            'columns': 10,
            'allow_preview': False,
            'visible': 'reference' in roop.globals.face_recognition
        }
        if is_image(roop.globals.target_path):
            reference_frame = cv2.imread(roop.globals.target_path)
            reference_face_gallery_args['value'] = extract_gallery_frames(reference_frame)
        if is_video(roop.globals.target_path):
            reference_frame = get_video_frame(roop.globals.target_path, roop.globals.reference_frame_number)
            reference_face_gallery_args['value'] = extract_gallery_frames(reference_frame)
        FACE_RECOGNITION_DROPDOWN = gradio.Dropdown(
            label='FACE RECOGNITION',
            choices=roop.choices.face_recognition,
            value=roop.globals.face_recognition
        )
        REFERENCE_FACE_POSITION_GALLERY = gradio.Gallery(**reference_face_gallery_args)
        REFERENCE_FACE_DISTANCE_SLIDER = gradio.Slider(
            label='REFERENCE FACE DISTANCE',
            value=roop.globals.reference_face_distance,
            maximum=3,
            step=0.05,
            visible='reference' in roop.globals.face_recognition
        )
        ui.register_component('face_recognition_dropdown', FACE_RECOGNITION_DROPDOWN)
        ui.register_component('reference_face_position_gallery', REFERENCE_FACE_POSITION_GALLERY)
        ui.register_component('reference_face_distance_slider', REFERENCE_FACE_DISTANCE_SLIDER)


def listen() -> None:
    FACE_RECOGNITION_DROPDOWN.select(update_face_recognition, inputs=FACE_RECOGNITION_DROPDOWN, outputs=[REFERENCE_FACE_POSITION_GALLERY, REFERENCE_FACE_DISTANCE_SLIDER])
    REFERENCE_FACE_POSITION_GALLERY.select(clear_and_update_face_reference_position)
    REFERENCE_FACE_DISTANCE_SLIDER.change(update_reference_face_distance, inputs=REFERENCE_FACE_DISTANCE_SLIDER)
    update_component_names: List[ComponentName] = [
        'target_file',
        'preview_frame_slider'
    ]
    for component_name in update_component_names:
        component = ui.get_component(component_name)
        if component:
            component.change(update_face_reference_position, outputs=REFERENCE_FACE_POSITION_GALLERY)
    select_component_names: List[ComponentName] = [
        'face_analyser_direction_dropdown',
        'face_analyser_age_dropdown',
        'face_analyser_gender_dropdown'
    ]
    for component_name in select_component_names:
        component = ui.get_component(component_name)
        if component:
            component.select(update_face_reference_position, outputs=REFERENCE_FACE_POSITION_GALLERY)


def update_face_recognition(face_recognition: FaceRecognition) -> Tuple[Update, Update]:
    if face_recognition == 'reference':
        roop.globals.face_recognition = face_recognition
        return gradio.update(visible=True), gradio.update(visible=True)
    if face_recognition == 'many':
        roop.globals.face_recognition = face_recognition
        return gradio.update(visible=False), gradio.update(visible=False)


def clear_and_update_face_reference_position(event: gradio.SelectData) -> Update:
    clear_face_reference()
    return update_face_reference_position(event.index)


def update_face_reference_position(reference_face_position: int = 0) -> Update:
    sleep(0.2)
    gallery_frames = []
    roop.globals.reference_face_position = reference_face_position
    if is_image(roop.globals.target_path):
        reference_frame = cv2.imread(roop.globals.target_path)
        gallery_frames = extract_gallery_frames(reference_frame)
    if is_video(roop.globals.target_path):
        reference_frame = get_video_frame(roop.globals.target_path, roop.globals.reference_frame_number)
        gallery_frames = extract_gallery_frames(reference_frame)
    if gallery_frames:
        return gradio.update(value=gallery_frames)
    return gradio.update(value=None)


def update_reference_face_distance(reference_face_distance: float) -> Update:
    roop.globals.reference_face_distance = reference_face_distance
    return gradio.update(value=reference_face_distance)


def extract_gallery_frames(reference_frame: Frame) -> List[Frame]:
    crop_frames = []
    faces = get_many_faces(reference_frame)
    for face in faces:
        start_x, start_y, end_x, end_y = map(int, face['bbox'])
        crop_frame = reference_frame[start_y:end_y, start_x:end_x]
        crop_frames.append(ui.normalize_frame(crop_frame))
    return crop_frames
