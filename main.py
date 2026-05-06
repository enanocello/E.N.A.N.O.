import app.ascii as ascii
import services.connectService as connectService
import questionary as qt
from app.dashboard import dashboard
from app.controlPanel import controlPanel, clear
import utils.prompts as prompts

def main():
    conn = connectService.connect()
    cursor = connectService.getCursor(conn)

    # Displays the main menu
    while True:
        clear()
        qt.print(ascii.enano(),style="bold magenta")
        
        option = prompts.mainMenuOptions()
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