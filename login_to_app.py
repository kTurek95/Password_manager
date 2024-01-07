import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
from check_password import CheckPassword

class LoginToApp:
    def __init__(self, tab2, root):
        self.tab2 = tab2
        self.root = root
        self.username = None

        password_from_user_label = ctk.CTkLabel(tab2, text='Password')
        password_from_user_label.place(relx=0.7, rely=0.2, anchor="center")

        password_from_user = ctk.CTkEntry(tab2, show='*', width=120)
        password_from_user.place(relx=0.75, rely=0.45, anchor="center")

        username_label = ctk.CTkLabel(tab2, text='Username')
        username_label.place(relx=0.2, rely=0.2, anchor='center')

        self.username = ctk.CTkEntry(tab2, width=120)
        self.username.place(relx=0.25, rely=0.45, anchor="center")

        check_password_instance = CheckPassword(self.username, password_from_user, root)

        add_login_button = ctk.CTkButton(tab2, corner_radius=10, text='Login', width=100)
        add_login_button.place(relx=0.49, rely=0.85, anchor="center")
        add_login_button.bind('<Button-1>', lambda event: check_password_instance.on_submit(event))
