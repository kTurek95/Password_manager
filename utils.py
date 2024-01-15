import customtkinter as ctk
from tkinter import messagebox
from database import create_database
from database import LoginCredentials

def clear_input_fields(*args):
    """
    Clear input fields in the UI.

    This method clears the website, login, and password input fields.
    """

    for field in args:
        field.delete(0, ctk.END)


def get_users_from_database(username=None):
    """
    If a username is provided, 
    retrieves the user's password. If no username is provided, 
    retrievesthe user's usernames.

    Parameters:
        username (str, optional): The username of the user whose password is to be retrieved. 
                                If None, all usernames are retrieved. Defaults to None.

    Returns:
        list: A list of usernames if no username is provided. If a username is provided, 
            returns a list containing the user password.
    """
    users = []
    session = create_database()
    if not username:
        all_users = session.query(LoginCredentials).all()
        for user in all_users:
            users.append(user.username)
    else:
        user = session.query(LoginCredentials).filter_by(username=username).first()
        users.append(user.password)

    return users

def move_user(tabview, tab_name):
    """
    Switches the user's view to a specified tab in the tabview interface.

    Takes a tabview control (e.g., a ttk.Notebook widget) and a tab name (tab_name),
    then sets the active tab to the one indicated by tab_name.

    Parameters:
        tabview: The tab control widget where the active tab is to be changed.
        tab_name: The name of the tab (string) to switch the view to.

    Returns:
        None
    """
    tabview.set(tab_name)


def check_if_fields_not_missing(**kwargs):
    """
    Check if any of the provided keyword arguments (fields) are missing or empty.

    This function iterates through each key-value pair in the kwargs. If the value associated with
    a key is an empty string (or only contains whitespace), the key is considered as a missing field.

    Args:
        **kwargs: A variable number of keyword arguments. Each argument represents a field 
                  with its value as the field's content.

    Returns:
        bool: True if all fields are non-empty, False otherwise.
    """
    missing_fields = []
    for key, value in kwargs.items():
        if not value.strip():
            missing_fields.append(key)


    if missing_fields:
                messagebox.showinfo('Info',f"You didn't enter the {', '.join(missing_fields)}")
                return False
    return True