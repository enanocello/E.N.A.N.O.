# This file is the only one that will touch the DB

import utils.prompts as prompts
from typing import Literal

# Returns course list bases on column parameter
# If param is * it returns a list with the next format:
# [courseID,courseCode,courseName,semester]
def getCourse(semester,cursor,column: Literal["*","id","courseCode","courseName"] = "*"):
    query = f"SELECT {column} FROM course WHERE semester = ?"
    cursor.execute(query,(semester,))
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
    courses = getCourse(semester,cursor,"courseCode")
    if course in courses:
        prompts.dbCourseExists()
        return False
    else:
        return True

def addCourse(courseSemester,courseCode,courseName,cursor,conn):
    if verifyCourse(courseSemester,courseCode,cursor):
        if prompts.confirm(None,"addCourse"):
            query = """
                    INSERT
                    INTO course
                    (semester,courseCode,courseName)
                    values (?,?,?)
                    """
            cursor.execute(query, (courseSemester,courseCode,courseName))
            conn.commit()
            prompts.dbAddCourseSuccess()