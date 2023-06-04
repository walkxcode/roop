import tkinter as tk
import customtkinter as CTk
from typing import Any, Callable, Tuple
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
import threading

from roop.utils import is_img

CTk.set_appearance_mode("System")
CTk.set_default_color_theme("dark-blue")

max_preview_size = 800

def create_preview(parent):
    global preview_image_frame, preview_frame_slider, test_button

    preview_window = CTk.CTkToplevel(parent)
    # Override close button
    preview_window.protocol("WM_DELETE_WINDOW", hide_preview)
    preview_window.withdraw()
    preview_window.title("Preview")
    preview_window.configure(bg_color="#1E1E1E")
    preview_window.resizable(width=False, height=False)

    frame = CTk.CTkFrame(preview_window)
    frame.pack(fill='both', side='left', expand='True')

    # Preview image
    preview_image_frame = CTk.CTkLabel(frame, width=180, height=180, text="")
    preview_image_frame.pack(side='top')

    # Bottom frame
    buttons_frame = CTk.CTkFrame(frame, bg_color="#292929")
    buttons_frame.pack(fill='both', side='bottom')

    current_frame = CTk.IntVar()
    preview_frame_slider = CTk.CTkSlider(
        buttons_frame,
        variable=current_frame,
        bg_color="#292929",
        fg_color="#CCCCCC",
    )
    preview_frame_slider.pack(fill='both', side='left', expand='True')

    test_button = CTk.CTkButton(buttons_frame, text="Render Frame", width=15, text_color="#1E1E1E", fg_color="#3BFFCB", hover_color="#09B587")
    test_button.pack(side='right', fill='y')
    return preview_window


def show_preview():
    preview.deiconify()
    preview_visible.set(True)


def hide_preview():
    preview.withdraw()
    preview_visible.set(False)


def set_preview_handler(test_handler):
    test_button.configure(command = test_handler)


def init_slider(frames_count, change_handler):
    preview_frame_slider.configure(to=frames_count, command=lambda value: change_handler(preview_frame_slider.get()))
    preview_frame_slider.set(0)


def update_preview(frame):
    img = Image.fromarray(frame)
    width, height = img.size
    aspect_ratio = 1
    if width > height:
        aspect_ratio = max_preview_size / width
    else:
        aspect_ratio = max_preview_size / height
    img = img.resize(
        (
            int(width * aspect_ratio),
            int(height * aspect_ratio)
        ),
        Image.ANTIALIAS
    )
    photo_img = ImageTk.PhotoImage(img)
    preview_image_frame.configure(image=photo_img)
    preview_image_frame.image = photo_img


def select_face(select_face_handler: Callable[[str], None]):
    if select_face_handler:
        path = filedialog.askopenfilename(title="Select a face")
        preview_face(path)
        return select_face_handler(path)
    return None


def update_slider_handler(get_video_frame, video_path):
    return lambda frame_number: update_preview(get_video_frame(video_path, frame_number))


def test_preview(create_test_preview):
    frame = create_test_preview(preview_frame_slider.get())
    update_preview(frame)


def update_slider(get_video_frame, create_test_preview, video_path, frames_amount):
    init_slider(frames_amount, update_slider_handler(get_video_frame, video_path))
    set_preview_handler(lambda: preview_thread(lambda: test_preview(create_test_preview)))


def analyze_target(select_target_handler: Callable[[str], Tuple[int, Any]], target_path: CTk.StringVar, frames_amount: CTk.IntVar):
    path = filedialog.askopenfilename(title="Select a target")
    target_path.set(path)
    amount, frame = select_target_handler(path)
    frames_amount.set(amount)
    preview_target(frame)
    update_preview(frame)


def select_target(select_target_handler: Callable[[str], Tuple[int, Any]], target_path: CTk.StringVar, frames_amount: CTk.IntVar):
    if select_target_handler:
        analyze_target(select_target_handler, target_path, frames_amount)


def save_file(save_file_handler: Callable[[str], None], target_path: str):
    filename, ext = 'output.mp4', '.mp4'

    if is_img(target_path):
        filename, ext = 'output.png', '.png'

    if save_file_handler:
        return save_file_handler(asksaveasfilename(initialfile=filename, defaultextension=ext, filetypes=[("All Files","*.*"),("Videos","*.mp4")]))
    return None


def toggle_all_faces(toggle_all_faces_handler: Callable[[int], None], variable: CTk.IntVar):
    if toggle_all_faces_handler:
        return lambda: toggle_all_faces_handler(variable.get())
    return None


def toggle_fps_limit(toggle_all_faces_handler: Callable[[int], None], variable: CTk.IntVar):
    if toggle_all_faces_handler:
        return lambda: toggle_all_faces_handler(variable.get())
    return None


def toggle_keep_frames(toggle_keep_frames_handler: Callable[[int], None], variable: CTk.IntVar):
    if toggle_keep_frames_handler:
        return lambda: toggle_keep_frames_handler(variable.get())
    return None


def create_button(parent, text, command):
    return CTk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color="#3BFFCB",
        text_color="#1E1E1E",
        hover_color="#09B587",
    )


def create_background_button(parent, text, command):
    button = create_button(parent, text, command)
    button.configure (
        bg_color="#1E1E1E",
        fg_color="#781AD6",
        hover_color="#4e0994",
    )
    return button


def create_check(parent, text, variable, command):
    return CTk.CTkCheckBox(
        parent,
        text=text,
        variable=variable,
        command=command
    )


def preview_thread(thread_function):
    threading.Thread(target=thread_function).start()


def open_preview_window(get_video_frame, target_path):
    if preview_visible.get():
        hide_preview()
    else:
        show_preview()
        if target_path:
            frame = get_video_frame(target_path)
            update_preview(frame)


def preview_face(path):
    if path is not None:
        img = Image.open(path)
        img = img.resize((180, 180), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(img)
        face_label.configure(image=photo_img, text="")
        face_label.image = photo_img
    else:
        face_label.configure(image=None, text="No image selected...")


def preview_target(frame):
    if frame is not None:
        img = Image.fromarray(frame)
        img = img.resize((180, 180), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(img)
        target_label.configure(image=photo_img, text="")
        target_label.image = photo_img
    else:
        target_label.configure(image=None, text="No image selected...")



def update_status_label(value):
    status_label["text"] = value
    window.update()


def init(
    initial_values: dict,
    select_face_handler: Callable[[str], None],
    select_target_handler: Callable[[str], Tuple[int, Any]],
    toggle_all_faces_handler: Callable[[int], None],
    toggle_fps_limit_handler: Callable[[int], None],
    toggle_keep_frames_handler: Callable[[int], None],
    save_file_handler: Callable[[str], None],
    start: Callable[[], None],
    get_video_frame: Callable[[str, int], None],
    create_test_preview: Callable[[int], Any],
):
    global window, preview, preview_visible, face_label, target_label, status_label

    window = CTk.CTk()
    window.geometry("600x700")
    window.title("Roop - Face Replacement Software")
    window.configure(bg_color="#1E1E1E")
    window.resizable(width=False, height=False)

    preview_visible = CTk.BooleanVar(window, False)
    target_path = CTk.StringVar()
    frames_amount = CTk.IntVar()

    # Preview window
    preview = create_preview(window)

    left_frame = CTk.CTkFrame(window, bg_color="#292929")
    left_frame.place(x=60, y=100)
    face_label = CTk.CTkLabel(left_frame, text="No image selected...", padx=10, pady=10)
    face_label.pack(fill='both', side='top', expand=True)

    right_frame = CTk.CTkFrame(window, bg_color="#292929")
    right_frame.place(x=360, y=100)
    target_label = CTk.CTkLabel(right_frame, text="No image selected...", padx=10, pady=10)
    target_label.pack(fill='both', side='top', expand=True)

    # Select a face button
    face_button = create_background_button(window, "Select a face", lambda: [
        select_face(select_face_handler)
    ])
    face_button.configure(width=180, height=80)
    face_button.place(x=60,y=320)

    # Select a target button
    target_button = create_background_button(window, "Select a target", lambda: [
        select_target(select_target_handler, target_path, frames_amount),
        update_slider(get_video_frame, create_test_preview, target_path.get(), frames_amount.get())
    ])
    target_button.configure(width=180, height=80)
    target_button.place(x=360,y=320)

    # All faces checkbox
    all_faces = CTk.IntVar(None, initial_values['all_faces'])
    all_faces_checkbox = create_check(window, "Process all faces in frame", all_faces, toggle_all_faces(toggle_all_faces_handler, all_faces))
    all_faces_checkbox.configure(width=240,height=20)
    all_faces_checkbox.place(x=60,y=500)

    # FPS limit checkbox
    limit_fps = CTk.IntVar(None, not initial_values['keep_fps'])
    fps_checkbox = create_check(window, "Limit FPS to 30", limit_fps, toggle_fps_limit(toggle_fps_limit_handler, limit_fps))
    fps_checkbox.configure(width=240,height=20)
    fps_checkbox.place(x=60,y=475)

    # Keep frames checkbox
    keep_frames = CTk.IntVar(None, initial_values['keep_frames'])
    frames_checkbox = create_check(window, "Keep frames dir", keep_frames, toggle_keep_frames(toggle_keep_frames_handler, keep_frames))
    frames_checkbox.configure(width=240,height=20)
    frames_checkbox.place(x=60,y=450)

    # Start button
    start_button = create_button(window, "Start", lambda: [save_file(save_file_handler, target_path.get()), preview_thread(lambda: start(update_preview))])
    start_button.configure(width=120,height=49)
    start_button.place(x=170,y=560)

    # Preview button
    preview_button = create_button(window, "Preview", lambda: open_preview_window(get_video_frame, target_path.get()))
    preview_button.configure(width=120,height=49)
    preview_button.place(x=310,y=560)

    # Status label
    status_label = CTk.CTkLabel(window, text="Status: Ready!")
    status_label.configure(width=480,height=31)
    status_label.place(x=60,y=630)

    return window
