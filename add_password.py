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
        website_value = self.website.get()
        login_value = self.login.get()
        password_value = self.password.get()

        missing_fields = []
        if not website_value.strip():
            missing_fields.append("website")
        if not login_value.strip():
            missing_fields.append("login")
        if not password_value.strip():
            missing_fields.append("password")

        if missing_fields:
            messagebox.showinfo('Info', f'You forgot to add {", ".join(missing_fields)}')
            self.clear_input_fields()

        else:
            session = create_database()
            query = session.query(Credential).filter_by(website=website_value, login=login_value)
            result = query.first()

            if result and result.website == website_value and result.login == login_value:
                messagebox.showinfo('Info', 'The data is already in the database')
                self.clear_input_fields()

            else:
                password = api.Api(password_value)
                valid, errors = main.validate_password(password)
                if valid:
                    credential = Credential(website=website_value, login=login_value)
                    password_data = (
                        Password(password=encrypt_password('kacper95', password_value), credential=credential))

                    session.add(credential)
                    session.add(password_data)
                    session.commit()

                    self.update_credentials_treeview(tree_name=self.credentials.tree, table_name=Credential)
                    self.update_credentials_treeview(tree_name=self.update_password.tree, table_name=Credential)
                    self.update_credentials_treeview(tree_name=self.delete_password.tree, table_name=Credential)

                    self.clear_input_fields()
                    messagebox.showinfo('Info', 'Credentials were added')

                else:
                    error_messages = '\n'.join([f' - {error}\n' for _, error in errors])
                    messagebox.showerror(
                        'Error',
                        f'The provided password does not meet the following requirements:\n \n{error_messages}'
                    )