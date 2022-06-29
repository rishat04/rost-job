import sqlite3

class AdminBase:

    def __init__(self, table_name, row_name):
        self.table_name = table_name
        self.row_name = row_name

        field = 'Departament' if row_name == 'dep_id' else 'Company'

        self.connect = sqlite3.connect('database.db', check_same_thread = False)
        self.cursor = self.connect.cursor()
        self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    admin_id INTEGER PRIMARY KEY,
                    {self.row_name} INTEGER,
                    FOREIGN KEY ({self.row_name}) REFERENCES {field} ({self.row_name})
                )
            ''')

    def add(self, user_id, obj_id):
        self.cursor.execute(f'INSERT INTO {self.table_name} VALUES(?,?)', [user_id, obj_id])
        self.connect.commit()

    def delete(self, admin_id):
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE admin_id=?', [admin_id])
        self.connect.commit()

    def get_admins(self):
        self.cursor.execute(f'SELECT admin_id FROM {self.table_name}')
        return self.cursor.fetchall()

    def is_admin(self, user_id):
        row = self.get_admins()
        res = list(map(lambda u: user_id in u, row))
        return True in res
    
    def get_company_by_admin(self, admin_id):
        self.cursor.execute(f'SELECT {self.row_name} FROM {self.table_name} WHERE admin_id=?', [admin_id])
        return self.cursor.fetchone()[0]


    def show(self):
        self.cursor.execute(f'SELECT * From {self.table_name}')
        #print(self.cursor.fetchall())
