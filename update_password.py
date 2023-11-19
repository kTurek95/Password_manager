import tkinter as tk
from tkinter import ttk
from update_treeview import UpdateTreeview


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
