import tkinter as tk
from tkinter import ttk
from add_password import AddPassword
from credentials import Credentials
from database import Credential
from delete_password import DeletePassword
from center_window import center_window
from update_password import UpdatePassword


def open_main_window(root):
    def on_close():
        root.destroy()

    main_window = tk.Toplevel(root)
    main_window.title('Password Manager')
    main_window.geometry('550x200')
    main_window.resizable(False, False)
    center_window(main_window)

    tabsystem = ttk.Notebook(main_window)

    credentials = ttk.Frame(tabsystem)
    credentials_instance = Credentials(credentials, main_window, table_name=Credential)
    credentials_instance.update_credentials_treeview(credentials_instance.tree)

    add_password = ttk.Frame(tabsystem)
    add_password_instance = AddPassword(
        add_password,
        credentials_instance,
        update_password=None,
        delete_password=None
    )

    update_password = ttk.Frame(tabsystem)
    update_password_instance = UpdatePassword(
        update_password,
        main_window,
        table_name=Credential
    )
    update_password_instance.update_credentials_treeview(update_password_instance.tree)

    delete_password = ttk.Frame(tabsystem)
    delete_password_instance = DeletePassword(
        delete_password,
        credentials_instance,
        update_password_instance,
        table_name=Credential
    )
    delete_password_instance.update_credentials_treeview(delete_password_instance.tree)

    add_password_instance.update_password = update_password_instance
    add_password_instance.delete_password = delete_password_instance

    tabsystem.add(credentials, text='Credentials')
    tabsystem.add(add_password, text='Add Password')
    tabsystem.add(update_password, text='Update Password')
    tabsystem.add(delete_password, text='Delete Password')
    tabsystem.pack(expand=1, fill='both')

    main_window.protocol("WM_DELETE_WINDOW", on_close)
    main_window.mainloop()