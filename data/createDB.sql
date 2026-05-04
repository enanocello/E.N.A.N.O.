DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS exam;
CREATE TABLE IF NOT EXISTS course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courseCode VARCHAR(10),
    courseName VARCHAR(80),
    semester VARCHAR(8)
);
CREATE TABLE IF NOT EXISTS exam (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courseID INTEGER,
    examType VARCHAR(20),
    examDate DATE,
    examContent VARCHAR(500),

    Foreign Key (courseID) REFERENCES course(id) ON DELETE CASCADE
);