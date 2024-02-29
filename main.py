"""
This module defines the main functionality for the Password Manager application,
allowing users to log in, register, and delete their accounts. It utilizes custom
Tkinter widgets for the graphical user interface components.
"""

import customtkinter as ctk
from register_user import RegisterUser
from login_to_app import LoginToApp
from delete_user import DeleteUser
from center_window import center_window
from users import Users


def open_login_window():
    """
    Opens the login window for the Password Manager application.
    
    This function creates a graphical user interface for the Password Manager application,
    allowing users to log in, register, and delete their accounts.
    """
    root = ctk.CTk()
    root.title('Password Manager')
    ctk.set_appearance_mode('Dark')
    root.geometry('220x130')
    root.resizable(False, False)

    def on_closing():
        root.destroy()

    my_tab = ctk.CTkTabview(root)
    my_tab.pack(fill='both', expand=True, pady=15, padx=15)

    users_tab = my_tab.add('Users')
    login_tab = my_tab.add('Login')
    register_tab = my_tab.add('Register')
    delete_tab = my_tab.add('Delete User')

    my_frame = ctk.CTkScrollableFrame(delete_tab)
    my_frame.pack()

    RegisterUser(register_tab)

    LoginToApp(login_tab, root, my_tab)
    user_instance = Users(users_tab, login_tab, root, my_tab)
    user_instance.display_login_users()
    deleteuser_instance = DeleteUser(my_frame)
    deleteuser_instance.display_users()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    center_window(root)
    root.mainloop()


if __name__ == '__main__':
    open_login_window()
