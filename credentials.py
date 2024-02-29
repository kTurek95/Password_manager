import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from cipher_tools import decrypt_password
from database import create_database, Credential
from update_treeview import UpdateTreeview
import os
from dotenv import load_dotenv


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
            height=4,
            style="mystyle.Treeview"
            )

        my_color = '#292929'
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview', fieldbackground=my_color, background=my_color, foreground='white')
        self.configure_tree()


    def configure_tree(self):
        """
        Configures the 'tree' treeview by setting up columns, headings, and a scrollbar.
        Also adds a 'Submit' button and assigns it a corresponding function.
        """
        
        self.tree['columns'] = ('first', 'second')
        self.tree.column('#0', width=120, stretch=tk.NO)
        self.tree.column('first', stretch=tk.YES, width=120)
        self.tree.column('second', stretch=tk.YES, width=120)

        self.tree.heading('#0')
        self.tree.heading('first', text='Website')
        self.tree.heading('second', text='Login')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack(expand=True, fill='both')
        self.scrollbar.place(x=490, rely=0.32, anchor='center', height=99)

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
        load_dotenv()
        key = os.environ.get('KEY')
        [item] = self.tree.selection()
        if item:
            values = self.tree.item(item, 'values')
            selected_website = values[0]
            messagebox.showinfo(
                'Info', f'You chose {selected_website}, Your password has been copied to the clipboard')

            session = create_database()
            credential = session.query(Credential).filter_by(website=selected_website).first()

            related_password = credential.passwords.password
            if related_password:
                self.root.clipboard_clear()
                self.root.clipboard_append(decrypt_password(key, related_password))
        self.tree.selection_remove(item)
