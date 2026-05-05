# This file is the only one that will touch the DB

import utils.prompts as prompts
from typing import Literal

# Returns course list bases on column parameter
# If param is * it returns a list with the next format:
# [courseID,courseCode,courseName,semester]
def getCourseBySemester(semester,cursor,column: Literal["*","id","courseCode","courseName"] = "*"):
    query = f"SELECT {column} FROM course WHERE semester = ?"
    cursor.execute(query,(semester,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoCourses()
        return
    if column == "*":
        return [list(course) for course in result]
    else:
        return [course[0] for course in result]

def getCourseByID(courseID,cursor,column: Literal["*","id","courseCode","courseName"] = "*"):
    query = f"SELECT {column} FROM course WHERE id = ?"
    cursor.execute(query,(courseID,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoCourses()
        return None
    if column == "*":
        return [list(course) for course in result]
    else:
        return [course[0] for course in result]

# Returns false is course is already in the DB
def verifyCourse(semester,course,cursor):
    courses = getCourseBySemester(semester,cursor,"courseCode")
    if course in courses:
        prompts.dbCourseExists()
        return False
    else:
        return True

def addCourse(courseSemester,courseCode,courseName,cursor,conn):
    if verifyCourse(courseSemester,courseCode,cursor):
        if prompts.confirm("addCourse"):
            query = """
                    INSERT
                    INTO course
                    (semester,courseCode,courseName)
                    values (?,?,?)
                    """
            cursor.execute(query, (courseSemester,courseCode,courseName))
            conn.commit()
            prompts.dbAddCourseSuccess()

def updateCourse(courseID,courseSemester,newValue,column: Literal["courseCode","courseName"],cursor,conn):
    if column == "courseCode":
        if not verifyCourse(courseSemester,newValue,cursor):
            return
    if prompts.confirm("updateValue",newValue):
            query = f"""
                    UPDATE
                    course
                    SET {column} = ?
                    WHERE id = ?
                    """
            cursor.execute(query, (newValue,courseID))
            conn.commit()
            prompts.dbUpdateCourseSuccess()