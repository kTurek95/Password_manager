import tkinter as tk
from tkinter import ttk, messagebox
from cipher_tools import decrypt_password
from database import create_database, Credential
from update_treeview import UpdateTreeview


class Credentials(UpdateTreeview):
    def __init__(self, tab, root, table_name):
        super().__init__(table_name)
        self.root = root
        self.tab = tab
        self.scrollbar = tk.Scrollbar(tab, orient='vertical')

        self.tree = ttk.Treeview(
            tab,
            yscrollcommand=self.scrollbar.set,
            columns=('Website', 'Login'),
            show='headings',
            height=4
            )

        self.configure_tree()

    def configure_tree(self):
        self.tree.column('Website', width=240)
        self.tree.column('Login', width=240)
        self.tree.heading('Website', text='Website', anchor='w')
        self.tree.heading('Login', text='Login', anchor='w')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()
        self.scrollbar.place(x=490, rely=0.36, anchor='center', height=99)
