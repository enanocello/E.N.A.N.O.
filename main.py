import sqlite3
import os
import interface
import dashboard

dbDirectory = "/home/enano/Documents/E.N.A.N.O./enano.db"

def clear():
    os.system("clear")

def main():
    try:
        # Try to connect to db
        conn = sqlite3.connect(dbDirectory)
        cursor = conn.cursor()
    except Exception:
        input("There is an error trying to connect the database\nPress [enter] to exit")
        return
    
    dashboard.dashboard(cursor,conn)
    interface.modifyMenu(cursor, conn)

    conn.close()
    clear();input("See you dude :b");clear()

if __name__ == "__main__":
    main()