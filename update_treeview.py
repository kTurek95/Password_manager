from database import create_database


class UpdateTreeview:
    def __init__(self, table_name):
        self.table_name = table_name

    def update_credentials_treeview(self, tree_name):
        tree_name.delete(*tree_name.get_children())

        if self.table_name:
            session = create_database()
            data = session.query(self.table_name).all()

            for record in data:
                tree_name.insert('', 'end', values=(record.website, record.login))
