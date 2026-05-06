# This file makes the dashboard functional
# In this menu the users can see their upcoming exams

import services.dashboardService as dashboardService
import utils.prompts as prompts
import utils.titles as titles

def dashboard(cursor):
    titles.dashboardTitle()

    # Gets the exams in the next 2 weeks
    upcomingExams = dashboardService.getUpcomingExams(cursor)
    # Prints the table with the exams
    prompts.printUpcomingExams(upcomingExams)

    prompts.pressAnyKey()