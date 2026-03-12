import sqlite3
import os

def course():
    print("Lets take the period of your course")
    try:
        flag = True
        while flag:
            #Ask for year (Doesn't care which year lol)
            year = int(input("Year: "))
            print(f"{year} cool year bro")

            if 0 <= year <= 9999:
                flag = False
            else:
                os.system("clear")
                print(f"Tf you mean with {year} lol")

        flag = True
        while flag:
            #Ask for a valid semester
            semester = int(input("Semester (1 | 2): "))
            if semester in (1,2):
                flag = False
            else:
                os.system("clear")
                print("I said 1 or 2 idiot")
                
    except:
        #Handle error
        os.system("clear")
        print("Dont valid option dude")

    while True:
        os.system("clear")
        print(f"You choose {year}-{semester}\nIs it correct? (y | n)")
        answer = input()
        if answer == "y":
            return(f"{year}-{semester}")
        elif answer == "n":
            return None
        else:
            print(f"What is {answer}???")
        

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
        newCourse = course()
        if newCourse == None:
            modifyMenu(cursor,conn)
            exit()
        else:
            print(f"The course {newCourse} has been added succesfully compa")
            flag = False
    elif answer == "exam":
        flag = False
    else:
        flag = False