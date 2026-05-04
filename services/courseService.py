import utils.prompts as prompts
from typing import Literal

def getCourse(semester,cursor,column: Literal["*","id","courseCode","courseName"] = "*"):
    query = f"SELECT {column} FROM course WHERE semester = ?"
    cursor.execute(query,(semester,))
    result = cursor.fetchall()
    if column == "*":
        return [list(course) for course in result]
    else:
        return [course[0] for course in result]

def verifyCourse(semester,course,cursor):
    courses = getCourse(semester,cursor,"courseCode")
    if course in courses:
        prompts.dbCourseExists()
        return False
    else:
        return True

def addCourse(courseSemester,courseCode,courseName,cursor,conn):
    codes = getCourse(courseSemester,cursor,"courseCode")
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