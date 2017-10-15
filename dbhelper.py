import sqlite3


class DBHelper:
    def __init__(self, dbname='homework.sqlite'):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)



    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS assignments (description text, student text)"
        hwaidx = "CREATE INDEX IF NOT EXISTS hwaIndex ON assignments (description ASC)"
        stuidx = "CREATE INDEX IF NOT EXISTS stuIndex ON assignments (student ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(hwaidx)
        self.conn.execute(stuidx)
        self.conn.commit()

    def add_assignment(self, assignment_text, student):
        stmt = "INSERT INTO assignments (description, student) VALUES (?, ?)"
        args = (assignment_text, student)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_assignment(self, assignment_text, student):
        stmt = "DELETE FROM assignments WHERE description = (?) AND student = (?)"
        args = (assignment_text, student)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_assignments(self, student):
        stmt = "SELECT description FROM assignments WHERE student = (?)"
        args = (student, )
        return [x[0] for x in self.conn.execute(stmt, args)]