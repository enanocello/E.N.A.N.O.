import app.ascii as ascii
import questionary as qt
import utils.prompts as prompts
import services.courseService as courseService
import services.examService as examService
from rich.table import Table
from datetime import datetime
from rich.console import Console
from utils.terminal import clear

def addCourse(cursor,conn):
    clear()
    qt.print(f"{ascii.controlPanel()}\n=> ADD COURSE",style="bold yellow")

    # Asks for the course values
    courseSemester = prompts.courseSemester()
    courseCode = prompts.courseCode()
    courseName = prompts.courseName()

    # Shows the table with the new course
    prompts.printCourseTable([[None,courseSemester,courseCode,courseName],])

    # Adds the course
    courseService.addCourse(courseSemester,courseCode,courseName,cursor,conn)

def listCourses(cursor):
    clear()
    qt.print(f"{ascii.controlPanel()}\n=> LIST COURSES",style="bold yellow")

    # Asks for semester
    semester = prompts.courseSemester()

    # Search for courses in the semester
    courses = courseService.getCourse(semester,cursor)
    if not courses: return
    
    # Shows the table with all the courses
    prompts.printCourseTable(courses)

    # Asks for exam listing
    if qt.confirm("Do you want to list exams?").ask():
        clear()
        qt.print(f"{ascii.controlPanel()}\n=> LIST COURSES => LIST EXAMS",style="bold yellow")
        
        # Asks for the course to get the ID
        selectedCourse = prompts.selectCourse(courses)
        courseID = selectedCourse[0]

        # Gets all the exams of the selected course
        exams = examService.getExam(courseID,cursor)

        # Prints the table with all the exams
        prompts.printExamTable(exams)
        prompts.pressAnyKey()

def addExam(cursor,conn):
    clear()
    qt.print(f"{ascii.controlPanel()}\n=> ADD EXAM",style="bold yellow")

    # Asks for the semester
    semester = prompts.courseSemester()

    # Search for courses in the semester
    courses = courseService.getCourse(semester,cursor)
    if not courses: return

    # Asks for the course to get the ID
    selectedCourse = prompts.selectCourse(courses)
    courseID = selectedCourse[0]

    # Asks for exam values
    examType = prompts.examType()
    examDate = prompts.examDate(semester)
    examContent = prompts.examContent()

    # Prints the table
    prompts.printExamTable([[None,None,examType,examDate,examContent]])

    # Adds the exam
    examService.addExam(courseID,examType,examDate,examContent,cursor,conn)


def manageCourses(cursor,conn):
    while True:
        clear()
        qt.print(f"{ascii.controlPanel()}\n=> MANAGE COURSES",style="bold yellow")

        # ASK FOR THE SEMESTER
        semester = qt.select(
            "Select the semester",
            choices=["2026-1",
                    "2026-2",
                    "2027-1",
                    "2027-2",
                    "Return to Control Panel"]
            ).ask()
        if semester == "Return to Control Panel": return

        # TAKES ONLY THE COURSE CODE TO DISPLAY AS OPTIONS
        cursor.execute("SELECT courseCode FROM course WHERE semester = ?", (semester,))
        courseOptions = [course[0] for course in cursor.fetchall()]
        if not courseOptions:
            qt.print("No courses on this semester", style="red")
            qt.press_any_key_to_continue().ask()
            return
        courseOptions.append("Return to Control Panel")
        selectedCourse = qt.select(
            "Select the course",
            choices=courseOptions
        ).ask()
        if selectedCourse == "Return to Control Panel": return

        # TAKES THE SELECTED COURSE ID
        cursor.execute("SELECT id FROM course WHERE courseCode = ? AND semester = ?", (selectedCourse,semester))
        courseID = cursor.fetchone()[0]
        option = qt.select(
            "What do you want to do?",
            choices=["Modify Course","Modify Exams","Return to Control Panel"]
        ).ask()
        if option == "Return to Control Panel": return
        if option == "Modify Course":
            while True:
                # TAKES ALL DATA ABOUT THE COURSE SELECTED 
                cursor.execute("SELECT * FROM course WHERE id = ?", (courseID,))
                _,actualCode,actualName,_  = cursor.fetchone()
                clear()
                qt.print(f"{ascii.controlPanel()}\n=> MANAGE COURSES => MODIFY COURSE",style="bold yellow")

                # GET THE TABLE READY
                table = Table()
                table.add_column("Code", justify="center", style="cyan")
                table.add_column("Name", justify="center", style="cyan")
                table.add_column("Semester", justify="center", style="cyan")
                table.add_row(actualCode,actualName,semester)

                # PRINT THE TABLE
                console = Console(); console.print(table)
                
                # ASK FOR THE VALUES THE USER WANT TO CHANGE
                valueToModify = qt.select(
                    "Select the value you want to modify",
                    choices=["Course Code","Course Name","Return"]
                ).ask()
                if valueToModify == "Return": break
                elif valueToModify == "Course Code":
                    newCode = (qt.text(f"Type the new course code").ask()).upper()
                    if newCode.lower() == "exit": return
                    if newCode and len(newCode) <= 10:
                        if qt.confirm(f"You wrote {newCode}. Confirm?").ask():
                            cursor.execute("UPDATE course SET courseCode = ? WHERE id = ?",(newCode.upper(),courseID))
                            conn.commit()
                    else:
                        qt.print("Write a valid option\n(Not empty and 10 characters max)",style="bold red")
                elif valueToModify == "Course Name":
                    newName = (qt.text("Type the new course name").ask()).upper()
                    if newName.lower() == "exit": return
                    if newName and len(newName) <= 80:
                        if qt.confirm(f"You wrote {newName}. Confirm?").ask():
                            cursor.execute("UPDATE course SET courseName = ? WHERE id = ?",(newName.upper(),courseID))
                            conn.commit()
                    else:
                        print("Write a valid option\n(Not empty and 80 characters max)",style="bold red")
        if option == "Modify Exams":
            while True:
                # TAKES ALL EXAM DATA ABOUT THE SELECTED COURSE
                cursor.execute("SELECT * FROM exam WHERE courseID = ?", (courseID,))
                exams = cursor.fetchall()
                clear()
                qt.print(f"{ascii.controlPanel()}\n=> MANAGE COURSES => MODIFY EXAMS",style="bold yellow")
                if not exams:
                    print(courseID)
                    qt.print("No exams on this course", style="red")
                    qt.press_any_key_to_continue().ask()
                    break

                # DISPLAY ALL EXAMS AND ASK TO PICK ONE
                examOptions = [f"{option[2]} | {option[3]} | {option[4][:10]}" for option in exams]
                examOptions.append("Return to Manage Courses")
                option = qt.select(
                    f"Select the {selectedCourse} exam",
                    choices = examOptions
                ).ask()
                if option == "Return to Manage Courses": break
                examIndex = examOptions.index(option)
                examID,_,examType,examDate,examContent = exams[examIndex]

                while True:
                    clear()
                    qt.print(f"{ascii.controlPanel()}\n=> MANAGE COURSES => MODIFY EXAMS",style="bold yellow")

                    # TAKES ALL DATA ABOUT THE SELECTED EXAM
                    cursor.execute("SELECT * FROM exam WHERE id = ?", (examID,))
                    exams = cursor.fetchall()
                    _,_,examType,examDate,examContent = exams[0]

                    # GET THE TABLE READY
                    table = Table(title=f"Exam on {selectedCourse}")
                    table.add_column("Exam ID", style="cyan")
                    table.add_column("Type", style="magenta")
                    table.add_column("Date", style="green")
                    table.add_column("Content", style="yellow")
                    table.add_row(str(examID),examType,examDate,examContent)
                    console = Console(); console.print(table)

                    # ASK FOR THE VALUE TO MODIFY
                    valueToModify = qt.select(
                        "Select the value you want to modify",
                        choices=["Type",
                                 "Date",
                                 "Content",
                                 "Return to Manage Courses"]
                        ).ask()
                    if valueToModify == "Return to Manage Courses": break

                    # IF TYPE WAS SELECTED
                    elif valueToModify == "Type":
                        newType = qt.select(
                            "Select the type of exam",
                            choices=["Certamen",
                                    "Control",
                                    "Tarea",
                                    "Quiz",
                                    "Return"]
                        ).ask()
                        if newType == "Return": break
                        cursor.execute("UPDATE exam SET examType = ? WHERE id = ?",(newType,examID))
                        conn.commit()
                    
                    # IF DATE WAS SELECTED
                    elif valueToModify == "Date":
                        year = (semester.split("-"))[0]

                        months = ["January","February","March",
                                "April","May","June",
                                "Jule","August","September",
                                "October","November","December"]
                        month = qt.select("Select the month",choices=months).ask()
                        monthNumber = months.index(month)+1

                        while True:
                            day = qt.text("Enter a valid day for the month").ask()
                            try:
                                newDate = f"{year}-{monthNumber}-{day}"
                                print(newDate)
                                datetime.strptime(newDate, "%Y-%m-%d")
                                cursor.execute("UPDATE exam SET examDate = ? WHERE id = ?",(newDate,examID))
                                conn.commit()
                                break
                            except:
                                qt.print("Not a valid day", style="red")
                    
                    # IF CONTENT WAS SELECTED
                    elif valueToModify == "Content":
                        while True:
                            newContent = qt.text("Write the contents or a description of the exam (500 characters max.)\n").ask() or "No content"
                            if len(newContent) <= 500:
                                cursor.execute("UPDATE exam SET examContent = ? WHERE id = ?",(newContent,examID))
                                conn.commit()
                                break
                            else: qt.print("Text is more longer than 500 characters",style="red")

def controlPanel(cursor, conn):
    while True:
        clear()
        qt.print(ascii.controlPanel(),style="bold yellow")
        answer = qt.select(
            "Select an option!",
            choices=["Add new Course",
                     "List Courses",
                     "Add new Exam",
                     "Manage Courses/Exams",
                     "Return to main menu"]
            ).ask()
        clear()
        if answer == "Add new Course":          addCourse(cursor,conn)
        elif answer == "List Courses":          listCourses(cursor)
        elif answer == "Add new Exam":          addExam(cursor,conn)
        elif answer == "Manage Courses/Exams":  manageCourses(cursor,conn)
        elif answer == "Return to main menu":   return