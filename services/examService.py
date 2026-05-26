# This file allows the program to interact with the exam table in the DB

import utils.prompts as prompts
from typing import Literal

# Returns exam list in the next format:
# [examID,courseID,examType,examDate,examContent]
def getExams(value, cursor, by: Literal["id", "courseID"] = "id"):
    query = f"SELECT * FROM exam WHERE {by} = ?"
    cursor.execute(query, (value,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoExams()
        return None

    return [list(exam) for exam in result]

def addExam(courseID,examType,examDate,examContent,cursor,conn):
        if prompts.confirm("addExam"):
            query = """
                    INSERT
                    INTO exam
                    (courseID,examType,examDate,examContent,examGrade)
                    values (?,?,?,?,-1)
                    """
            cursor.execute(query, (courseID,examType,examDate,examContent))
            conn.commit()
            prompts.dbAddExamSuccess()

def updateExam(examID,newValue,column: Literal["examType","examDate","examContent","examGrade"],cursor,conn):
    if prompts.confirm("updateValue",newValue):
            if newValue == "Not graded": newValue = -1
            query = f"""
                    UPDATE
                    exam
                    SET {column} = ?
                    WHERE id = ?
                    """
            cursor.execute(query, (newValue,examID))
            conn.commit()
            prompts.dbUpdateExamSuccess()

def deleteExam(examID,cursor,conn):
    if prompts.confirm("deleteExam"):  
        query = "DELETE FROM exam WHERE id = ?"
        cursor.execute(query, (examID,))
        conn.commit()
    prompts.dbDeleteExamSuccess()