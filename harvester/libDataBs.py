import os
import sqlite3


# Simple sqlite wrapper
# Should be used with 'with' keyword to ensure proper initialization and closure of database
class DataBs:
    def __init__(self):
        archive_dir = os.environ['HOME'] + os.sep + "archive"
        harvester_db = archive_dir + os.sep + "harvester.db"

        self.db = sqlite3.connect(harvester_db)
        self.curse = self.db.cursor()
        self.curse.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='harvs'")
        if not self.curse.fetchone():
            self.curse.execute("CREATE TABLE harvs(hash TEXT PRIMARY KEY, filename TEXT, count INTEGER)")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()

    def checkHashExistence(self, hash):
        """Check if given hash is already in the database."""
        self.curse.execute("SELECT hash, filename, count FROM harvs WHERE hash = ?", [hash])
        if self.curse.fetchone():
            return True
        else:
            return False

    def insertData(self, dct):
        """Insert hash, filename and count into database."""
        if self.checkHashExistence(dct['hash']):
            return False
        else:
            self.curse.execute('''INSERT INTO harvs(hash, filename, count)
                VALUES(:hash,:filename, :count)''', dct)
            return True

    def upCount(self, hash):
        if not self.checkHashExistence(hash):
            return False
        else:
            self.curse.execute("UPDATE harvs SET count= count + 1 WHERE hash = ?", [hash])
            return True

    def gibData(self, hash):
        if not self.checkHashExistence(hash):
            return
        else:
            self.curse.execute("SELECT hash, filename, count FROM harvs WHERE hash=?", [hash])
            return [i for i in self.curse.fetchone()]

#
'''
d = {
            'hash': 'faf0e9ab400ef5a7e1a9ea55277fa559',
            'filename': '1414478734164',
            'count':  1
    }
with DataBs() as dbs:
    print check(d['hash'])
    dbs.set(d)
    dbs.upCount(d['hash'])
    print check(d['hash'])
    print dbs.gibData(d['hash'])
    print 'kek'
'''
