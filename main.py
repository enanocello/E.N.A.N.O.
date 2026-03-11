import sqlite3
import os
import interface

dbDirectory = "enano.db"

def main():
    try:
        # Try to connect to db
        conn = sqlite3.connect(dbDirectory)
        cursor = conn.cursor()
        print(f"Connection established successfully with '{dbDirectory}'")
    except Exception:
        print(f"Couldn't connect to Database '{dbDirectory}'")
    
    interface.mainMenu(cursor, conn)
    
    conn.close()
    print(f"Connection to Database closed successfully")

if __name__ == "__main__":
    os.system("clear")
    main()
    input()
    os.system("clear")