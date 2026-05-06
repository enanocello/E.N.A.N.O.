# This file allows the program to interact with the exam table in the DB

import utils.prompts as prompts
from typing import Literal

# Returns exam list in the next format:
# [examID,courseID,examType,examDate,examContent]
def getExamByCourse(courseID,cursor):
    query = f"SELECT * FROM exam WHERE courseID = ?"
    cursor.execute(query,(courseID,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoExams()
        return
    return [list(exam) for exam in result]

def getExamByID(examID,cursor):
    query = f"SELECT * FROM exam WHERE id = ?"
    cursor.execute(query,(examID,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoExams()
        return
    return [list(exam) for exam in result]

def addExam(courseID,examType,examDate,examContent,cursor,conn):
        if prompts.confirm("addExam"):
            query = """
                    INSERT
                    INTO exam
                    (courseID,examType,examDate,examContent)
                    values (?,?,?,?)
                    """
            cursor.execute(query, (courseID,examType,examDate,examContent))
            conn.commit()
            prompts.dbAddExamSuccess()

def updateExam(examID,newValue,column: Literal["examType","examDate","examContent"],cursor,conn):
    if prompts.confirm("updateValue",newValue):
            query = f"""
                    UPDATE
                    exam
                    SET {column} = ?
                    WHERE id = ?
                    """
            cursor.execute(query, (newValue,examID))
            conn.commit()
            prompts.dbUpdateExamSuccess()