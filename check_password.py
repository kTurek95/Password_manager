from os import getenv
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from main_window import open_main_window

failed_attempts = 0


class CheckPassword:
    def __init__(self, user_password, root):
        """
       Initialize a CheckPassword instance.

       Parameters:
       - user_password (str): The user-entered password to be checked.
       - root: The root of the application (assuming it's a Tkinter application).
       """
        self.root = root
        self.user_password = user_password

    def check_password(self):
        """
       Check if the user-entered password matches the valid password.

       Returns:
       - bool: True if the user-entered password matches the valid password, False otherwise.
       """
        load_dotenv()
        valid_password = getenv('PASSWORD')
        password_from_user = self.user_password.get()

        if valid_password == password_from_user:
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
        global failed_attempts
        user_password = self.user_password.get()
        if not user_password.strip():
            messagebox.showinfo('Info', "You didn't enter the password")

        elif self.check_password():
            self.root.withdraw()
            open_main_window(self.root)

        else:
            if len(user_password) > 1:
                self.user_password.delete(0, tk.END)
                failed_attempts += 1
                messagebox.showwarning('Error', 'Wrong password')
                if failed_attempts >= 3:
                    messagebox.showwarning('Error', 'Access blocked')
                    self.root.destroy()
