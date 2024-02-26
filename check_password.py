"""
The 'check_password' module is responsible for verifying
whether the user's password and login exist in the database.
If they do not, an error message is displayed, indicating that the data is incorrect.
If they do, the user can proceed to the main application.
"""
from tkinter import messagebox
from main_window import open_main_window
from database import create_database, LoginCredentials
from utils import clear_input_fields
from utils import check_if_fields_not_missing
import os
from dotenv import load_dotenv
from cipher_tools import decrypt_password

FAILED_ATTEMPTS = 0


class CheckPassword:
    """
    The 'CheckPassword' class handles the logic for verifying user-provided passwords and logins.

    Methods:
        - __init__
        - check_password
        - on submit
    """
    def __init__(self, user_login, user_password, root):
        """
       Initialize a CheckPassword instance.

       Parameters:
        - user_login (str) : The user-entered login to be checked
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
        load_dotenv()
        key = os.environ.get('KEY')
        session = create_database()
        credentials = session.query(LoginCredentials.username, LoginCredentials.password).all()
        username = self.user_login.get()
        password_from_user = self.user_password.get()


        for login, password in credentials:
            decrypted_password = decrypt_password(key, password)
            if password_from_user == decrypted_password and login == username:
                return True
        return False

    def on_submit(self):
        """
        Handles the form submission event in the user interface.

        This method is invoked when the user attempts to submit the form with a password.
        It checks if the password field is not empty and then verifies the password.
        If the password is correct, the main window of the application is opened.
        In case of failed login attempts, the user is presented with appropriate
        warning messages, and after three failed attempts, access is blocked.

        Returns:
            None. May close the main application window in case of access being blocked.
        """
        # pylint: disable=global-statement
        global FAILED_ATTEMPTS
        user_password = self.user_password.get()
        username = self.user_login.get()

        missing_fields = check_if_fields_not_missing(
            username = self.user_login.get(),
            password = self.user_password.get()
        )

        if missing_fields and self.check_password():
            self.root.withdraw()
            open_main_window(self.root, username, self.user_login, self.user_password)
            return True

        if len(user_password) > 1 and not self.check_password():
            clear_input_fields(self.user_password, self.user_login)
            FAILED_ATTEMPTS += 1
            messagebox.showwarning('Error', 'Wrong credentials')
            if FAILED_ATTEMPTS >= 3:
                messagebox.showwarning('Error', 'Access blocked')
                self.root.destroy()

        return False
