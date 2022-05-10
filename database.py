import json
import os
import sys
import sqlite3

class database:
    fullFilePath = lambda self, filename : os.path.join(self.dataDir, filename)

    def __init__(self, dataFilename="data.db", dataDir=None):
        """Set the data directory for the database"""
        self.dataFilename = dataFilename
        if dataDir != None:
            self.dataDir = dataDir
        else:
            if "--data-dir" in sys.argv:
                self.dataDir = sys.argv[sys.argv.index("--data-dir") + 1]
            else:
                self.dataDir = os.path.dirname(__file__)

    def connect(self):
        """Load the database"""
        os.makedirs(self.dataDir, exist_ok=True)
        filename = self.fullFilePath(self.dataFilename)
        con = sqlite3.connect(filename)
        cur = con.cursor()
        return con, cur

    def createTables(self):
        """Create tables if they dont exist"""
        con, cur = self.connect()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                username VARCHAR not null,
                password VARCHAR not null,
                accessLevel INTEGER not null
            )
        """)
        con.commit()
        con.close()