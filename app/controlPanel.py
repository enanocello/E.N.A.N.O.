# This file makes the control panel functional
# In this menu the users can manage their courses and exams

import services.courseService as courseService
import services.examService as examService
import utils.prompts as prompts
import utils.titles as titles
import questionary as qt

def addCourse(cursor,conn):
    titles.controlPanelTitle("=> ADD COURSE")

    # Asks for the course values
    courseSemester = prompts.courseSemester()
    courseCode = prompts.courseCode()
    courseName = prompts.courseName()

    # Shows the table with the new course
    prompts.printCourseTable([[None,courseSemester,courseCode,courseName],])

    # Adds the course
    courseService.addCourse(courseSemester,courseCode,courseName,cursor,conn)

def listCourses(cursor):
    titles.controlPanelTitle("=> LIST COURSES")

    # Asks for semester
    semester = prompts.courseSemester()

    # Search for courses in the semester
    courses = courseService.getCourseBySemester(semester,cursor)
    if not courses: return
    
    # Shows the table with all the courses
    prompts.printCourseTable(courses)

    # Asks for exam listing
    if qt.confirm("Do you want to list exams?").ask():
        titles.controlPanelTitle("=> LIST COURSES => LIST EXAMS")
        
        # Asks for the course to get the ID
        selectedCourse = prompts.selectCourse(courses)
        courseID = selectedCourse[0]

        # Gets all the exams of the selected course
        exams = examService.getExamByCourse(courseID,cursor)
        if not exams: return
        # Prints the table with all the exams
        prompts.printExamTable(exams)
        prompts.pressAnyKey()

def addExam(cursor,conn):
    titles.controlPanelTitle("=> ADD EXAM")

    # Asks for the semester
    semester = prompts.courseSemester()

    # Search for courses in the semester
    courses = courseService.getCourseBySemester(semester,cursor)
    if not courses: return

    # Asks for the course to get the ID
    selectedCourse = prompts.selectCourse(courses)
    courseID = selectedCourse[0]

    # Asks for exam values
    examType = prompts.examType()
    examDate = prompts.examDate(semester)
    examContent = prompts.examContent()

    # Prints the table
    prompts.printExamTable([[None,None,examType,examDate,examContent]])

    # Adds the exam
    examService.addExam(courseID,examType,examDate,examContent,cursor,conn)


def manageCourses(cursor,conn):
    while True:
        titles.controlPanelTitle("=> MANAGE COURSES")

        # Asks for the semester
        semester = prompts.courseSemester()

        # Search for courses in the semester
        courses = courseService.getCourseBySemester(semester,cursor)
        if not courses: return

        # Asks for the course to get the ID
        selectedCourse = prompts.selectCourse(courses)
        courseID = selectedCourse[0]

        while True:
            titles.controlPanelTitle(f"=> MANAGE COURSES => SELECTED COURSE")
            
            # Gets the course in each iteration to keep the info updated
            selectedCourse = courseService.getCourseByID(courseID,cursor,"*")
            prompts.printCourseTable(selectedCourse)
            
            # Select the value to modify and asks for the new value
            courseOption = prompts.courseOption()
            if courseOption == "Return": return
            elif courseOption == "Course Code":
                newCourseCode = prompts.courseCode()
                courseService.updateCourse(courseID,semester,newCourseCode,"courseCode",cursor,conn)
            elif courseOption == "Course Name":
                newCourseName = prompts.courseName()
                courseService.updateCourse(courseID,semester,newCourseName,"courseName",cursor,conn)
            elif courseOption == "Course Exams":
                exams = examService.getExamByCourse(courseID,cursor)
                if not exams: return
                selectedExam = prompts.selectExam(exams)
                examID = selectedExam[0]
                
                while True:
                    titles.controlPanelTitle("=> MANAGE COURSES => SELECTED COURSE => MANAGE EXAMS")
                    
                    # Prints the course table to remind the selected course
                    prompts.printCourseTable(selectedCourse)
                    
                    # Gets the exam in each iteration to keep the info updated
                    selectedExam = examService.getExamByID(examID,cursor)
                    prompts.printExamTable(selectedExam)

                    # Select the value to modify and asks for the new value
                    examOption = prompts.examOption()
                    if examOption == "Return": break
                    elif examOption == "Exam Type":
                        newExamType = prompts.examType()
                        examService.updateExam(examID,newExamType,"examType",cursor,conn)
                    elif examOption == "Exam Date":
                        newExamDate = prompts.examDate(semester)
                        examService.updateExam(examID,newExamDate,"examDate",cursor,conn)
                    elif examOption == "Exam Content":
                        newExamContent = prompts.examContent()
                        examService.updateExam(examID,newExamContent,"examContent",cursor,conn)

def controlPanel(cursor, conn):
    while True:
        titles.controlPanelTitle()
        option = prompts.controlPanelOptions()
        if option == "Add new Course":          addCourse(cursor,conn)
        elif option == "List Courses":          listCourses(cursor)
        elif option == "Add new Exam":          addExam(cursor,conn)
        elif option == "Manage Courses/Exams":  manageCourses(cursor,conn)
        elif option == "Return to main menu":   return