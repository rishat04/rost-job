import sqlite3

class User:

    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread = False)
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT
                )
            ''')

    def add(self, user_id, username):
        self.cursor.execute('INSERT INTO User VALUES(?,?)', [user_id, username])
        self.connect.commit()

    def is_user_exists(self, user_id):
        row = self.get_users()
        res = list(map(lambda u: user_id in u, row))
        return True in res

    def update_user_name(self, username, user_id):
        self.cursor.execute('UPDATE User set name=? WHERE user_id=?', [username, user_id])
        self.connect.commit()

    def get_users(self):
        self.cursor.execute('SELECT name, user_id FROM User')
        row = self.cursor.fetchall()
        return row

    def get_name_by_id(self, user_id):
        self.cursor.execute('SELECT name FROM User WHERE user_id = ?', [user_id])
        return self.cursor.fetchone()[0]

    def show(self):
        self.cursor.execute('SELECT * FROM User')
        #print(self.cursor.fetchall())
