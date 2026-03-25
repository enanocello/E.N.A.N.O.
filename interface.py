import sqlite3
import os
import questionary

def clear():
    os.system("clear")

def confirm(value, currentFunction):
    while True:
        clear()
        print(f"You choose {value}\nIs it correct? (y | n)\nType (e) for exit")
        answer = input("=> ").lower()
        if answer in ("y",""):
            return value
        elif answer == "n":
            value = currentFunction()
            return(f"{value}")
        elif answer in ("e","exit"):
            return None
        else:
            input(f"Wtf is {answer}???\nPress [enter]")

def courseSemester():
    #ASK FOR THE SEMESTER
    clear()
    print("STEP 1\nLets take the semester of your course")
    try:
        flag = True
        while flag:
            #Ask for year (Doesn't care which year lol)
            clear()
            year = int(input("Which year? => "))
            print(f"{year} cool year bro")

            if 0 <= year <= 9999:
                flag = False
            else:
                input(f"Tf you mean {year} lol (enter)")

        flag = True
        while flag:
            #Ask for a valid semester
            clear()
            semester = int(input("Which semester? (1 | 2) => "))
            if semester in (1,2):
                flag = False
            else:
                input("I said 1 or 2 idiot")
                
    except:
        #Handle error
        input("Dude I'm asking for numbers lol (enter)")
        return courseSemester()

    clear()
    finalSemester = f"{year}-{semester}"
    return confirm(finalSemester,courseSemester)

def courseCode():
    #ASK FOR THE COURSE CODE
    clear()
    print("STEP 2\nLets take the course code")
    code = str(input("For example IWI-131 => ")).upper()
    return confirm(code,courseCode)

def courseName():
    #ASK FOR THE COURSE NAME
    clear()
    print("STEP 3\nLets take the course name")
    name = str(input("=> ")).upper()
    return confirm(name,courseName)

def addCourse(cursor,conn):
    newSemester = courseSemester()
    if newSemester != None:
        newCode = courseCode()
        if newCode != None:
            newName = courseName()
            if newName != None:
                clear()
                cursor.execute("INSERT INTO course (courseCode,courseName,semester) VALUES (?,?,?)", (newCode,newName,newSemester))
                conn.commit()
                input(f"The following course has been added succesfully bro :b\nName: {newName}\nCode: {newCode}\nSemester: {newSemester}\nPress [enter]")

def modifyCourse(cursor,conn):
    while True:
        clear()
        courseID = input("Type the course ID you want to modify\nPress [e] to return\n=>")
        cursor.execute("SELECT * FROM course WHERE id = ?",(courseID,))
        result = cursor.fetchall()
        if result in ("e","exit"):
            return
        if result:
            _,code,name,fullSemester = result[0]
            year,semester = fullSemester.split("-")
            clear();newCode = input(f"Current course code: {code}\nType the new code (Leave empty to skip)\n=>") or code
            clear();newName = input(f"Current course name: {name}\nType the new name (Leave empty to skip)\n=>") or name
            flag = True
            while flag:
                clear();newYear = input(f"Current course year: {year}\nType new year (Leave empty to skip)\n=>") or year
                try:
                    if (0 <= int(newYear) <= 9999): flag = False
                    else: input(f"Tf you mean {newYear} lol\n[enter] to try again")
                except:
                    input("Yo that value is not correct\nExample: 2021\n[enter] to try again")
            flag = True
            while flag:
                clear();newSemester = input(f"Current course semester: {semester}\nType new semester (1 | 2) (Leave empty to skip)\n=>") or semester
                try:
                    if int(newSemester) in (1,2): flag = False
                    else: input("I said 1 or 2 idiot\n[enter] to try again")
                except:
                    input("Yo that value is not correct\nIt's 1 or 2\n[enter] to try again")
            newSemester = f"{newYear}-{newSemester}"

            cursor.execute("UPDATE course SET courseCode = ?, courseName = ?, semester = ? WHERE id = ?",(newCode.upper(),newName.upper(),newSemester,courseID))
            conn.commit()
            clear();input("All done bro, [enter] to exit")
            return

def listCourses(cursor,conn):
    while True:
        clear()
        semester = input("Digit the semester (ex: 2026-1)\nPress [e] to return\n=>")
        cursor.execute("SELECT * FROM course WHERE semester = ?", (semester,))
        results = cursor.fetchall()
        if semester in ("e","exit"):
            return
        if results:
            clear()
            print(f"Results for semester {semester}\nID\tCode\t\tName")
            for id,code,name,_ in results:
                if len(code) >= 8: print(f"{id}\t{code}\t{name}")
                else: print(f"{id}\t{code}\t\t{name}") 
            input("[enter] to continue")
            return semester
        input("There is no courses in that semester bro\n(Press [enter])")

def addExam(cursor,conn):
    while True:
        semester = listCourses(cursor,conn)
        if not semester: return
        print("\nType the course code or course ID where you wanna add an exam")
        examCourse = input("=> ").upper()

        cursor.execute("SELECT * FROM course WHERE (courseCode = ? OR id = ?) AND semester = ?",(examCourse,examCourse,semester))
        exists = cursor.fetchall()

        if exists:
            input(f"Cool i found it :b {exists}")
            return
        else:
            input(f"Yoo I can't find {examCourse} in database ffff")

def modifyMenu(cursor, conn):
    while True:
        clear()
        answer = questionary.select(
            "Select an option!",
            choices=["Add new Course",
                     "Modify Course",
                     "List Courses",
                     "Add new Exam",
                     "Exit"]
            ).ask()

        if answer == "Add new Course":  addCourse(cursor,conn)
        elif answer == "List Courses":  listCourses(cursor,conn)
        elif answer == "Modify Course": modifyCourse(cursor,conn)
        elif answer == "Add new Exam":  addExam(cursor,conn)
        elif answer == "Exit":          return
        else:                           input("Try again please")
