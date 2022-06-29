import sqlite3

class Application:

    def __init__(self):
        self.connect = sqlite3.connect('database.db', check_same_thread = False)
        self.cursor = self.connect.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Application (
                    dep_id INTEGER,
                    comp_id INTEGER,
                    user_id INTEGER,
                    admin_id INTEGER,
                    description TEXT,
                    status TEXT,
                    header TEXT,
                    priority TEXT,
                    date TEXT,
                    FOREIGN KEY (dep_id) REFERENCES Departament(rowid),
                    FOREIGN KEY (comp_id) REFERENCES Company(rowid),
                    FOREIGN KEY (user_id) REFERENCES User(user_id),
                    FOREIGN KEY (admin_id) REFERENCES AdminDepartament(admin_id)
                )
            ''')
    
    def add(self, dep_id, comp_id, user_id, admin_id, description, header, priority, date_now):
        self.cursor.execute('INSERT INTO Application VALUES(?,?,?,?,?,?,?,?,?)',
            [dep_id, comp_id, user_id, admin_id, description, 'На рассмотрении', header, priority, date_now]
        )
        self.connect.commit()

    def get_applications(self, user_id):
        self.cursor.execute('''SELECT Application.rowid, Departament.dep_name, Company.company_name, User.name, Application.admin_id, description, status, header, priority, date
                            FROM Application 
                            JOIN Departament ON Application.dep_id = Departament.rowid
                            JOIN Company ON Application.comp_id = Company.rowid
                            JOIN User ON Application.user_id = User.user_id
                            JOIN AdminDepartament ON Application.admin_id = AdminDepartament.admin_id WHERE Application.user_id = ?''', [user_id])
        return self.cursor.fetchall()

    def get_applications_for_admin(self, admin_id):
        self.cursor.execute('''SELECT Application.rowid, Departament.dep_name, Company.company_name, User.name, Application.admin_id, description, status, header, priority, date
                            FROM Application 
                            JOIN Departament ON Application.dep_id = Departament.rowid
                            JOIN Company ON Application.comp_id = Company.rowid
                            JOIN User ON Application.user_id = User.user_id
                            JOIN AdminDepartament ON Application.admin_id = AdminDepartament.admin_id WHERE Application.admin_id = ?''', [admin_id])
        return self.cursor.fetchall()

    def edit_status(self, id, status):
        self.cursor.execute(f'UPDATE Application SET status="{status}" WHERE rowid={id}')
        self.connect.commit()

    def get_header_by_user_id(self, user_id):
        self.cursor.execute('SELECT header FROM Application WHERE user_id=?', [user_id])
        return self.cursor.fetchone()[0]

    def get_header_by_admin_id(self, admin_id):
        self.cursor.execute('SELECT header FROM Application WHERE admin_id=?', [admin_id])
        return self.cursor.fetchone()[0]

    def get_user_by_application(self, header):
        self.cursor.execute('SELECT user_id FROM Application WHERE header=?', [header])
        return self.cursor.fetchone()[0]

    def get_header(self, app_id):
        self.cursor.execute('SELECT header FROM Application WHERE rowid=?', [app_id])
        return self.cursor.fetchone()[0]

    def get_user_id(self, app_id):
        self.cursor.execute('SELECT user_id FROM Application WHERE rowid=?', [app_id])
        return self.cursor.fetchone()[0]

    def show(self):
        self.cursor.execute('SELECT * FROM Application')
        print(self.cursor.fetchall())

    