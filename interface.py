import sqlite3
import os

def mainMenu(cursor, conn):
    print("1. Add new Course \n2. Add new Exam \n3. Exit")
    flag = True
    while flag:
        answer = str(input("=> ")).lower()
        match answer:
            case "1" | "course":
                print("LOL")
                flag = False
            case "2" | "exam":
                print("LOL")
                flag = False
            case "3" | "exit" | "e":
                print("LOL")
                flag = False
            case _:
                print("notLOL")