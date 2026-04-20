import os
import questionary as qt
from rich.console import Console
from rich.table import Table
from datetime import datetime

def clear(): os.system("clear")

def addCourse(cursor,conn):
    clear()
    qt.print("CONTROL PANEL => ADD COURSE",style="bold white")
    qt.print("To return write [return]",style="bold")

    # ASK FOR THE SEMESTER
    while True:
        semester = qt.select(
            "Select the semester",
            choices=["2026-1",
                     "2026-2",
                     "2027-1",
                     "2027-2",
                     "Return to Control Panel"]
            ).ask()
        if semester == "Return to Control Panel": return
        if qt.confirm(f"You selected {semester}. Confirm?").ask(): break

    # ASK FOR THE COURSE CODE
    while True:
        code = (qt.text("Type the course code (e.g. MAT-021)").ask()).upper()
        if code.lower() == "return": return
        if code and len(code) <= 10:
            if qt.confirm(f"You wrote {code}. Confirm?").ask(): break
        else:
            qt.print("Write a valid option\n(Not empty and 10 characters max)",style="bold red")

    # ASK FOR THE COURSE NAME
    while True:
        name = (qt.text("Type the course name").ask()).upper()
        if name.lower() == "return": return
        if name and len(name) <= 80:
            if qt.confirm(f"You wrote {name}. Confirm?").ask(): break
        else:
            print("Write a valid option\n(Not empty and 80 characters max)",style="bold red")

    # GET THE TABLE READY
    table = Table()
    table.add_column("Code", justify="center", style="cyan")
    table.add_column("Name", justify="center", style="cyan")
    table.add_column("Semester", justify="center", style="cyan")
    table.add_row(code,name,semester)

    # PRINT THE TABLE
    console = Console(); console.print(table)

    if qt.confirm("Add the following course?").ask():
        cursor.execute("INSERT INTO course (courseCode,courseName,semester) VALUES (?,?,?)", (code,name,semester))
        conn.commit()
    else:
        return

def listCourses(cursor):
    clear()
    qt.print("CONTROL PANEL => LIST COURSES",style="bold white")

    # ASK FOR SEMESTER
    semester = qt.select(
        "Select the semester",
        choices=["2026-1",
                    "2026-2",
                    "2027-1",
                    "2027-2",
                    "Return to Control Panel"]
        ).ask()
    if semester == "Return to Control Panel": return

    # SEARCH SEMESTER IN DB
    cursor.execute("SELECT * FROM course WHERE semester = ?", (semester,))
    results = cursor.fetchall()
    if not results:
        qt.print("No courses on this semester", style="red")
        qt.press_any_key_to_continue().ask()
        return
    
    # GET THE TABLE READY
    table = Table(title=semester)
    table.add_column("ID", style="cyan")
    table.add_column("Code", style="magenta")
    table.add_column("Name", style="green")
    for id,code,name,_ in results:
        table.add_row(str(id),code,name)

    # PRINT THE TABLE
    console = Console(); console.print(table)

    # ASK FOR EXAM LISTING
    if qt.confirm("Do you want to list exams?").ask():
        clear()
        qt.print("CONTROL PANEL => LIST COURSES => LIST EXAMS",style="bold white")

        # TAKES THE COURSES NAMES SO THE USER CAN PICK ONE TO LIST THE EXAMS
        courses = list(course[1] for course in results)
        courses.append("Return to Control Panel")
        course = qt.select(
            "Select the course",
            choices=courses
        ).ask()
        if course == "Return to Control Panel": return

        # SEARCH FOR THE COURSE IN DB
        courseID = results[courses.index(course)][0]
        cursor.execute("SELECT * FROM exam WHERE courseID = ?",(courseID,))
        exams = cursor.fetchall()
        if not exams:
            qt.print("No exams on this course", style="red")
            qt.press_any_key_to_continue().ask()
            return

        # GET THE TABLE READY
        table = Table(title=f"{course} exams")
        table.add_column("Exam ID", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Content", style="yellow")
        for examID,_,examType,examDate,examContent in exams:
            table.add_row(str(examID),examType,examDate,examContent)

        # PRINT THE TABLE
        console = Console(); console.print(table)

        qt.press_any_key_to_continue().ask()
    return

def addExam(cursor,conn):
    clear()
    qt.print("CONTROL PANEL => ADD EXAM",style="bold white")

    # ASK FOR SEMESTER
    semester = qt.select(
        "Select the semester",
        choices=["2026-1",
                 "2026-2",
                 "2027-1",
                 "2027-2",
                 "Return to Control Panel"]
        ).ask()
    if semester == "Return to Control Panel": return

    # GET ALL THE COURSES FROM THE DB
    cursor.execute("SELECT courseCode FROM course WHERE semester = ?", (semester,))
    courses = [course[0] for course in cursor.fetchall()]
    if not courses:
        qt.print("No courses on this semester", style="red")
        qt.press_any_key_to_continue().ask()
        return
    courses.append("Return to Control Panel")

    # ASK FOR A COURSE
    course = qt.select(
        "Select the course",
        choices=courses
    ).ask()
    if course == "Return to Control Panel": return
    cursor.execute("SELECT id FROM course WHERE courseCode = ?", (course,))
    courseID = (cursor.fetchone())[0]

    # ASK FOR EXAM TYPE
    type = qt.select(
        "Select the type of exam",
        choices=["Certamen",
                 "Control",
                 "Tarea",
                 "Quiz",
                 "Return to Control Panel"]
    ).ask()
    if type == "Return to Control Panel": return

    # ASK FOR EXAM DATE
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
            date = f"{year}-{monthNumber}-{day}"
            longerDate = f"{year}-{month[:3]}-{day}"
            date = datetime.strptime(date, "%Y-%m-%d")
            break
        except:
            qt.print("Not a valid day", style="red")
    
    # ASK FOR EXAM CONTENT
    while True:
        content = qt.text("Write the contents or a description of the exam (500 characters max.)\n").ask() or "No content"
        if len(content) <= 500: break
        else: qt.print("Text is more longer than 500 characters",style="red")
    
    #GET THE TABLE READY
    table = Table()
    table.add_column("Course", justify="center", style="cyan")
    table.add_column("Type", justify="center", style="cyan")
    table.add_column("Date", justify="center", style="cyan")
    table.add_column("Content", justify="center", style="cyan")
    table.add_row(course,type,longerDate,content)

    # PRINT TABLE
    console = Console(); console.print(table)

    if qt.confirm("Add the following exam?").ask():
        cursor.execute("INSERT INTO exam (courseID,examType,examDate,examContent) VALUES (?,?,?,?)", (courseID,type,date,content))
        conn.commit()
    else:
        return

def manageCourses(cursor,conn):
    while True:
        clear()
        qt.print("CONTROL PANEL => MANAGE COURSES",style="bold white")

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
                qt.print("CONTROL PANEL => MANAGE COURSES => MODIFY COURSE",style="bold white")

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
                qt.print("CONTROL PANEL => MANAGE COURSES => MODIFY EXAMS",style="bold white")
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
                    qt.print("CONTROL PANEL => MANAGE COURSES => MODIFY EXAMS",style="bold white")

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
                        choices=["Type","Date","Content","Return to Manage Courses"]
                    ).ask()
                    if valueToModify == "Return to Manage Courses": break
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
                    elif valueToModify == "Content":
                        while True:
                            newContent = qt.text("Write the contents or a description of the exam (500 characters max.)\n").ask() or "No content"
                            if len(newContent) <= 500:
                                cursor.execute("UPDATE exam SET examContent = ? WHERE id = ?",(newContent,examID))
                                conn.commit()
                                break
                            else: qt.print("Text is more longer than 500 characters",style="red")

def modifyMenu(cursor, conn):
    while True:
        clear()
        qt.print("CONTROL PANEL",style="bold white")
        answer = qt.select(
            "Select an option!",
            choices=["Add new Course",
                     "List Courses",
                     "Add new Exam",
                     "Manage Courses/Exams",
                     "Exit"]
            ).ask()
        clear()
        if answer == "Add new Course":          addCourse(cursor,conn)
        elif answer == "List Courses":          listCourses(cursor)
        elif answer == "Add new Exam":          addExam(cursor,conn)
        elif answer == "Manage Courses/Exams":  manageCourses(cursor,conn)
        elif answer == "Exit":                  return
        else:                                   input("Try again please")