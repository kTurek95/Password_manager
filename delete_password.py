import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from database import create_database, Credential
from update_treeview import UpdateTreeview


class DeletePassword(UpdateTreeview):
    """
    A class derived from UpdateTreeview, designed to handle the deletion of passwords.

    The DeletePassword class is responsible for setting up a user interface in a given tab
    of an application where users can select and delete credentials. It inherits from the
    UpdateTreeview class, leveraging its capabilities to update the display of credentials.

    This class manages a treeview widget along with a scrollbar for the user to interact with
    the credentials data. It allows for the selection and deletion of credentials through the UI.

    Attributes:
    - credentials (list): A list containing the credentials data.
    - update_password (function): A reference to a function used to update the password data.
    - tab (tkinter widget): The tab in which this UI component will be displayed.
    - scrollbar (tk.Scrollbar): A scrollbar for the treeview.
    - tree (ttk.Treeview): A treeview widget to display the credentials.
    """
    def __init__(self, tab, credentials, update_password, table_name):
        """
        Initializes the DeletePassword class with the given parameters.

        This constructor initializes the DeletePassword instance, setting up the necessary widgets
        and configurations for the user interface in the specified tab. It calls the constructor of
        its superclass (UpdateTreeview) with the table name and sets up the treeview and scrollbar
        for displaying credentials.

        Parameters:
        - tab (tkinter widget): The tab in which this UI component will be displayed.
        - credentials (list): A list of credentials that will be managed. Each credential should be
                               a dictionary with relevant keys and values.
        - update_password (function): A function to call for updating passwords. This function should
                                      handle the logic for password modification in the application's backend.
        - table_name (str): The name of the table to be updated, passed to the UpdateTreeview superclass.
        """
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
        self.tree['columns'] = ('first',)
        self.tree.column('first', stretch=tk.YES)
        self.tree.heading('first', text='Choose website credential to delete')
        self.scrollbar.config(command=self.tree.yview)
        self.tree.pack(expand=True, fill='both')
        self.scrollbar.place(x=490, rely=0.32, anchor='center', height=99)

        add_tree3_button = ctk.CTkButton(self.tab, text='Submit')
        add_tree3_button.place(relx=0.5, rely=0.9, anchor="center")
        add_tree3_button.bind('<Button-1>', lambda event: self.delete_credentials(event))

    def delete_credentials(self, event):
        """
        Deletes selected credentials from the database and updates the treeview.

        This method is triggered by an event (typically a button click or a selection change).
        It first checks if an item is selected in the treeview. If an item is selected, it confirms
        with the user if they indeed want to delete the selected credential. Upon confirmation, it
        queries the database for the corresponding credential and deletes it. After the deletion,
        the treeview is updated to reflect the changes.

        Parameters:
        - event: The event that triggered this method. Not used in the method but typically required
                 for event handling in Tkinter.
        """
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
