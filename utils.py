import customtkinter as ctk
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
        users = []
        session = create_database()
        if username:
            user_username = session.query(LoginCredentials).filter_by(username=username).first()
            if user_username:
                all_users = session.query(LoginCredentials).all()
                for record in all_users:
                    if record.id != user_username.id:
                        users.append(record.username)
        else:
             all_users = session.query(LoginCredentials).all()
             for record in all_users:
                  users.append(record.username)

        return users