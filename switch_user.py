import customtkinter as ctk
from database import create_database
from database import LoginCredentials

class SwitchUser:
    def __init__(self, tab, root, username):
        self.tab = tab
        self.root = root
        self.username = username

    def get_users_from_database(self):
        users = []
        session = create_database()
        user_username = session.query(LoginCredentials).filter_by(username=self.username).first()
        if user_username:
            all_users = session.query(LoginCredentials).all()
            for record in all_users:
                if record.id != user_username.id:
                    users.append(record.username)

        return users

    def new_window(self):
        new_window = ctk.CTkToplevel(self.root)
        new_window.transient(self.root)
        new_window.grab_set()
        new_window.geometry('200x100')

        password_label=ctk.CTkLabel(new_window, text='Input password:', fg_color=("white", "gray75"), corner_radius=10)
        password_label.pack(pady=10)
        password = ctk.CTkEntry(new_window)
        password.pack()

    def display_users(self):
        label = ctk.CTkLabel(master=self.tab,
                             text='Choose account do you want to switch:',
                             corner_radius=10,
                             fg_color=("white", "gray75"))
        label.pack(pady=20)
        users = self.get_users_from_database()

        for user in users:
            my_check = ctk.CTkCheckBox(self.tab, text=user)
            my_check.pack()

        add_new_window_button = ctk.CTkButton(master=self.tab, text='Submit', command=self.new_window)
        add_new_window_button.pack(pady=20)