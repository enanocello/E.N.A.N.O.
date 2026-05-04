import app.ascii as ascii
import services.connectService as connectService
import questionary as qt
from pathlib import Path
from app.dashboard import dashboard
from app.controlPanel import controlPanel, clear

# Look up for the absolute path of database
BASE_DIR = Path(__file__).resolve().parent
dbPath = BASE_DIR / "data" / "enano.db"

def main():
    conn = connectService.connect(dbPath)
    cursor = connectService.getCursor(conn)

    # Displays the main menu
    while True:
        clear()
        qt.print(ascii.enano(),style="bold magenta")
        option = qt.select(
                "Select an option!",
                choices=["Dashboard",
                        "Control Panel",
                        "Exit"]
                ).ask()
        if option == "Dashboard":
            dashboard(cursor)
        elif option == "Control Panel":
            controlPanel(cursor,conn)
        elif option == "Exit":
            if qt.confirm("Are you sure?").ask():
                break

    conn.close()
    clear()

if __name__ == "__main__":
    main()