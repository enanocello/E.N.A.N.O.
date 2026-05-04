import questionary as qt
from typing import Literal
from rich.table import Table
from rich.console import Console

def confirm(type: Literal["write","select","addCourse"],whatever = None):
    if type == "write":
        return qt.confirm(f"You wrote {whatever}. Confirm?").ask()
    elif type == "select":
        return qt.confirm(f"You selected {whatever}. Confirm?").ask()
    elif type == "addCourse":
        return qt.confirm("Add the following course?").ask()

def dbError():
    qt.print("There was an internal database error, please try again later.",style="bold red")
    qt.press_any_key_to_continue().ask()
def dbCourseExists():
    qt.print("Course already exists in this semester",style="bold red")
    qt.press_any_key_to_continue().ask()
def dbAddCourseSuccess():
    qt.print("Course added succesfully",style="bold green")
    qt.press_any_key_to_continue().ask()

def length(text,maxLength):
    if text != "" and len(text) <= maxLength:
        return confirm("write",text)

def courseSemester():
    while True:
        semester = qt.select(
            "Select the semester",
            choices=["2026-1",
                    "2026-2",]
            ).ask()
        if confirm("select",semester):
            return semester

def courseCode():
    while True:
        courseCode = (qt.text("Type the course code (e.g. MAT-021)").ask()).upper()
        if length(courseCode,10):
            return courseCode
        else:
            qt.print("Write a valid option\n(Not empty and 10 characters max)",style="bold red")

def courseName():
    while True:
        courseName = (qt.text("Type the course name").ask()).upper()
        if length(courseName,80):
            return courseName
        else:
            print("Write a valid option\n(Not empty and 80 characters max)",style="bold red")

def printCourseTable(courseSemester,courseCode,courseName):
    # GET THE TABLE READY
    table = Table()
    table.add_column("Code", justify="center", style="cyan")
    table.add_column("Name", justify="center", style="cyan")
    table.add_column("Semester", justify="center", style="cyan")
    table.add_row(courseCode,courseName,courseSemester)
    # PRINT THE TABLE
    console = Console(); console.print(table)