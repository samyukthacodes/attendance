import tkinter as tk
import cv2 
from PIL import Image, ImageTk
import os
import util
from database import *
from datetime import date
from threading import *
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x200+150+100")

        self.login_new_user_button_root_window = util.get_button(self.root, text = 'Login', bg = 'white',command = self.login_window_create, fg = 'red')
        self.login_new_user_button_root_window.place(x = 60, y = 20)
        self.register_new_user_button_root_window = util.get_button(self.root, text = 'Register', bg = 'grey', command =  self.register_new_user, fg = 'black')
        self.register_new_user_button_root_window.place(x = 60, y = 120)
        self.db_dir = './dib'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
    def start(self):
        self.root.mainloop()

    def login_window_create(self):
        self.main_window = tk.Toplevel(self.root)
        self.main_window.geometry("1300x520+150+100")
        
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x = 10, y = 0, width = 700, height = 500)
        self.add_webcam(self.webcam_label, process='login')
        
        self.login_thread = Thread(target = self.login)
        self.login_thread.start()
        
        self.main_window.mainloop()


    def login(self):
        while(self.main_window.winfo_exists()):
            print('Login entered')
            unknown_img_path = './tmp.jpg'
            cv2.imwrite(unknown_img_path, self.most_recent_capt_arr)

            username = util.recognize(self.most_recent_capt_arr, self.db_dir)
            #output = str(subprocess.check_output(['face_recognition','--tolerance', '0.44', self.db_dir, unknown_img_path]))
            #print(output)
            #username = output.split(',')[1][:8]
            print(username)
            #if username in ['no_person_found'[:8], 'unknown_person'[:8]]:
            if username == 'no_person_found':
                self.text_label_main_window = util.get_text_label(self.main_window, 'Person not found. Please register')
                self.text_label_main_window.place(x = 750, y = 50)
                self.text_label_main_window.after(3000, self.text_label_main_window.destroy)
            else:
                user = get_user(username)
                name = user["name"]
                present_dates = set(user["present_dates"])
                present_dates.add(str(date.today()))
                updates = {"present_dates": list(present_dates)}
                update_user(username, updates)

                self.text_label_main_window = util.get_text_label(self.main_window, 'Welcome {}.Your attendance has been marked.'.format(name))
                self.text_label_main_window.place(x = 750, y = 50)
                self.text_label_main_window.after(3000, self.text_label_main_window.destroy)
            os.remove(unknown_img_path)

    def register_new_user(self):


        self.register_new_user_window = tk.Toplevel(self.root)
        self.register_new_user_window.geometry("1200x680+350+100")
        

        self.capture_button_register_new_user_window = util.get_button(self.register_new_user_window, text = 'Capture', bg = 'green', command=self.capture_register_new_user)
        self.capture_button_register_new_user_window.place(x = 750, y = 450)

        

        self.webcam_register_label = util.get_img_label(self.register_new_user_window)
        self.webcam_register_label.place(x = 10, y = 20, width = 700, height = 600)
        self.add_webcam(self.webcam_register_label)

        
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x =750, y=90)
        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'User ID: ')
        self.text_label_register_new_user.place(x = 750, y = 50)
        

        self.name_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.name_register_new_user.place(x =750, y=190)
        self.text_name_register_new_user = util.get_text_label(self.register_new_user_window, 'Name : ')
        self.text_name_register_new_user.place(x = 750, y = 150)
        

        self.email_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.email_register_new_user.place(x =750, y=290)
        self.text_email_register_new_user = util.get_text_label(self.register_new_user_window, 'Email : ')
        self.text_email_register_new_user.place(x = 750, y = 250)
        

        self.password_register_new_user = util.get_password_text(self.register_new_user_window)
        self.password_register_new_user.place(x =750, y=390)
        self.text_password_register_new_user = util.get_text_label(self.register_new_user_window, 'Password : ')
        self.text_password_register_new_user.place(x = 750, y = 350)
        
        

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
        self.capture_label.place(x=10, y=20, width = 700, height = 600)
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', bg = 'green', command = self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x = 750, y = 540)
        self.add_img_to_label(self.capture_label)

    def accept_register_new_user(self):
        username = self.entry_text_register_new_user.get(1.0,'end-1c')
        name = self.name_register_new_user.get(1.0,'end-1c')
        email = self.email_register_new_user.get(1.0,'end-1c')
        password = self.password_register_new_user.get()
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(username)), self.register_new_user_capture)
        insert_user(username, name, email,password)
        util.msg_box('Success!', 'User registered successfully')
        self.register_new_user_window.destroy()
        app.start()

    

    def process_webcam(self, process = 'register'):
        ret, frame = self.cap.read()
        self.most_recent_capt_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capt_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk =ImageTk.PhotoImage(image = self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image = imgtk)
        
    #    if process == 'login':
    #        self.login()
        self._label.after(20, self.process_webcam, process)
         

if __name__ == "__main__":
    app = App()
    app.start()