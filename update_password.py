import tkinter as tk
from tkinter import ttk
from center_window import center_window
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

            user_login_label = ttk.Label(self.toplevel, text='Podaj login: ')
            user_login_label.place(relx=0.5, rely=0.1, anchor='center')

            self.user_login = ttk.Entry(self.toplevel, show='*')
            self.user_login.place(relx=0.5, rely=0.25, anchor='center')

            new_password_label = ttk.Label(self.toplevel, text='Podaj nowe hasło: ')
            new_password_label.place(relx=0.5, rely=0.45, anchor='center')

            self.new_password = ttk.Entry(self.toplevel, show='*')
            self.new_password.place(relx=0.5, rely=0.60, anchor='center')


