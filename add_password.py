import tkinter as tk
from tkinter import ttk, messagebox
from cipher_tools import encrypt_password
from database import create_database, Credential, Password
from password_package import api, main


class AddPassword:
    def __init__(self, tab, credentials, update_password, delete_password):
        self.credentials = credentials
        self.update_password = update_password
        self.delete_password = delete_password
        website_label = ttk.Label(tab, text='Website')
        self.website = ttk.Entry(tab, width=45)
        website_label.grid(row=0, column=0)
        self.website.grid(row=0, column=1)

        login_label = ttk.Label(tab, text='Login')
        self.login = ttk.Entry(tab, width=45)
        login_label.grid(row=1, column=0)
        self.login.grid(row=1, column=1)

        password_label = ttk.Label(tab, text='Password')
        self.password = ttk.Entry(tab, show='*', width=45)
        password_label.grid(row=2, column=0)
        self.password.grid(row=2, column=1)

        add_password_button = ttk.Button(tab, text='Add password')
        add_password_button.place(relx=0.5, rely=0.7, anchor="center")
        add_password_button.bind('<Button-1>', lambda event: self.insert_data_and_update_ui(event))

    @staticmethod
    def update_credentials_treeview(tree_name, table_name):
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
            data = session.query(table_name).all()

            for record in data:
                tree_name.insert('', 'end', values=(record.website, record.login))

    def clear_input_fields(self):
        self.website.delete(0, tk.END)
        self.login.delete(0, tk.END)
        self.password.delete(0, tk.END)

    def insert_data_and_update_ui(self, event):
        pass