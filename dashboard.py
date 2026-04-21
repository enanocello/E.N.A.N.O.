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
                   CAST(julianday(examDate) - julianday('now','localtime') AS INTEGER) AS daysLeft 
                   FROM exam
                   JOIN course ON exam.courseID = course.id 
                   WHERE date(examDate) >= date('now','localtime') 
                   AND date(examDate) <= date('now','localtime','+14 days')
                   """)
    exams = cursor.fetchall()
    return exams

def dashboard(cursor,conn):
    while True:
        clear()
        info = getInfo(cursor)
        qt.print(art.dashboard(), style="bold cyan")
        
        table = Table(title="Exams in the next 14 days")
        table.add_column("Exam ID")
        table.add_column("Course name")
        table.add_column("Exam type")
        table.add_column("Exam date")
        table.add_column("Days left")
        table.add_column("Exam content")
        for examID,courseName,examType,examDate,examContent,daysLeft, in info:
            table.add_row(str(examID),courseName,examType,examDate,str(daysLeft)+" days",str(examContent))
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