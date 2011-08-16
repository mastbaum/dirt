import os
import sqlite3


if False:
  print settings['db']
  class SQLiteManager:
    def __init__(self, path):
        if os.path.isabs(path):
            self.path = path
        else:
            here = os.path.dirname(os.path.abspath(__file__))
            self.path = os.path.join(here, path)
    def execute(self, query):
        db = sqlite3.connect(self.path)
        rs = db.execute(query)
        db.close()
        return rs



