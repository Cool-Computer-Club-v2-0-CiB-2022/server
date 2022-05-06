import json
import os
import sys


class database:
    fullFilePath = lambda self, filename : os.path.join(self.dataDir, filename)

    def __init__(self, dataFilename="data.json", dataDir=None):
        """Set the data directory for the database"""
        self.dataFilename = dataFilename
        if dataDir != None:
            self.dataDir = dataDir
        else:
            if "--data-dir" in sys.argv:
                self.dataDir = sys.argv[sys.argv.index("--data-dir") + 1]
            else:
                self.dataDir = os.path.join(os.path.dirname(__file__), "data")

    def load(self):
        """Load the database"""
        os.makedirs(self.dataDir, exist_ok=True)

        filename = self.fullFilePath(self.dataFilename)

        try:
            # Load database
            with open(filename, "r") as dataFile:
                self.data = json.loads(dataFile.read())
        except:
            try:
                # Cannot load database, try backup
                with open(filename + ".bak", "r") as dataFile:
                    self.data = json.loads(dataFile.read())
            except:
                # Cannot load backup either
                self.data = {}

    def save(self):
        """Save the database"""
        filename = self.fullFilePath(self.dataFilename)

        if os.path.exists(filename):
            try:
                os.remove(filename + ".bak")
            except:
                pass
            os.rename(filename, filename + ".bak")

        with open(filename, "w") as dataFile:
            dataFile.write(json.dumps(self.data, indent=4))
