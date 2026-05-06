# This file uses the ASCII file in app folder
# Prints all the titles in the program to make it easier for the user to see the information

from utils.terminal import clear
import app.ascii as ascii
import questionary as qt

def mainTitle():
    clear()
    qt.print(
        f"\n{ascii.enano()}\n",
        style="bold magenta"
    )
def dashboardTitle():
    clear()
    qt.print(
        f"{ascii.enanoSmall()}",
        style="bold magenta"
    )
    qt.print(
        f"{ascii.dashboard()}\n",
        style="bold cyan"
    )
def controlPanelTitle(subtitle = ""):
    clear()
    qt.print(
        f"{ascii.enanoSmall()}",
        style="bold magenta"
    )
    qt.print(
        f"{ascii.controlPanel()}\n{subtitle}\n",
        style="bold yellow"
    )