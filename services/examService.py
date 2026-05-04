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