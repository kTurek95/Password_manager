"""
This module provides the Logout functionality
for a GUI-based application using the customtkinter library.

The module contains the `Logout` class
which is responsible for handling the logout process of a user from the application.
It displays a logout interface in a specified tab or frame within the application's main window.
The class provides a user-friendly way to log out, asking for user confirmation before proceeding.
"""

import customtkinter as ctk
from utils import clear_input_fields

# pylint: disable=too-few-public-methods
class Logout:
    """
    This class represents the logout functionality in a GUI application.

    Attributes:
        logout_tab (ctk.CTkFrame): The tab or frame in the GUI
        where the logout functionality is displayed.
        username (str): The username of the currently logged-in user.
        main_window (ctk.CTk): The main window of the application.
        root (ctk.CTk): The root window of the application.
        user_login (ctk.CTkEntry): The entry widget for user login.
        user_password (ctk.CTkEntry): The entry widget for user password.
    """
    # pylint: disable=too-many-arguments
    def __init__(self, logut_tab, username, main_window, root, user_login, user_password) -> None:
        """
        Initializes the Logout class with necessary widgets and user information.

        Args:
            logout_tab (ctk.CTkFrame): The tab or frame for logout functionality.
            username (str): The username of the currently logged-in user.
            main_window (ctk.CTk): The main window of the application.
            root (ctk.CTk): The root window of the application.
            user_login (ctk.CTkEntry): The entry widget for user login.
            user_password (ctk.CTkEntry): The entry widget for user password.
        """
        self.logout_tab = logut_tab
        self.username = username
        self.main_window = main_window
        self.root = root
        self.user_login = user_login
        self.user_password = user_password

        label = ctk.CTkLabel(self.logout_tab,
                             text=f'You are loogged in as {self.username}',
                             font=('Helvetica', 20) )
        label.pack()

        label = ctk.CTkLabel(self.logout_tab, text='Do you want to logout?', font=('Helvetica', 20))
        label.pack(pady=20)

    def logout_user(self):
        """
        Handles the logout process for the user.
        It provides options for the user to confirm logout and 
        performs necessary actions based on the user's choice.
        """
        def close():
            """ Closes the main application window. """
            self.main_window.destroy()

        def open_window():
            """ Clears input fields and reopens the root window for new login. """
            clear_input_fields(self.user_login, self.user_password)
            self.root.deiconify()

        def get_choice():
            """
            Retrieves the user's choice from the radio buttons and processes the logout accordingly.
            """
            user_choice_result = user_choice.get()
            if user_choice_result == 'Yes':
                close()
                open_window()

        user_choice = ctk.StringVar(value='other')
        yes_button = ctk.CTkRadioButton(self.logout_tab,
                                        text='Yes', value='Yes',
                                        font=('Helvetica', 15),
                                        variable=user_choice)
        yes_button.pack(pady=20)

        no_button = ctk.CTkRadioButton(self.logout_tab,
                                       text='No',
                                       value='No',
                                       font=('Helvetica', 15),
                                       variable=user_choice)
        no_button.pack()

        choice_label = ctk.CTkLabel(self.logout_tab, text='')
        choice_label.pack()

        submit_button = ctk.CTkButton(self.logout_tab, text='Submit', command=get_choice)
        submit_button.pack(pady=10)
