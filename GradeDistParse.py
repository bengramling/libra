#GradeDistParse.py
#Part of B351 Final Project, Schedule Balancer
#authors: Ben Gramling, Pratik Aluri, Zack Chelf
#version: 1.0.0

import csv

def load_data(csvFile):
    with open(csvFile, 'r') as f:
        csv_reader = csv.reader(f)
        line_count = 0
        courseDict = dict()
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            if row[4] == "NR" or row[4] == "0" or row[5] == "NR" or row[5] == "0":
                continue
            newCourse = Course(termCode=row[0], department=row[1],
                               subject=row[2], course=row[3], courseGPA=float(row[4]), studentGPA=float(row[5]))
            courseDict.update({newCourse.courseID : newCourse})
        return courseDict

def calc_agc(courseGPA, studentGPA, meanGPA):
    print(meanGPA)
    weightMultiplier = meanGPA/studentGPA
    agc = min(max(round(weightMultiplier*courseGPA, 2), 0), 4)
    return agc

def calc_mean_GPA(courseDict):
    numCourses = len(courseDict)
    sumGPA = 0
    for course in courseDict.values():
        sumGPA += course.studentGPA
    return round(sumGPA/numCourses, 2)


class Course:
    def __init__(self, termCode, department, subject, course, courseGPA, studentGPA):
        self.termCode = termCode
        self.department = department
        self.subject = subject
        self.course = course
        self.courseGPA = courseGPA
        self.studentGPA = studentGPA
        self.courseID = subject + course
        self.adjustedCourseGPA = courseGPA

class Semester:
    def __init__(self, classCSV):
        self.courses = load_data(classCSV) #Dictionary with format {"BUS-C106" : (course object)}
        self.meanGPA = calc_mean_GPA(self.courses)
        for course in self.courses.values():
            course.adjustedCourseGPA = calc_agc(course.courseGPA, course.studentGPA, self.meanGPA)
