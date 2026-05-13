# Main file of the program
# Initializes the main menu

import services.connectService as connectService
import utils.prompts as prompts
import utils.titles as titles
from app.controlPanel import controlPanel
from app.dashboard import dashboard
from utils.terminal import clear

def main():
    conn = connectService.connect()
    cursor = connectService.getCursor(conn)

    # Displays the main menu
    while True:
        titles.mainTitle()
        
        option = prompts.mainMenuOptions()
        if option == "Dashboard":
            dashboard(cursor)
        elif option == "Control Panel":
            controlPanel(cursor,conn)
        elif option == "Exit":
            if prompts.confirm("exit"):
                break

    conn.close()
    clear()

if __name__ == "__main__":
    main()