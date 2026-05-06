# This file take charge of the DB connection

import utils.prompts as prompts
import sqlite3
from pathlib import Path

# Look up for the absolute path of database
def getAbsolutePath():
    BASE_DIR = Path(__file__).resolve().parent
    absolutePath = BASE_DIR / ".." / "data" / "enano.db"
    return absolutePath

# Connects to DB with the given path
def connect():
    try:
        path = getAbsolutePath()
        conn = sqlite3.connect(path)
        return conn
    except:
        prompts.dbError()
        exit

# Gives the cursor of the connection given
def getCursor(conn):
    try:
        cursor = conn.cursor()
        return cursor
    except:
        prompts.dbError()
        exit