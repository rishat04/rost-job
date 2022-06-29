import sqlite3

class Company:

    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread = False)
        self.cursor = self.connect.cursor()
        
        self.cursor.execute('PRAGMA foreign_keys = ON')
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Company (
                    company_name TEXT
                )
            ''')

    def add(self, company_name):
        self.cursor.execute('INSERT INTO Company(company_name) VALUES(?)', [company_name])
        self.connect.commit()

    def delete(self, comp_id):
        self.cursor.execute('DELETE FROM Company WHERE rowid=?', [comp_id])
        self.connect.commit()

    def get_companies(self):
        self.cursor.execute('SELECT company_name, rowid FROM Company')
        return self.cursor.fetchall()

    def get_id_by_name(self, company_name):
        self.cursor.execute('SELECT rowid FROM Company WHERE company_name = ?', [company_name])
        return self.cursor.fetchone()[0]

    def show(self):
        self.cursor.execute('SELECT * From company')
        print(self.cursor.fetchall())