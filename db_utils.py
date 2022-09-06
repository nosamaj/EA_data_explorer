# db_utils.py
import os
import sqlite3
from pathlib import Path
home = str(Path.home())

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = home+'/db/database.sqlite3'

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con