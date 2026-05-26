# This file allows the program to interact with the course table in the DB

import utils.prompts as prompts
from typing import Literal

# Returns course list bases on column parameter
# If param is * it returns a list with the next format:
# [courseID,courseCode,courseName,semester]
def getCourses(value, cursor, by: Literal["id", "semester"] = "id", column: Literal["*", "id", "courseCode", "courseName", "courseCredits"] = "*"):
    query = f"SELECT {column} FROM course WHERE {by} = ?"
    cursor.execute(query, (value,))
    result = cursor.fetchall()

    if not result:
        return None
    if column == "*":
        return [list(course) for course in result]
    return [course[0] for course in result]

# Returns false is course is already in the DB
def verifyCourse(semester,course,cursor):
    courses = getCourses(semester,cursor,"semester","courseCode")
    if not courses:
        return True
    if course in courses:
        prompts.dbCourseExists()
        return False
    else:
        return True
    
def courseExists(courseID,cursor):
    courses = getCourses(courseID,cursor,by="id")
    if courses:
        return True
    else:
        return

def addCourse(courseSemester,courseCode,courseName,courseCredits,cursor,conn):
    if verifyCourse(courseSemester,courseCode,cursor):
        if prompts.confirm("addCourse"):
            query = """
                    INSERT
                    INTO course
                    (courseCode,courseName,courseCredits,semester)
                    values (?,?,?,?)
                    """
            cursor.execute(query, (courseCode,courseName,courseCredits,courseSemester))
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

def deleteCourse(courseID,cursor,conn):
    if courseExists(courseID,cursor):
        if prompts.confirm("deleteCourse"):
            query = "DELETE FROM course WHERE id = ?"
            cursor.execute(query, (courseID,))
            conn.commit()
            prompts.dbDeleteCourseSuccess()
    else:
        prompts.dbNoCourses()