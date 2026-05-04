import sqlite3
import utils.prompts as prompts

def connect(path):
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        return conn
    except Exception:
        prompts.dbError()
        return

def getCursor(conn):
    try:
        cursor = conn.cursor()
        return cursor
    except:
        prompts.dbError()