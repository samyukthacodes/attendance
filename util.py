import os


import tkinter as tk
from tkinter import messagebox
import face_recognition
import numpy as np

def get_button(window, text, command, bg = 'green', fg='black'):
    button = tk.Button(
                        window,
                        text=text,
                        fg=fg,
                        bg=bg,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=30, font=("Arial", 25  ))
    return inputtxt

def get_password_text(window):
    inputtxt = tk.Entry(window,
                       width=30, font=("Arial", 25  ), show = '*')
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_person_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))    
    match = np.array([False])
    j = 0
    while(not match.all() and j < len(db_dir)):
        path_ = os.path.join(db_path, db_dir[j])
        known_image = face_recognition.load_image_file(path_)
        known_faces = face_recognition.face_encodings(face_image = known_image)

        match = face_recognition.compare_faces([known_faces], embeddings_unknown, tolerance=0.44)[0]
        
        
        j += 1

    if match.all():
        return db_dir[j-1].split('.',)[0]
    else:
        return 'no_person_found'
