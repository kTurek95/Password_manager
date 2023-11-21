from tkinter import ttk
import tkinter as tk
from check_password import CheckPassword


def on_closing():
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Password Manager')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.geometry('250x100')
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')

    password_from_user_label = ttk.Label(root, text='Input password')
    password_from_user_label.place(relx=0.5, rely=0.2, anchor="center")

    password_from_user = ttk.Entry(root, show='*')
    password_from_user.place(relx=0.5, rely=0.45, anchor="center")

    check_password_instance = CheckPassword(password_from_user, root)

    add_submit_button = ttk.Button(root, text='Submit')
    add_submit_button.place(relx=0.5, rely=0.75, anchor="center")
    add_submit_button.bind('<Button-1>', lambda event: check_password_instance.on_submit(event))

    root.mainloop()