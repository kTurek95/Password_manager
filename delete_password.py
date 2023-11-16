import tkinter as tk
from tkinter import ttk, messagebox
from database import create_database, Credential
from update_treeview import UpdateTreeview


class DeletePassword(UpdateTreeview):
    def __init__(self, tab, credentials, update_password, table_name):
        super().__init__(table_name)
        self.credentials = credentials
        self.update_password = update_password
        self.tab = tab
        self.scrollbar = tk.Scrollbar(tab, orient='vertical')
        self.tree = ttk.Treeview(
            tab,
            yscrollcommand=self.scrollbar.set,
            columns=('Choose credential',),
            show='headings',
            height=4, )

        self.configure_tree()

    def configure_tree(self):
        self.tree.column('Choose credential', width=480)
        self.tree.heading('Choose credential', text='Choose website credential to delete')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack()
        self.scrollbar.place(x=490, rely=0.36, anchor='center', height=99)

        add_tree3_button = ttk.Button(self.tab, text='Submit')
        add_tree3_button.place(relx=0.5, rely=0.9, anchor="center")
        add_tree3_button.bind('<Button-1>', lambda event: self.delete_credentials(event))

    def delete_credentials(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            selected_website = item.get('values')[0]
            response = messagebox.askyesno('Question', 'Czy na pewno chcesz usunąć hasło?')
            if response:
                session = create_database()
                credential = session.query(Credential).filter_by(website=selected_website).first()
                if credential:
                    session.delete(credential)
                    session.commit()

                    if self.tree.exists(selected_item[0]):
                        self.tree.delete(selected_item[0])

                        self.update_credentials_treeview(tree_name=self.credentials.tree)
                        self.update_credentials_treeview(tree_name=self.update_password.tree)
                        self.update_credentials_treeview(self.tree)

                        messagebox.showinfo('Info', 'Credentials were deleted')
