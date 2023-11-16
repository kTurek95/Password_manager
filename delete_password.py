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

        self.configure_tree()

    def configure_tree(self):
        self.tree.column('Choose credential', width=480)
        self.tree.heading('Choose credential', text='Choose website credential to delete')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()
        self.scrollbar.place(x=490, rely=0.36, anchor='center', height=99)

        add_tree3_button = ttk.Button(self.tab, text='Submit')
        add_tree3_button.place(relx=0.5, rely=0.9, anchor="center")
