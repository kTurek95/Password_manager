import customtkinter as ctk
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils import get_users_from_database
from center_window import center_window
from utils import clear_input_fields


class SwitchUser:
    def __init__(self, tab, root, username, user_login, user_password, main_window):
        self.tab = tab
        self.root = root
        self.username = username
        self.user_login = user_login
        self.user_password = user_password
        self.main_window = main_window
        self.checkboxes = []
        self.tree = ttk.Treeview(tab,
                            columns=('Users',),
                            show='headings',
                            height=4, )

    def open_new_window(self):
        new_window = ctk.CTkToplevel(self.root)
        new_window.transient(self.root)
        new_window.grab_set()
        new_window.geometry('300x200')
        center_window(new_window)

        password_label=ctk.CTkLabel(new_window, text='Input password:', fg_color=("white", "gray"), corner_radius=10)
        password_label.pack(pady=10)
        password = ctk.CTkEntry(new_window, show='*')
        password.pack()

        username = self.get_selected_item()

        def close():
            new_window.destroy()
            self.root.withdraw()
            self.main_window.withdraw()

        def open_window():
            from main_window import open_main_window
            open_main_window(self.main_window, username, self.user_login, self.user_password)

        def check_password():
            correct_password = password.get()
            user = get_users_from_database(username=username)
        
            if user[0] == correct_password:
                close()
                open_window()
            else:
                messagebox.showerror('Error', 'Wrong password')
                clear_input_fields(password)

        submit_button = ctk.CTkButton(new_window, text='ok', command=check_password)
        submit_button.pack(pady=10)

    def display_users(self):
        self.tree["columns"] = ("1",)
        self.tree.column("1", stretch=tk.YES)

        self.tree.heading("1", text="Users")

        users = get_users_from_database()

        for user in users:
            if user != self.username:
                self.tree.insert("", "end", values=(f"{user}",))

        self.tree.pack(expand=True, fill='both')

        add_new_window_button = ctk.CTkButton(master=self.tab, text='Submit', command= lambda: (self.open_new_window(), self.get_selected_item()))
        add_new_window_button.place(relx=0.5, rely=0.9, anchor="center")

    def get_selected_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            selected_username = item.get('values')[0]
            return selected_username
        