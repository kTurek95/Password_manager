import tkinter as tk
from tkinter import ttk, messagebox
from cipher_tools import encrypt_password
from database import create_database, Credential
from center_window import center_window
from update_treeview import UpdateTreeview
from password_package import api, main


class UpdatePassword(UpdateTreeview):
    def __init__(self, tab, root, table_name):
        super().__init__(table_name)
        self.root = root
        self.tab = tab
        self.scrollbar = tk.Scrollbar(tab, orient='vertical')

        self.tree = ttk.Treeview(
            tab,
            yscrollcommand=self.scrollbar.set,
            columns=('Choose credential',),
            show='headings',
            height=4
        )

        self.configure_tree()
        self.item = None
        self.toplevel = None
        self.user_login = None
        self.new_password = None

    def configure_tree(self):
        self.tree.column('Choose credential', width=480)
        self.tree.heading('Choose credential', text='Choose website credential to update')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()
        self.scrollbar.place(x=490, rely=0.36, anchor='center', height=99)

        add_tree2_button = ttk.Button(self.tab, text='Submit')
        add_tree2_button.place(relx=0.5, rely=0.9, anchor="center")
        add_tree2_button.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.toplevel = tk.Toplevel(self.root)
            self.item = selected_item
            self.toplevel.geometry('250x150')
            center_window(self.toplevel)
            self.toplevel.transient(self.root)
            self.toplevel.grab_set()
            self.toplevel.resizable(False, False)

            user_login_label = ttk.Label(self.toplevel, text='Input login: ')
            user_login_label.place(relx=0.5, rely=0.1, anchor='center')

            self.user_login = ttk.Entry(self.toplevel, show='*')
            self.user_login.place(relx=0.5, rely=0.25, anchor='center')

            new_password_label = ttk.Label(self.toplevel, text='Input new password: ')
            new_password_label.place(relx=0.5, rely=0.45, anchor='center')

            self.new_password = ttk.Entry(self.toplevel, show='*')
            self.new_password.place(relx=0.5, rely=0.60, anchor='center')

            submit_button = ttk.Button(self.toplevel, text='Submit')
            submit_button.place(relx=0.5, rely=0.85, anchor="center")
            submit_button.bind('<Button-1>', self.on_submit_button)

    def get_data(self):
        login_from_user = self.user_login.get()
        user_password = self.new_password.get()
        data_item = self.tree.selection()[0]
        password = api.Api(user_password)
        valid, errors = main.validate_password(password)
        if data_item:
            values = self.tree.item(data_item, 'values')
            selected_website = values[0]

            session = create_database()
            credential = session.query(Credential).filter_by(website=selected_website).first()
            if credential and login_from_user == credential.login:
                password_obj = credential.passwords
                if valid:
                    if password_obj:
                        password_obj.password = encrypt_password('kacper95', user_password)
                        session.commit()
                        messagebox.showinfo('Info', 'Password were updated')
                else:
                    error_messages = '\n'.join([f' - {error}\n' for _, error in errors])
                    messagebox.showerror('Error',
                                         f'The provided password does not meet the following requirements:\n \n{error_messages}')
            else:
                messagebox.showwarning('Warning', 'Incorrect login')

            self.tree.selection_remove(self.item)

    def on_submit_button(self, event):
        self.get_data()
        if self.toplevel:
            self.toplevel.destroy()
