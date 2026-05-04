# This file should not work with any cursor or DB connection
# Only prompts or verification functions that doesn't need to touch DB

import questionary as qt
from typing import Literal
from rich.table import Table
from rich.console import Console

def pressAnyKey():
    qt.press_any_key_to_continue().ask()

# VERIFICATION PROMPTS

def confirm(type: Literal["write","select","addCourse"],whatever = None):
    if type == "write":
        return qt.confirm(f"You wrote {whatever}. Confirm?").ask()
    elif type == "select":
        return qt.confirm(f"You selected {whatever}. Confirm?").ask()
    elif type == "addCourse":
        return qt.confirm("Add the following course?").ask()
    
def verifyLength(text,maxLength):
    if text != "" and len(text) <= maxLength:
        return confirm("write",text)

# DATABASE PROMPTS

def dbError():
    qt.print("There was an internal database error, please try again later.",style="bold red")
    qt.press_any_key_to_continue().ask()

# COURSE PROMPTS

def dbCourseExists():
    qt.print("Course already exists in this semester",style="bold red")
    qt.press_any_key_to_continue().ask()
def dbNoCourses():
    qt.print("No courses on this semester",style="bold red")
    qt.press_any_key_to_continue().ask()
def dbAddCourseSuccess():
    qt.print("Course added succesfully",style="bold green")
    qt.press_any_key_to_continue().ask()

# EXAM PROMPTS

def dbNoExams():
    qt.print("No exams on this course",style="bold red")
    qt.press_any_key_to_continue().ask()

# QUESTIONARY PROMPTS

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
        if verifyLength(courseCode,10):
            return courseCode
        else:
            qt.print("Write a valid option\n(Not empty and 10 characters max)",style="bold red")

def courseName():
    while True:
        courseName = (qt.text("Type the course name").ask()).upper()
        if verifyLength(courseName,80):
            return courseName
        else:
            print("Write a valid option\n(Not empty and 80 characters max)",style="bold red")

def selectCourse(courses):
    courseList = [course[2] for course in courses]
    selectedCourse = qt.select(
        "Select the course",
        choices=courseList
    ).ask()
    courseIndex = courseList.index(selectedCourse)
    return courses[courseIndex]


# TABLES

def printCourseTable(courses):
    # Gets the table ready
    table = Table(show_lines=True)
    table.add_column("Code", justify="center", style="cyan")
    table.add_column("Name", justify="left", style="magenta")
    table.add_column("Semester", justify="center", style="yellow")
    for _,courseCode,courseName,courseSemester in courses:
        table.add_row(courseCode,courseName,courseSemester)
    # Prints the table
    console = Console();
    console.print(table)

def printExamTable(exams):
    # Gets the table ready
    table = Table(show_lines=True)
    table.add_column("Type", style="green")
    table.add_column("Date", style="magenta")
    table.add_column("Content", style="yellow")
    for _,_,examType,examDate,examContent in exams:
        table.add_row(examType,examDate,examContent)
    # Prints the table
    console = Console();
    console.print(table)