import os
import questionary as qt
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

def dashboard(cursor,info):
    clear()
    qt.print("DASHBOARD", style="bold white")
    info = getInfo(cursor)

    table = Table(title="Exams in the next 14 days")
    table.add_column("Exam ID")
    table.add_column("Course name")
    table.add_column("Exam type")
    table.add_column("Exam date")
    table.add_column("Days left")
    table.add_column("Exam content")
    for examID,courseName,examType,examDate,examContent,daysLeft, in info:
        table.add_row(str(examID),courseName,examType,examDate,str(daysLeft),str(examContent))
    console = Console(); console.print(table)

    input()