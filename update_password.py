"""
The update_password module is responsible for updating passwords.
It contains the UpdatePassword class, which inherits from UpdateTreeView.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from password_package import api, main
from cipher_tools import encrypt_password
from database import create_database, Credential, LoginCredentials
from center_window import center_window
from update_treeview import UpdateTreeview
import os
from dotenv import load_dotenv


# pylint: disable=too-many-instance-attributes
class UpdatePassword(UpdateTreeview):
    """
    A class for updating user passwords in a Treeview widget.

    This class inherits from UpdateTreeview and provides functionality
    for updating user passwords displayed in a Treeview widget.

    Attributes:
        root (tk.Tk): The root Tkinter application.
        tab (tk.Frame): The parent frame where the Treeview widget is placed.
        scrollbar (tk.Scrollbar): The vertical scrollbar for the Treeview widget.
        tree (ttk.Treeview): The Treeview widget for displaying user credentials.
        item: None (Optional): The currently selected Treeview item.
        toplevel: None (Optional): The top-level window for updating the password.
        user_login: None (Optional): The login of the user whose password is being updated.
        new_password: None (Optional): The new password to set for the selected user.
        username: The username from currently logged user
    """
    def __init__(self, tab, root, username, table_name):
        """
       Initialize the UpdatePassword class.

       Parameters:
           tab (tk.Frame): The parent frame where the Treeview widget will be placed.
           root (tk.Tk): The root Tkinter application.
           table_name (str): The name of the database table to work with.
       """
        super().__init__(table_name)
        self.root = root
        self.tab = tab
        self.username = username
        self.scrollbar = tk.Scrollbar(tab, orient='vertical')

        self.tree = ttk.Treeview(
            tab,
            yscrollcommand=self.scrollbar.set,
            columns=('Choose credential',),
            show='headings',
            height=4,
            style="mystyle.Treeview"
        )

        self.configure_tree()
        self.item = None
        self.toplevel = None
        self.user_login = None
        self.new_password = None

    def configure_tree(self):
        """
        Configures the 'tree' treeview by setting up columns, headings, and a scrollbar.
        Also adds a 'Submit' button and assigns it a corresponding function.
        """
        
        self.tree['columns'] = ('first',)
        self.tree.column('first', stretch=tk.YES)
        self.tree.heading('first', text='Choose website credential to update')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack(expand=True, fill='both')
        self.scrollbar.place(x=490, rely=0.32, anchor='center', height=99)

        add_tree2_button = ctk.CTkButton(self.tab, text='Submit')
        add_tree2_button.place(relx=0.5, rely=0.9, anchor="center")
        add_tree2_button.bind('<Button-1>', self.on_click)

    # pylint: disable=unused-argument
    def on_click(self, event):
        """
        Configure the Treeview widget for displaying user credentials.

        This method sets up the Treeview widget with appropriate columns and headings,
        configures the scrollbar, and places the widget and related button on the tab.
        """
        selected_item = self.tree.selection()
        if selected_item:
            self.toplevel = ctk.CTkToplevel(self.root)
            self.item = selected_item
            self.toplevel.geometry('250x150')
            center_window(self.toplevel)
            self.toplevel.transient(self.root)
            self.toplevel.grab_set()
            self.toplevel.resizable(False, False)

            user_login_label = ctk.CTkLabel(self.toplevel, text='Input login: ')
            user_login_label.place(relx=0.5, rely=0.1, anchor='center')

            self.user_login = ctk.CTkEntry(self.toplevel, show='*')
            self.user_login.place(relx=0.5, rely=0.25, anchor='center')

            new_password_label =ctk.CTkLabel(self.toplevel, text='Input new password: ')
            new_password_label.place(relx=0.5, rely=0.45, anchor='center')

            self.new_password = ctk.CTkEntry(self.toplevel, show='*')
            self.new_password.place(relx=0.5, rely=0.60, anchor='center')

            submit_button = ctk.CTkButton(self.toplevel, text='Submit')
            submit_button.place(relx=0.5, rely=0.85, anchor="center")
            submit_button.bind('<Button-1>', self.on_submit_button)

    def get_data(self):
        """
        Get and update user password data based on user input and Treeview selection.

        This method retrieves user input for login and new password,
        as well as the selected Treeview item.
        It then validates the new password, checks if the login matches the selected item,
        and updates the password
        in the database if the password meets the requirements.

        Raises:
            - An error message if the provided password does not meet the requirements.
            - A warning if the login does not match the selected website credential.
        """
        load_dotenv()
        key = os.environ.get('KEY')
        login_from_user = self.user_login.get()
        user_password = self.new_password.get()
        data_item = self.tree.selection()[0]
        valid, errors = main.validate_password(api.Api(user_password))
        if data_item:
            values = self.tree.item(data_item, 'values')
            selected_website = values[0]

            session = create_database()
            user = session.query(LoginCredentials).filter_by(username=self.username).first()
            credential = session.query(Credential).filter_by(website=selected_website, username_id=user.id).first()
            if credential and login_from_user == credential.login:
                password_obj = credential.passwords
                if valid:
                    if password_obj:
                        password_obj.password = encrypt_password(key, user_password)
                        session.commit()
                        messagebox.showinfo('Info', 'Password were updated')
                else:
                    error_messages = '\n'.join([f' - {error}\n' for _, error in errors])
                    messagebox.showerror(
                        'Error',
                        f'The provided password does not meet the following requirements:'
                        f'\n \n{error_messages}'
                    )
            else:
                messagebox.showwarning('Warning', 'Incorrect login')

            self.tree.selection_remove(self.item)

    # pylint: disable=unused-argument
    def on_submit_button(self, event):
        """
        Handle the submit button event.
        This method triggers the retrieval and update of user password data
         using the `get_data` method.
        If a top-level window (`toplevel`) exists, it is destroyed.

        Args:
            event: The event object associated with the button click.
        """
        self.get_data()
        if self.toplevel:
            self.toplevel.destroy()
