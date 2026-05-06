# This file should not work with any cursor or DB connection
# Only prompts or verification functions that doesn't need to touch DB

import questionary as qt
import calendar
from rich.console import Console
from datetime import datetime
from rich.table import Table
from typing import Literal

def pressAnyKey():
    qt.press_any_key_to_continue().ask()

# VERIFICATION PROMPTS

def confirm(type: Literal["write","select","addCourse","addExam","updateValue","exit"],whatever = None):
    if type == "write":
        return qt.confirm(f"You wrote {whatever}. Confirm?").ask()
    elif type == "select":
        return qt.confirm(f"You selected {whatever}. Confirm?").ask()
    elif type == "addCourse":
        return qt.confirm("Add the following course?").ask()
    elif type == "addExam":
        return qt.confirm("Add the following exam?").ask()
    elif type == "updateValue":
        return qt.confirm(f"Update value to {whatever}?").ask()
    elif type == "exit":
        return qt.confirm(f"Do you want to exit?").ask()
    
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
    qt.print("No courses found",style="bold red")
    qt.press_any_key_to_continue().ask()
def dbAddCourseSuccess():
    qt.print("Course added succesfully",style="bold green")
    qt.press_any_key_to_continue().ask()
def dbAddExamSuccess():
    qt.print("Exam added succesfully",style="bold green")
    qt.press_any_key_to_continue().ask()
def dbUpdateCourseSuccess():
    qt.print("Course updated succesfully",style="bold green")
    qt.press_any_key_to_continue().ask()
def dbUpdateExamSuccess():
    qt.print("Exam updated succesfully",style="bold green")
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
            qt.print("Write a valid option\n(Not empty and 80 characters max)",style="bold red")

def selectCourse(courses):
    courseList = [course[2] for course in courses]
    selectedCourse = qt.select(
        "Select the course",
        choices=courseList
    ).ask()
    courseIndex = courseList.index(selectedCourse)
    return courses[courseIndex]

def selectExam(exams):
    examList = [f"{exam[2]} | {exam[3]}" for exam in exams]
    selectedExam = qt.select(
        "Select the exam",
        choices=examList
    ).ask()
    examIndex = examList.index(selectedExam)
    return exams[examIndex]

def examType():
    while True:
        examType = qt.select(
            "Select the type of exam",
            choices=["Midterm",
                    "Test",
                    "Homework"]
        ).ask()
        if confirm("select",examType):
            return examType

def examDate(semester):
    examYear = int(semester.split("-")[0])
    months = list(calendar.month_name)[1:]
    month = qt.select(
        "Select the month",
        choices=months
    ).ask()
    examMonth = months.index(month) + 1

    while True:
        examDay = qt.text("Enter a valid day for the month").ask()
        
        if not examDay.isdigit():
            qt.print("Day must be a number", style="red")
            continue
        examDay = int(examDay)

        try:
            date = datetime(examYear,examMonth,examDay)
            examDate = date.strftime("%Y-%b-%d")  # e.g. 2026-May-04
            return examDate
        except:
            qt.print("Not a valid day for that month", style="red")

def examContent():
    while True:
        examContent = qt.text("Write the contents or a description of the exam (500 characters max.)\n").ask() or "No content"
        if verifyLength(examContent,500):
            return examContent
        else:
            qt.print("Text is more longer than 500 characters",style="red")

def courseOption():
    modifyCourse = qt.select(
                    "Select the value you want to modify",
                    choices=["Course Code","Course Name","Course Exams","Return"]
                ).ask()
    return modifyCourse

def examOption():
    modifyExam = qt.select(
                    "Select the value you want to modify",
                    choices=["Exam Type","Exam Date","Exam Content","Return"]
                ).ask()
    return modifyExam

def controlPanelOptions():
    option = qt.select(
            "Select an option!",
            choices=["Add new Course",
                     "List Courses",
                     "Add new Exam",
                     "Manage Courses/Exams",
                     "Return to main menu"]
    ).ask()
    return option

def mainMenuOptions():
    option = qt.select(
        "Select an option!",
        choices=["Dashboard",
                "Control Panel",
                "Exit"]
    ).ask()
    return option

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

def printUpcomingExams(upcomingExams):
    # Gets the table ready
    table = Table(title="Exams in the next 14 days")
    table.add_column("Course name", style="bold cyan")
    table.add_column("Exam type",   style="red")
    table.add_column("Exam date",   style="bold magenta")
    table.add_column("Days left",   style="bold yellow")
    table.add_column("Exam content",style="green")
    for _,courseName,examType,examDate,examContent,daysLeft, in upcomingExams:
        if daysLeft == 0: daysLeft = "Today"
        elif daysLeft == 1: daysLeft = "Tomorrow"
        else: daysLeft = f"{daysLeft} days left"
        table.add_row(courseName,examType,examDate,daysLeft,str(examContent))
    
    # Prints the table
    console = Console();
    console.print(table)
