"""
This module contains the UpdateTreeview class for updating a Treeview widget.

The UpdateTreeview class is responsible for updating the content of a Treeview widget by
deleting existing items and adding new data based on the provided table name and username.
"""

from database import create_database, LoginCredentials

#pylint: disable=too-few-public-methods
class UpdateTreeview:
    """
    Class responsible for updating the content of a Treeview.
    """
    def __init__(self, table_name):
        """
        Initializes an instance of the UpdateTreeview class.

        Parameters:
            table_name (str): The name of the database table to be updated.
        """
        self.table_name = table_name

    def update_credentials_treeview(self, tree_name, username):
        """
        Updates the content of a Treeview.

        Deletes existing items in the Treeview (tree_name) and then adds new data
        based on the provided username and table (self.table_name).

        Parameters:
            tree_name (tkinter.ttk.Treeview): The Treeview object to be updated.
            username (str): The username based on which data will be selected.
        """
        tree_name.delete(*tree_name.get_children())

        if self.table_name:
            session = create_database()
            user_username = session.query(LoginCredentials).filter_by(username=username).first()
            data = session.query(self.table_name).all()

            for record in data:
                if record.username_id == user_username.id:
                    tree_name.insert('', 'end', values=(record.website, record.login))
