import tkinter as tk
from tkinter import messagebox
from main_window import open_main_window
from database import create_database, LoginCredentials

FAILED_ATTEMPTS = 0


class CheckPassword:
    def __init__(self, user_login, user_password, root):
        """
       Initialize a CheckPassword instance.

       Parameters:
       - user_password (str): The user-entered password to be checked.
       - root: The root of the application (assuming it's a Tkinter application).
       """
        self.root = root
        self.user_password = user_password
        self.user_login = user_login

    def check_password(self):
        """
       Check if the user-entered password matches the valid password.

       Returns:
       - bool: True if the user-entered password matches the valid password, False otherwise.
       """

        session = create_database()
        credentials = session.query(LoginCredentials.login, LoginCredentials.password).all()
        password_from_user = self.user_password.get()
        username = self.user_login.get()


        for login, password in credentials:
            if password == password_from_user and login == username:
                return True
            return False


    def on_submit(self, event):
        """
        Handles the form submission event in the user interface.

        This method is invoked when the user attempts to submit the form with a password.
        It checks if the password field is not empty and then verifies the password.
        If the password is correct, the main window of the application is opened.
        In case of failed login attempts, the user is presented with appropriate
        warning messages, and after three failed attempts, access is blocked.

        Parameters:
            event: The event object passed by the Tkinter event system.

        Returns:
            None. May close the main application window in case of access being blocked.
        """
        global FAILED_ATTEMPTS
        user_password = self.user_password.get()
        if not user_password.strip():
            messagebox.showinfo('Info', "You didn't enter the password")

        elif self.check_password():
            self.root.withdraw()
            open_main_window(self.root)

        else:
            if len(user_password) > 1:
                self.user_password.delete(0, tk.END)
                FAILED_ATTEMPTS += 1
                messagebox.showwarning('Error', 'Wrong password')
                if FAILED_ATTEMPTS >= 3:
                    messagebox.showwarning('Error', 'Access blocked')
                    self.root.destroy()
