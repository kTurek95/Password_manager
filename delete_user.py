"""
This module contains the DeleteUser class,
which manages the process of deleting users from a database.
It uses the customtkinter library to create a graphical interface
and the 'database' module for database interactions.

Classes:
    DeleteUser:
    Manages the user interface and logic for deleting users from the database.
"""


from tkinter import messagebox
import customtkinter as ctk
from database import create_database
from database import LoginCredentials
from utils import get_users_from_database

class DeleteUser:
    """
    A class for managing the process of deleting users from the system.

    This class creates a user interface for the delete user from database.

    Attributes:
        delete_tab:
            The widget (usually a tab in the user interface)
            where the class operates.
        checkboxes:
            A list storing checkboxes for each user.
    Methods:
        display_users():
            Displays a list of users with options to select them for deletion.
        delete_user():
            Deletes the selected user from the database.
        delete_button():
            Creates a button for submitting the delete operation.
        on_check(selected_var):
            Manages the logic of selecting only one checkbox at a time.
    """
    def __init__(self, delete_tab):
        """
        Initializes the DeleteUser class.

        Args:
            delete_tab:
                The widget (usually a tab in the user interface) where the class will operate.
        """
        self.delete_tab = delete_tab
        self.checkboxes = []

    def display_users(self):
        """
        Displays a list of users from the database in the form of checkboxes,
        allowing their selection for deletion.
        Each user is represented as a separate checkbox.
        """
        for widget in self.delete_tab.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.delete_tab,
                             text='Choose account to delete:',
                             corner_radius=10,
                             fg_color=("white", "gray"))
        label.pack(pady=20)

        users = get_users_from_database()
        for user in users:
            check_var = ctk.BooleanVar()
            my_check = ctk.CTkCheckBox(self.delete_tab, text=user, variable=check_var,
                                    command=lambda var=check_var: self.on_check(var))
            my_check.pack()
            self.checkboxes.append((check_var, user))
        self.delete_button()

    def delete_user(self):
        """
        Deletes the selected user from the database.
        The selected user is removed,
        and an informational message about the successful deletion is displayed.
        """
        session = create_database()
        selected_user = [user for check_var, user in self.checkboxes if check_var.get()][0]
        user = session.query(LoginCredentials).filter_by(username=selected_user).first()
        if user:
            session.delete(user)
            session.commit()
            messagebox.showinfo('Info', 'The user has been deleted.')

    def delete_button(self):
        """
        Creates a 'Submit' button which, when pressed,
        initiates the process of deleting the selected user
        and refreshes the list of users.
        """
        delete_button = ctk.CTkButton(self.delete_tab,
                                      text='Submit',
                                      command=lambda: (self.delete_user(),
                                                       self.display_users()))
        delete_button.pack(pady=20)

    def on_check(self, selected_var):
        """
        Manages the logic of checkbox selection,
        allowing only one checkbox to be selected at a time.

        Args:
            selected_var:
                The BooleanVar variable associated with the currently selected checkbox.
        """
        for check_var, _ in self.checkboxes:
            if check_var is not selected_var:
                check_var.set(False)
