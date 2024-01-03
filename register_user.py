import tkinter as tk
import sqlite3
from tkinter import messagebox
import customtkinter as ctk
from database import create_database, LoginCredentials
from send_email import Email

class RegisterUser:
    def __init__(self, tab):
        self.tab = tab

        register_username_label = ctk.CTkLabel(tab, text='Username')
        register_username_label.place(x=15, y=1)
        register_username = ctk.CTkEntry(tab, width=120)
        register_username.place(x=15, y=31)

        register_email_label = ctk.CTkLabel(tab, text='Email')
        register_email_label.place(x=170, y=1)
        register_email = ctk.CTkEntry(tab, width=120)
        register_email.place(x=170, y=31)

        register_password_label = ctk.CTkLabel(tab, text='Password')
        register_password_label.place(x=15, y=61)
        register_password = ctk.CTkEntry(tab, width=120, show='*')
        register_password.place(x=15, y=91)

        register_confirm_password_label = ctk.CTkLabel(tab, text='Confirm Password')
        register_confirm_password_label.place(x=170, y=61)
        register_confirm_password = ctk.CTkEntry(tab, width=120, show='*')
        register_confirm_password.place(x=170, y=91)

        def insert_credentials_into_database():
            credentials_username = register_username.get()
            credentials_password = register_password.get()
            credentials_confirm_password = register_confirm_password.get()
            credentials_email = register_email.get()

            if credentials_password != credentials_confirm_password:
                messagebox.showerror('Error', 'The password do not match')
                register_username.delete(0, tk.END)
                register_password.delete(0, tk.END)
                register_confirm_password.delete(0, tk.END)
                register_email.delete(0, tk.END)
            else:
                session = create_database()

                def check_if_user_exist(username, email):
                    connection = sqlite3.connect('database.db')
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM LoginCredentials WHERE"
                                   " username=? or email=?", (username, email))
                    existing_user = cursor.fetchone()
                    connection.close()

                    return existing_user is not None

                if check_if_user_exist(credentials_username, credentials_email):
                    messagebox.showerror(
                        'Error',
                        'An account with the provided details already exists, please try again.'
                    )
                else:
                    login_credentials = LoginCredentials(
                        username=credentials_username,
                        password=credentials_password,
                        confirm_password=credentials_confirm_password,
                        email=credentials_email)
                    session.add(login_credentials)

                    email_object = Email(credentials_email, credentials_username)
                    email_object.send_mail()

                    messagebox.showinfo('Info', 'Thank you, your account has just been registered.')
                    session.commit()
                    register_username.delete(0, tk.END)
                    register_password.delete(0, tk.END)
                    register_confirm_password.delete(0, tk.END)
                    register_email.delete(0, tk.END)

        register_button = ctk.CTkButton(tab,
                                        command=insert_credentials_into_database,
                                        text='Register')
        register_button.place(x=82, y=125)
