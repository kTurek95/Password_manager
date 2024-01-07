from CTkListbox import *
import tkinter as tk

class Users:
    def __init__(self, tab, func):
        self.tab = tab
        self.func = func
        # self.username = username
    
    # def get_value(self, selected_option):
    #     self.username.delete(0, 'end')
    #     self.username.insert(0, selected_option)

    def display_login_users(self):
        list_box = CTkListbox(self.tab)
        list_box.pack(pady=10)
        for login in self.func:
            list_box.insert(tk.END, '\n'.join(login))