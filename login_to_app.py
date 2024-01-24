import customtkinter as ctk
from check_password import CheckPassword
from utils import move_user

class LoginToApp:
    def __init__(self, login_tab, root, tabview):
        self.login_tab = login_tab
        self.root = root
        self.tabview = tabview

        password_from_user_label = ctk.CTkLabel(login_tab, text='Password')
        password_from_user_label.place(relx=0.7, rely=0.2, anchor="center")

        password_from_user = ctk.CTkEntry(login_tab, show='*', width=120)
        password_from_user.place(relx=0.75, rely=0.45, anchor="center")

        username_label = ctk.CTkLabel(login_tab, text='Username')
        username_label.place(relx=0.2, rely=0.2, anchor='center')

        self.login_username = ctk.CTkEntry(login_tab, width=120)
        self.login_username.place(relx=0.25, rely=0.45, anchor="center")

        check_password_instance = CheckPassword(self.login_username, password_from_user, root)
        def handle_login():
            if not check_password_instance.on_submit():
                move_user(self.tabview, 'Users')

        add_login_button = ctk.CTkButton(login_tab, corner_radius=10, text='Login', width=100, command=handle_login)
        add_login_button.place(relx=0.49, rely=0.85, anchor="center")
