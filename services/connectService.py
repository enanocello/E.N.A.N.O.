import sqlite3
import utils.prompts as prompts

# Connects to DB with the given path
def connect(path):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        return conn
    except:
        prompts.dbError()
        return

# Gives the cursor of the connection given
def getCursor(conn):
    try:
        cursor = conn.cursor()
        return cursor
    except:
        prompts.dbError()