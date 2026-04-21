import sqlite3
import os
import controlPanel
import dashboard
import art
import questionary as qt

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
    
    while True:
        clear()
        qt.print(art.enano(),style="bold magenta")

        option = qt.select(
                "Select an option!",
                choices=["Dashboard",
                        "Control Panel",
                        "Exit"]
                ).ask()
        if option == "Dashboard":       dashboard.dashboard(cursor,conn)
        elif option == "Control Panel":   controlPanel.controlPanel(cursor,conn)
        elif option == "Exit":
            if qt.confirm("Are you sure?").ask(): break

    conn.close()
    clear()

if __name__ == "__main__":
    main()