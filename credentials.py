import tkinter as tk
from tkinter import ttk
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
