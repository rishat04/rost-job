import sqlite3
from .admin_base import AdminBase

class AdminDepartament(AdminBase):

    def get_admin_by_departament(self, dep_id):
        self.cursor.execute('SELECT admin_id FROM AdminDepartament WHERE dep_id = ?', [dep_id])
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_dep_name_by_admin(self, admin_id):
        self.cursor.execute('SELECT Departament.dep_name FROM AdminDepartament JOIN Departament on AdminDepartament.dep_id = Departament.rowid')
        row = self.cursor.fetchone()
        if row:
            return row[0]