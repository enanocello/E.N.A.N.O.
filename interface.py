import sqlite3
import os

def courseSemester():
    #ASK FOR THE SEMESTER
    print("STEP 1\nLets take the semester of your course")
    try:
        flag = True
        while flag:
            #Ask for year (Doesn't care which year lol)
            year = int(input("Which year? => "))
            print(f"{year} cool year bro")

            if 0 <= year <= 9999:
                flag = False
            else:
                os.system("clear")
                print(f"Tf you mean {year} lol")

        flag = True
        os.system("clear")
        while flag:
            #Ask for a valid semester
            semester = int(input("Which semester? (1 | 2) => "))
            if semester in (1,2):
                flag = False
            else:
                os.system("clear")
                print("I said 1 or 2 idiot")
                
    except:
        #Handle error
        os.system("clear")
        print("Dude I'm asking for numbers lol")
        courseSemester()
        exit()

    os.system("clear")
    while True:
        print(f"You choose {year}-{semester}\nIs it correct? (y | n)\nType (e) for exit")
        answer = input("=> ").lower()
        if answer in ("y",""):
            return(f"{year}-{semester}")
        elif answer == "n":
            semester = courseSemester()
            return(f"{semester}")
        elif answer in ("e","exit"):
            return None
        else:
            os.system("clear")
            print(f"Wtf is {answer}???")

def courseCode():
    #ASK FOR THE COURSE CODE
    os.system("clear")
    print("STEP 2\nLets take the course code")
    code = str(input("For example IWI-131 => ")).upper()
    os.system("clear")
    while True:
        print(f"You choose {code}\nIs it correct? (y | n)\nType (e) for exit")
        answer = str(input("=> ")).lower()
        if answer in ("y",""):
            return(f"{code}")
        elif answer == "n":
            code = courseCode()
            return code
        elif answer in ("e","exit"):
            return None
        else:
            os.system("clear")
            print(f"Wtf is {answer}???")
    return

def courseName():
    #ASK FOR THE COURSE NAME
    os.system("clear")
    print("STEP 3\nLets take the course name")
    name = str(input("=> ")).upper()
    os.system("clear")
    while True:
        print(f"You choose {name}\nIs it correct? (y | n)\nType (e) for exit")
        answer = input("=> ").lower()
        if answer in ("y",""):
            return(f"{name}")
        elif answer == "n":
            name = courseName()
            return name
        elif answer in ("e","exit"):
            return None
        else:
            os.system("clear")
            print(f"Wtf is {answer}???")
    return

def modifyMenu(cursor, conn):
    flag = True
    options = ["course","exam","exit"]
    while flag:
        os.system("clear")
        print("1. Add new Course \n2. Add new Exam \n3. Exit")

        answer = str(input("=> ")).lower()
        if answer == "1": answer = "course"
        elif answer == "2": answer = "exam"
        elif (answer == "3") | (answer == "e"): answer = "exit"

        if answer in options:
            flag = False
        else:
            os.system("clear")
            print("Not valid option, try again")

    os.system("clear")
    if answer == "course":
        newCourseSemester = courseSemester()
        if newCourseSemester == None: modifyMenu(cursor,conn); exit()
        newCourseCode = courseCode()
        if newCourseCode == None: modifyMenu(cursor,conn); exit()
        newCourseName = courseName()
        if newCourseName == None: modifyMenu(); exit()

        os.system("clear")
        print(f"The following course has been added succesfully bro :b\nName: {newCourseName}\nCode: {newCourseCode}\nSemester: {newCourseSemester}")

        flag = False
    elif answer == "exam":
        flag = False
    else:
        flag = False