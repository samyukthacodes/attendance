import tkinter as tk
import cv2 
from PIL import Image, ImageTk
import os
import util
import subprocess


class App:
    def __init__(self):
        self.i = 0
        self.root = tk.Tk()
        self.root.geometry("1200x520+350+100")

        self.login_new_user_button_root_window = util.get_button(self.root, 'Login', 'grey', self.login_window_create, fg = 'black')
        self.login_new_user_button_root_window.place(x = 750, y = 200)
        self.register_new_user_button_root_window = util.get_button(self.root, 'Register', 'grey', self.register_new_user, fg = 'black')
        self.register_new_user_button_root_window.place(x = 750, y = 300)
        self.db_dir = './dib'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
    def start(self):
        self.root.mainloop()

    def login_window_create(self):
        self.main_window = tk.Toplevel()
        self.main_window.geometry("1200x520+350+100")
        
        """
        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x = 750, y = 200)
        """
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x = 10, y = 0, width = 700, height = 500)
        self.add_webcam(self.webcam_label, process='login')
        
        self.main_window.mainloop()

    

    def login(self):
        unknown_img_path = './tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capt_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
        name = output.split(',')[1][:-3]
        print(output)
        if name in ['no_persons_found', 'unknown_user']:
            self.text_label_main_window = util.get_text_label(self.main_window, 'Person not found. Please register')
            self.text_label_main_window.place(x = 750, y = 50)
            self.text_label_main_window.after(3000, self.text_label_main_window.destroy)
        else:
            self.text_label_main_window = util.get_text_label(self.main_window, 'Welcome {}.Your attendance has been marked.'.format(name))
            self.text_label_main_window.place(x = 750, y = 50)
            self.text_label_main_window.after(3000, self.text_label_main_window.destroy)
        os.remove(unknown_img_path)

    def register_new_user(self):


        self.register_new_user_window = tk.Toplevel()
        self.register_new_user_window.geometry("1200x520+350+100")
        

        self.capture_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Capture', 'green', self.capture_register_new_user)
        self.capture_button_register_new_user_window.place(x = 750, y = 200)

        

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'Red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x = 750, y = 400)
        

        self.webcam_register_label = util.get_img_label(self.register_new_user_window)
        self.webcam_register_label.place(x = 10, y = 0, width = 700, height = 500)
        self.add_webcam(self.webcam_register_label)

        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x =750, y=100)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'User name: ')
        self.text_label_register_new_user.place(x = 750, y = 50)

    def add_img_to_label(self, label):
        imgtk =ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image = imgtk)

        self.register_new_user_capture = self.most_recent_capt_arr.copy()   

    def add_webcam(self, label, process = 'register'):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label     
        self.process_webcam(process)


    def capture_register_new_user(self):
        self.webcam_register_label.destroy()
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width = 700, height = 500)
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x = 750, y = 300)
        self.add_img_to_label(self.capture_label)

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0,'end-1c')
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Success!', 'User registered successfully')
        self.register_new_user_window.destroy()
        app.start()

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def process_webcam(self, process = 'register'):
        ret, frame = self.cap.read()
        self.most_recent_capt_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capt_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk =ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image = imgtk)

        if process == 'login':
            self.login()
        self._label.after(20, self.process_webcam, process)
        

if __name__ == "__main__":
    app = App()
    app.start()