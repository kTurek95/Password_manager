"""
This module provides functionality for user registration in an application.
It uses custom Tkinter widgets to create a registration form,
validates user input, and stores valid registration information in a SQLite database.
The module also includes email validation and sending a confirmation email
upon successful registration. The password is encrypted
before being stored in the database for enhanced security.
"""


import re
import sqlite3
from tkinter import messagebox
import customtkinter as ctk
from password_package import api, main
from database import create_database, LoginCredentials
from send_email import Email
from utils import clear_input_fields, check_if_fields_not_missing
from cipher_tools import encrypt_password
import smtplib
import os
from dotenv import load_dotenv

# pylint: disable=too-many-statements, too-few-public-methods
class RegisterUser:
    """
    This class creates a registration form for new users using custom Tkinter widgets.

    Attributes:
        registertab (CTkFrame): A Custom Tkinter Frame where the registration widgets are placed.

    Methods:
        insert_credentials_into_database:
        Validates user input, checks for existing users,
        encrypts the password, and stores new user credentials in the database.
        It also sends a confirmation email.
    """
    def __init__(self, register_tab):
        """
        Initializes the RegisterUser class with a Custom Tkinter Frame.

        Parameters:
            register_tab (CTkFrame):
            The Custom Tkinter Frame where the registration form will be displayed.
        """
        self.registertab = register_tab

        register_username_label = ctk.CTkLabel(register_tab, text='Username')
        register_username_label.place(x=15, y=1)
        register_username = ctk.CTkEntry(register_tab, width=160)
        register_username.place(x=15, y=31)

        register_email_label = ctk.CTkLabel(register_tab, text='Email')
        register_email_label.place(x=210, y=1)
        register_email = ctk.CTkEntry(register_tab, width=160)
        register_email.place(x=210, y=31)

        register_password_label = ctk.CTkLabel(register_tab, text='Password')
        register_password_label.place(x=15, y=61)
        register_password = ctk.CTkEntry(register_tab, width=160, show='*')
        register_password.place(x=15, y=91)

        register_confirm_password_label = ctk.CTkLabel(register_tab, text='Confirm Password')
        register_confirm_password_label.place(x=210, y=61)
        register_confirm_password = ctk.CTkEntry(register_tab, width=160, show='*')
        register_confirm_password.place(x=210, y=91)

        def is_valid_email(email):
                """
                Validates the format of an email address using regular expressions.

                Parameters:
                    email (str): The email address to validate.

                Returns:
                    bool: True if the email address is in a valid format, False otherwise.
                """
                regex = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
                if re.match(regex, email):
                    return True
                return False
        
        def check_if_user_exist(username, email):
                            """
                            Checks if a user with the given username or email
                            already exists in the database.

                            Parameters:
                                username (str): The username to check in the database.
                                email (str): The email to check in the database.

                            Returns:
                                bool: True if the user exists, False otherwise.
                            """
                            try:    
                                connection = sqlite3.connect('database.db')
                                cursor = connection.cursor()
                                cursor.execute("SELECT * FROM LoginCredentials WHERE"
                                            " username=? or email=?", (username, email))
                                existing_user = cursor.fetchone()
                                connection.close()

                                return existing_user is not None
                            except sqlite3.Error as error:
                                 print('An error occurred: '.format(error))
                            finally:
                                 if connection:
                                      connection.close()

        def insert_credentials_into_database():
            """
            Validates the registration form input, checks if the user already exists,
            and inserts new user credentials into the database.

            It performs several checks: ensuring all fields are filled,
            validating the email format, ensuring the passwords match,
            checking if the username or email already exists in the database,
            and validating the password strength. If all checks pass,
            the user's password is encrypted, and the credentials are stored in the database.
            A confirmation email is sent to the user.
            Error messages are displayed for any failed validations.
            """
            load_dotenv()
            key = os.environ.get('KEY')
            credentials_username = register_username.get()
            credentials_password = register_password.get()
            credentials_confirm_password = register_confirm_password.get()
            credentials_email = register_email.get()

            missing_fields = check_if_fields_not_missing(
                username = register_username.get(),
                password = register_password.get(),
                confirm_password = register_confirm_password.get(),
                email = register_email.get())

            if not missing_fields:
                if credentials_password != credentials_confirm_password:
                    messagebox.showerror('Error', 'The password do not match')
                    clear_input_fields(register_password, register_confirm_password)
                elif not is_valid_email(credentials_email) and not len(credentials_email) == 0:
                    messagebox.showerror('Error', 'Email address is not valid')
                    clear_input_fields(register_email)
            else:
                if  not len(credentials_password) == 0:
                    password = api.Api(credentials_password)
                    valid, errors = main.validate_password(password)
                    session = create_database()

                    if check_if_user_exist(credentials_username, credentials_email):
                        messagebox.showerror(
                            'Error',
                            '''An account with the provided details already exists,
                            please try again.'''
                        )
                        clear_input_fields(register_username,
                                        register_password,
                                        register_confirm_password,
                                        register_email
                        )
                    else:
                        if valid:
                            login_credentials = LoginCredentials(
                                username=credentials_username,
                                password=encrypt_password(key ,credentials_password),
                                confirm_password=credentials_confirm_password,
                                email=credentials_email)
                            session.add(login_credentials)

                            email_object = Email(credentials_email,
                                                credentials_username,
                                                credentials_password
                            )
                            try:
                                email_object.send_mail()
                            except smtplib.SMTPException as e:
                                print(f"An error occurred while sending the email: {e}")

                            messagebox.showinfo(
                                'Info', 'Thank you, your account has just been registered. \n'
                                'Check your email and restart the program.'
                            )
                            session.commit()
                            clear_input_fields(register_username,
                                            register_password,
                                            register_confirm_password,
                                            register_email
                            )
                        else:
                            error_messages = '\n'.join([f' - {error}\n' for _, error in errors])
                            messagebox.showerror(
                                'Error',
                                f'''The provided password does not
                                meet the following requirements:
                                \n \n{error_messages}'''
                            )
                            clear_input_fields(register_username,
                                            register_password,
                                            register_confirm_password,
                                            register_email
                            )

        register_button = ctk.CTkButton(register_tab,
                                        command=insert_credentials_into_database,
                                        text='Register')
        register_button.place(x=120, y=125)
