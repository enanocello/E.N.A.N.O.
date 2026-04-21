import os
import questionary as qt
import controlPanel
import art
from rich import print
from rich.console import Console
from rich.table import Table

def clear(): os.system("clear")

def getInfo(cursor):
    cursor.execute("""SELECT
                   exam.id,
                   course.courseName,
                   exam.examType,
                   date(examDate) as examDate,
                   exam.examContent,
                   CAST(julianday(DATE(examDate)) - julianday(DATE('now','localtime')) AS INTEGER) AS daysLeft 
                   FROM exam
                   JOIN course ON exam.courseID = course.id 
                   WHERE date(examDate) >= date('now','localtime') 
                   AND date(examDate) <= date('now','localtime','+14 days')
                   ORDER BY examDate
                   """)
    exams = cursor.fetchall()
    return exams

def dashboard(cursor,conn):
    while True:
        clear()
        info = getInfo(cursor)
        qt.print(art.dashboard(), style="bold cyan")
        
        table = Table(title="Exams in the next 14 days")
        table.add_column("Course name", style="bold cyan")
        table.add_column("Exam type",   style="red")
        table.add_column("Exam date",   style="bold magenta")
        table.add_column("Days left",   style="bold yellow")
        table.add_column("Exam content",style="green")
        for examID,courseName,examType,examDate,examContent,daysLeft, in info:
            if daysLeft == 0: daysLeft = "Today"
            elif daysLeft == 1: daysLeft = "Tomorrow"
            else: daysLeft = f"{daysLeft} days left"
            table.add_row(courseName,examType,examDate,daysLeft,str(examContent))


        console = Console(); console.print(table)

        answer = qt.select(
                "Select an option!",
                choices=["Control Panel",
                        "Refresh",
                        "Return to main menu"]
                ).ask()
        
        if answer == "Control Panel":
            controlPanel.controlPanel(cursor,conn)
            return
        elif answer == "Return to main menu": return