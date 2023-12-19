import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from cipher_tools import decrypt_password
from database import create_database, Credential
from update_treeview import UpdateTreeview


class Credentials(UpdateTreeview):
    """
    The Credentials class is responsible for creating and managing a treeview display of credential data.
    It provides functionalities for configuring the view and handles events related to selected items in the treeview.

    Attributes:
        root (Tk): The main GUI element.
        tab (Tk frame): The tab in the user interface where the tree is placed.
        scrollbar (Tk scrollbar): The scrollbar for the treeview.
        tree (ttk.Treeview): The treeview that displays the credential data.

    Parameters:
        tab (Tk frame): The tab where the treeview will be placed.
        root (Tk): The main GUI element, used for clipboard operations.
        table_name (str): The name of the table to be associated with the treeview.
    """
    def __init__(self, tab, root, table_name):
        """
        Initializes the Credentials class with given tab, root, and table name.

        Parameters:
            tab (Tk frame): The tab where the treeview will be placed.
            root (Tk): The main GUI element, used for clipboard operations.
            table_name (str): The name of the table to be associated with the treeview.
        """
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
        """
        Configures the 'tree' treeview by setting up columns, headings, and a scrollbar.
        Also adds a 'Submit' button and assigns it a corresponding function.
        """
        self.tree.column('Website', width=240)
        self.tree.column('Login', width=240)
        self.tree.heading('Website', text='Website', anchor='w')
        self.tree.heading('Login', text='Login', anchor='w')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()
        self.scrollbar.place(x=490, rely=0.36, anchor='center', height=99)

        add_tree_button = ctk.CTkButton(self.tab, text='Submit')
        add_tree_button.place(relx=0.5, rely=0.9, anchor="center")
        add_tree_button.bind('<Button-1>', lambda event: self.on_select(event))

    def on_select(self, event):
        """
       Handles the event of selecting an item in the treeview.
       Displays information about the selected website and retrieves and decrypts the associated password.

       Parameters:
           event (Event): The event that triggers this function, containing information about the selected item.
       """
        [item] = self.tree.selection()
        if item:
            values = self.tree.item(item, 'values')
            selected_website = values[0]
            messagebox.showinfo(
                'Info', f'Wybrałeś {selected_website}, Twoje hasło zostało skopiowane do schowka')

            session = create_database()
            credential = session.query(Credential).filter_by(website=selected_website).first()

            related_password = credential.passwords
            if related_password:
                self.root.clipboard_clear()
                self.root.clipboard_append(decrypt_password('kacper95', related_password.password))
        self.tree.selection_remove(item)
