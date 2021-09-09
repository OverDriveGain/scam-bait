# import modules
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
import os


# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="white").pack()
    Label(register_screen, text="").pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="white", command=register_user).pack()



# Designing window for login
def start_counting(count, label):
    global main_screen
    # change text in label
    label['text'] = count
    if count > 0:
    # call countdown again after 1000ms (1s)
        main_screen.after(1000, start_counting, count - 1, label)

def countdown():
    global countdown_screen
    countdown_screen = Toplevel(main_screen)
    countdown_screen.title("Login without password")
    countdown_screen.geometry("350x350")
    Label(countdown_screen, text="Database opens after countdown (10 minutes)").pack()
    global countdown_label
    countdown_label = Label(countdown_screen, text="600", bg="white", width="150", height="2", font=("Calibri", 23))
    countdown_label.pack()
    Label(countdown_screen, text="").pack()
    start_counting(599, countdown_label)

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=15, height=1, command=login_verify).pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Forgot password", width=15, height=1, command=countdown).pack()


# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()


# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="Incorrect password").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = ''#os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# Designing Main(first) window

def main_app():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("350x350")
    main_screen.title("KeePassX Light")
    img = ImageTk.PhotoImage(Image.open(resource_path("Logo.png")))
    panel = Label(main_screen, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    Label(text="Select Your Choice", bg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Access password databases", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Create new password database", height="2", width="30", command=register).pack()
    Label(text="Copyright 2021. KeepassX", width="30", height="2", font=("Calibri", 9)).pack()
    Label(text="").pack(side="bottom")
    main_screen.mainloop()


def main_account_screen():
    thd = Thread(target=main_app)  # gui thread
    thd.daemon = True  # background thread will exit if main thread exits
    thd.start()  # start tk loop
    #thd.join()
