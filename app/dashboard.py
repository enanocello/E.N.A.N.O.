import questionary as qt
import app.ascii as ascii

from utils.terminal import clear
import services.dashboardService as dashboardService
import utils.prompts as prompts

def dashboard(cursor):
    clear()
    qt.print(ascii.dashboard(), style="bold cyan")

    # Gets the exams in the next 2 weeks
    upcomingExams = dashboardService.getUpcomingExams(cursor)
    # Prints the table with the exams
    prompts.printUpcomingExams(upcomingExams)

    prompts.pressAnyKey()