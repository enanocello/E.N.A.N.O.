def getUpcomingExams(cursor):
    cursor.execute("""SELECT
                   exam.id,
                   course.courseName,
                   exam.examType,
                   date(examDate) as examDate,
                   exam.examContent,
                   CAST(julianday(DATE(examDate)) - julianday(DATE('now','localtime')) AS INTEGER) AS daysLeft 
                   FROM exam
                   JOIN course ON exam.courseID = course.id 
                   WHERE date(examDate) >= date('now','localtime') 
                   AND date(examDate) <= date('now','localtime','+14 days')
                   ORDER BY examDate
                   """)
    exams = cursor.fetchall()
    return exams