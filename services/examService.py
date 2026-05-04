import utils.prompts as prompts

# Returns exam list in the next format:
# [examID,courseID,examType,examDate,examContent]
def getExam(courseID,cursor):
    query = f"SELECT * FROM exam WHERE courseID = ?"
    cursor.execute(query,(courseID,))
    result = cursor.fetchall()
    if not result:
        prompts.dbNoExams()
        return None
    return [list(course) for course in result]

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