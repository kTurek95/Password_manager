"""
AddPassword Module

This module is responsible for encrypting and adding a password
provided by the user to the database.
It contains the AddPassword class and static methods
for managing data and the user interface.

Classes:
    AddPassword: The main class in the module, managing the process of adding a new password.

Methods:
    staitcmethod - update_credentials_treeview():
    A static method that updates the tree view of the credentials data.
    insert_data_and_update_ui():
    Method that inserts data into the database and updates the user interface.
"""

import tkinter as tk
from tkinter import messagebox
import string
import random
import customtkinter as ctk
from password_package import api, main
from cipher_tools import encrypt_password
from database import create_database, Credential, Password, LoginCredentials
from utils import clear_input_fields, check_if_fields_not_missing
import os
from dotenv import load_dotenv


class AddPassword:
    """ Class for adding password records """
    def __init__(self, tab, credentials, username, update_password, delete_password):
        """
        Initialize the AddPassword instance.

        Parameters:
            tab (tkinter.Tk): The tab in which the UI elements should be created.
            credentials: Containing credentials data.
            update_password (callable): A function to update password data.
            delete_password (callable): A function to delete password data.
        """
        self.credentials = credentials
        self.username = username
        self.update_password = update_password
        self.delete_password = delete_password

        website_label = ctk.CTkLabel(tab, text='Website', anchor='w')
        self.website = ctk.CTkEntry(tab, width=200, corner_radius=10)
        website_label.grid(row=0, column=0, padx=90, pady=5, sticky='w')
        self.website.grid(row=0, column=1, pady=5)

        login_label = ctk.CTkLabel(tab, text='Login')
        self.login = ctk.CTkEntry(tab, width=200, corner_radius=10)
        login_label.grid(row=1, column=0, padx=90, pady=5, sticky='w')
        self.login.grid(row=1, column=1, pady=5)

        password_label = ctk.CTkLabel(tab, text='Password', anchor='w')
        self.password = ctk.CTkEntry(tab, show='*', width=200, corner_radius=10)
        password_label.grid(row=2, column=0, padx=90, pady=5, sticky='w')
        self.password.grid(row=2, column=1, pady=5)

        add_password_button = ctk.CTkButton(tab, text='Add password')
        add_password_button.place(relx=0.35, rely=0.85, anchor="center")
        add_password_button.bind('<Button-1>', lambda event: self.insert_data_and_update_ui(event))

        def generate_password():
            letters = string.ascii_letters
            digits = string.digits
            special = '!@#$%^&*<>?|()'
            password = ''.join(
                random.sample(letters, 16) + (random.sample(special, 2)) + random.sample(digits, 2)
                )
            list_password = list(password)
            random.shuffle(list_password)
            shuffled_password = ''.join(list_password)

            self.password.delete(0, tk.END)
            self.password.insert(0, shuffled_password)

        add_generate_password_button = ctk.CTkButton(tab, text='Generate password')
        add_generate_password_button.place(relx=0.65, rely=0.85, anchor="center")
        add_generate_password_button.configure(
            command=generate_password
        )

    @staticmethod
    def update_credentials_treeview(tree_name, table_name, username):
        """
        Updates the items in a Treeview widget with data retrieved from a specified database table.

        This static method clears the current Treeview contents and, if a table name is provided,
        queries the database for all records in that table. It then inserts each record's 'website'
        and 'login' information as a new entry in the Treeview.

        Parameters:
        - tree_name (tkinter.Treeview): The Treeview widget instance to update.
        - table_name (sqlalchemy.Table): The database table object from which to retrieve data.

        Returns:
        - None
        """
        tree_name.delete(*tree_name.get_children())

        if table_name:
            session = create_database()
            user_username = session.query(LoginCredentials).filter_by(username=username).first()
            data = session.query(table_name).all()

            for record in data:
                if record.username_id == user_username.id:
                    tree_name.insert('', 'end', values=(record.website, record.login))

    def insert_data_and_update_ui(self, event):
        """
        Insert data from input fields into the database and update the user interface.

        This method performs the following steps:
        1. Retrieves values from the website, login, and password input fields.
        2. Validates if any of the required fields are missing (website, login, or password).
        3. If any required field is missing,
           it displays an info message and clears the input fields.
        4. If all required fields are provided,
           it checks if the data already exists in the database.
        5. If the data exists, it displays an info message and clears the input fields.
        6. If the data does not exist, it validates the password and checks for any errors.
        7. If the password is valid,
           it adds the credential and encrypted password data to the database.
        8. It updates the credentials treeview in the UI with the new data.
        9. It clears the input fields and displays an info message.

        Parameters:
            event: The event that triggered the function (not used here).
        """

        load_dotenv()
        key = os.environ.get('KEY')
        website_value = self.website.get()
        login_value = self.login.get()
        password_value = self.password.get()
        
        missing_fields= check_if_fields_not_missing(
            website = self.website.get(),
            login = self.login.get(),
            password = self.password.get()
        )
        
        clear_input_fields(self.website, self.login, self.password)

        if missing_fields:
            session = create_database()
            user = session.query(LoginCredentials).filter_by(username=self.username).first()
            if user:
                query = session.query(Credential).filter_by(
                    website=website_value,
                    login=login_value,
                    username_id=user.id
                    ).first()
                if query:
                    messagebox.showinfo('Info', 'The data is already in the database')
                    clear_input_fields(self.website, self.login, self.password)

                else:
                    valid, errors = main.validate_password(api.Api(password_value))
                    if valid:
                        credential = Credential(website=website_value,
                                                login=login_value,
                                                username_id=user.id)
                        password_data = (
                            Password(password=encrypt_password(key, password_value),
                                    credential=credential)
                                    )

                        session.add(credential)
                        session.add(password_data)
                        session.commit()

                        self.update_credentials_treeview(tree_name=self.credentials.tree,
                                                        table_name=Credential,
                                                        username=self.username)
                        self.update_credentials_treeview(tree_name=self.update_password.tree,
                                                        table_name=Credential,
                                                        username=self.username)
                        self.update_credentials_treeview(tree_name=self.delete_password.tree,
                                                        table_name=Credential,
                                                        username=self.username)

                        clear_input_fields(self.website, self.login, self.password)
                        messagebox.showinfo('Info', 'Credentials were added')

                    else:
                        error_messages = '\n'.join([f' - {error}\n' for _, error in errors])
                        messagebox.showerror(
                            'Error',
                            f'The provided password does not meet the following requirements:\n \n{error_messages}'
                        )
                        clear_input_fields(self.website, self.login, self.password)
                        