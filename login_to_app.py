import customtkinter as ctk
import tkinter as tk
from CTkListbox import *
from check_password import CheckPassword

class LoginToApp:
    def __init__(self, tab1, tab2, func, root):
        self.tab1 = tab1
        self.tab2 = tab2
        self.func = func
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

        def get_value(selected_option):
            self.username.delete(0, 'end')
            self.username.insert(0, selected_option)

        list_box = CTkListbox(tab1, command=get_value)
        list_box.pack(pady=10)
        for login in func:
            list_box.insert(tk.END, '\n'.join(login))

        check_password_instance = CheckPassword(self.username, password_from_user, root)


        add_login_button = ctk.CTkButton(tab2, corner_radius=10, text='Login', width=100)
        add_login_button.place(relx=0.49, rely=0.85, anchor="center")
        add_login_button.bind('<Button-1>', lambda event: check_password_instance.on_submit(event))
