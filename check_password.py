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
