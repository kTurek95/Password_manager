"""
This module defines a class 'Users' that manages the user tab in the application.
It inherits from the 'LoginToApp' class
and provides functions for listing available users,
selecting a user, and displaying them in the user tab.
"""

from tkinter import messagebox
import customtkinter as ctk
from database import create_database, LoginCredentials
from login_to_app import LoginToApp
from utils import get_users_from_database
from utils import move_user

class Users(LoginToApp):
    """
    The Users class inherits from the LoginToApp class
    and is responsible for handling the user tab in the application.

    Attributes:
        user_tab (tkinter.Frame): The user tab frame.
        tabview (customtkinter.CTkTabView): The tab view in the application.
        users_box (customtkinter.CTkComboBox): ComboBox for user selection.
    """
    def __init__(self, user_tab, login_tab, root, tabview):
        """
        Initializes an instance of the Users class.

        Parameters:
            user_tab (tkinter.Frame): The user tab frame.
            login_tab (tkinter.Frame): The login tab frame.
            root (tkinter.Tk): The main application window.
            tabview (customtkinter.CTkTabView): The tab view in the application.
        """
        self.user_tab = user_tab
        self.tabview = tabview
        LoginToApp.__init__(self, login_tab, root, tabview)
        self.users_box=None

    def logins_list(self) -> list:
        """
        Retrieves a list of usernames from the database.

        Returns:
            list: A list of usernames.
        """
        session = create_database()
        logins = session.query(LoginCredentials.username).all()

        login_list = [login[0] for login in logins]

        return login_list

    def user_picker(self) -> bool:
        """
        Selects a user from the ComboBox and inserts their name into the login field.

        Returns:
            bool: True if the user exists in the database, False otherwise.
        """
        users = get_users_from_database()
        if self.users_box.get() not in users:
            messagebox.showinfo(
                'Info',
                'User has been deleted, please restart the program or select another user'
                )
            return False
        self.login_username.delete(0, 'end')
        self.login_username.insert(0, self.users_box.get())
        return True

    def display_login_users(self):
        """
        Displays available users in the user tab.
        """
        for widget in self.user_tab.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.user_tab,
                             text='Available users: ',
                             corner_radius=10,
                             fg_color=("white", "gray"))
        label.pack(pady=5)

        users = self.logins_list()
        self.users_box = ctk.CTkComboBox(self.user_tab, values=users, state='readonly')
        self.users_box.pack(pady=5)

        button = ctk.CTkButton(self.user_tab,
                               text='Submit',
                               command= lambda: (self.user_picker() and
                                                 move_user(self.tabview,
                                                                'Login')))
        button.pack(pady=5)
