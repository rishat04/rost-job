import sqlite3

class Departament:

    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread = False)
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Departament (
                    comp_id INTEGER,
                    dep_name TEXT
                )
            ''')

    def add(self, dep_name, comp_id):
        self.cursor.execute('INSERT INTO Departament(comp_id, dep_name) VALUES(?,?)', [comp_id, dep_name])
        self.connect.commit()

    def delete(self, dep_id):
        self.cursor.execute('DELETE FROM Departament WHERE rowid=?', [dep_id])
        self.connect.commit()

    def get_departaments(self):
        self.cursor.execute('SELECT dep_name, rowid FROM Departament')
        return self.cursor.fetchall()

    def get_departaments_by_company(self, comp_id):
        self.cursor.execute('SELECT dep_name, rowid FROM Departament WHERE comp_id=?', [comp_id])
        return self.cursor.fetchall()

    def get_id_by_name(self, dep_name):
        self.cursor.execute('SELECT rowid FROM Departament WHERE dep_name = ?', [dep_name])
        return self.cursor.fetchone()[0]

    def edit_departament_name(self, dep_name, rowid):
        self.cursor.execute('UPDATE Departament SET dep_name=? WHERE rowid=?', [dep_name, rowid])
        self.connect.commit()

    def show(self):
        self.cursor.execute('SELECT * From Departament')
        print(self.cursor.fetchall())