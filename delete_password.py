import tkinter as tk
from tkinter import ttk
from update_treeview import UpdateTreeview


class DeletePassword(UpdateTreeview):
    def __init__(self, tab, credentials, update_password, table_name):
        super().__init__(table_name)
        self.credentials = credentials
        self.update_password = update_password
        self.tab = tab
        self.scrollbar = tk.Scrollbar(tab, orient='vertical')
        self.tree = ttk.Treeview(
            tab,
            yscrollcommand=self.scrollbar.set,
            columns=('Choose credential',),
            show='headings',
            height=4, )