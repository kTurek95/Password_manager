from tkinter import ttk


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
