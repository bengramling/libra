
from GradeDistParse import *
from _collections import OrderedDict

#testcase
class TestStudent:
    def __init__(self, numSemesters, courseAndPreReqs, classesTaken, frontLoad, nextTerm):
        self.numSemesters = numSemesters #number of semesters left
        self.courseAndPreReqs = courseAndPreReqs #dictionary of courses left to take. Key = course, Value = prereqs
        self.classesTaken = classesTaken #classes already taken
        self.frontLoad = frontLoad #balance, frontload, or backload
        self.nextTerm = nextTerm #next term of enrollment (fall or spring)

classesNeeded = {}

classesNeeded["MATH-M471"] = [None]
classesNeeded["CSCI-B351"] = ["CSCI-C343"]
classesNeeded["CSCI-B455"] = ["MATH-M212"]
classesNeeded["CSCI-B365"] = [None]
classesNeeded["STAT-S450"] = ["STAT-S350", "MATH-M212"]
classesNeeded["STAT-S350"] = ["MATH-M212"]
classesNeeded["BUS-K201"] = [None]
classesNeeded["BUS-K304"] = ["BUS-K201"]
classesNeeded["BUS-C106"] = [None]
classesNeeded["BUS-C204"] = ["BUS-C106"]
classesNeeded["BUS-T175"] = [None]
classesNeeded["BUS-T275"] = ["BUS-T175"]
classesNeeded["BUS-T375"] = ["BUS-T275"]
classesNeeded["BUS-D270"] = [None]
classesNeeded["BUS-D271"] = ["BUS-D270","BUS-L201"]
classesNeeded["BUS-G202"] = [None]
classesNeeded["MATH-M118"] = [None]
classesNeeded["MATH-M211"] = [None]
classesNeeded["BUS-A100"] = [None]
classesNeeded["BUS-A201"] = ["BUS-A100"]
classesNeeded["BUS-A202"] = ["BUS-A100"]
classesNeeded["BUS-L201"] = [None]


classesTakenTest = ["CSCI-C241", "CSCI-C212", "CSCI-C343", "CSCI-C200", "MATH-M212"]

testUser = TestStudent(numSemesters=5,
                       courseAndPreReqs=classesNeeded,
                       classesTaken=classesTakenTest,
                       frontLoad=True,
                       nextTerm="fall")
#***************************************************************************

#Make the list of all the courses that the student needs to take
def makeCourseList(courseAndPreReqs):
    coursedict = {}
    for section in courseAndPreReqs:
        if fall19.courses.get(section) is not None:
            offeredInFall = True
        else:
            #print(section, "is not offered in the fall")
            offeredInFall = False
        if spring19.courses.get(section) is not None:
            offeredInSpring = True
        else:
            #print(section, "is not offered in the spring")
            offeredInSpring = False
        if not offeredInFall and not offeredInSpring:
            raise Exception("One of the courses you supplied:", section, "is not available in our database in either fall or spring")
        elif offeredInFall:
            AGC = fall19.courses.get(section).adjustedCourseGPA
        elif offeredInSpring:
            AGC = spring19.courses.get(section).adjustedCourseGPA
        coursedict[section] = [courseAndPreReqs[section], offeredInSpring, offeredInFall, AGC]
    courses = OrderedDict(coursedict.items())
    return courses
    #COURSES: An dictionary of courses where the key is the course ID and the value is a list with 4 indexes:
        #Index 0: A list of the prerequisites for this course
        #Index 1: A boolean value for whether the course is offered in the spring
        #Index 2: A boolean value for whether the course is offered in the fall
        #Index 3: The AGC value for the course

#create the semesters thtat the student plans on enrolling in
def createSemesters(numSemesters, nextTerm, classesTaken):
    semesters = {}
    semesters["SEM 0"] = {}
    for course in classesTaken:
        semesters["SEM 0"][course] = []
    for i in range(numSemesters):
        semNum = i+1
        if (nextTerm.lower() == "fall" and semNum % 2 != 0):
            semesters["fall " + str(semNum)] = {}
            continue
        elif(nextTerm.lower() == "spring" and semNum % 2 == 0):
            semesters["fall "+str(semNum)] = {}
            continue
        elif (nextTerm.lower() == "fall" and semNum % 2 == 0):
            semesters["spring " + str(semNum)] = {}
            continue
        elif(nextTerm.lower() == "spring" and semNum % 2 != 0):
            semesters["spring "+str(semNum)] = {}
            continue
        else:
            raise Exception("Error: it appears you have entered an enrollment semester that is not 'spring' or 'fall'")
    sems = OrderedDict(semesters)
    return sems

#get the next semester to enroll a course in
def getLowestSemesterScore(semesters):
    lowestScore = 99999
    #print(semesters)
    for semester in semesters:
        if semester != "SEM 0":
            sumAGC = 0
            for course in semesters[semester]:
                sumAGC += semesters.get(semester)[course][3]
            if frontload and int(semester.split()[1]) == 1:
                sumAGC = sumAGC * .75 #AGC for semester 1 is 25% higher!
            if sumAGC <= lowestScore:
                lowestSem = semester
                lowestScore = sumAGC
            #print(sumAGC, semester)
        else: continue
    #print("lowest sem", lowestSem, "sum:", sumAGC)
    return lowestSem

def isValidEnroll(course, semester, semesters):
    #print(course[1])
    #DOES THE COURSE FIT IN A FALL OR SPRING SEMESTER
    fitsSeason = False
    if "fall" in semester:
        if course[1][2]:
            fitsSeason = True
    elif "spring" in semester:
        if course[1][1]:
            fitsSeason = True
            #print(course, "fits the season")
    elif "fall" not in semester and "spring" not in semester:
        raise Exception("Error: Semester not valid")

    #DOES THE COURSE HAVE PREREQUISITES SATISFIED
    previousSemesters = {}
    semNum = 0
    for sem in semesters:
        if sem.split()[1].isdigit():
            semNum = int(sem.split()[1])
        if semNum < int(semester.split()[1]):
            previousSemesters[sem] = semesters.get(sem)

    for prereq in course[1][0]:
        #print(prereq)
        fitsPrereq = False
        for sem in previousSemesters:
            if prereq is None or prereq in semesters.get(sem):
                fitsPrereq = True
        if fitsPrereq == False:
            break
    #print("course:",course,"fits season:",semester,fitsSeason,"fits prereqs:",fitsPrereq)
    if fitsPrereq and fitsSeason:
        return True

###### ALGORITHM HELPER METHODS ######
def solveSchedule():
    #printSemesters(semesters)
    if len(coursesLeft) == 0: return True
    possibleCourses = coursesLeft.copy()
    for i in range(len(possibleCourses)):
        targetSemester = getLowestSemesterScore(semesters)
        course = list(coursesLeft.items())[i]
        #print("checking to see if", course[0], "is a valid enroll in", targetSemester)
        if isValidEnroll(course, targetSemester, semesters):
            semesters[targetSemester][course[0]] = course[1]
            coursesLeft.pop(course[0])
            #print("SUCCESS, enrolling in", course[0])
            result = solveSchedule()
            if result is True: return result
            else:
                #print("backtracking, removing", course[0], "from ", targetSemester)
                coursesLeft[course[0]] = semesters[targetSemester].pop(course[0])
    return False

def getSemAGC(sem):
    sum = 0
    if sem != "SEM 0":
        for course in semesters[sem]:
            sum += semesters[sem][course][3]
    return round(sum,2)

def printSemesters(semesters):
    print("****************************************")
    print("OUTPUT (SEM 0 is all classes taken previously):")
    for sem in semesters:
        print(sem, ":", semesters[sem].keys(), "AGC SCORE:",getSemAGC(sem))

if __name__ == '__main__':
    fall19 = Semester("Grd_Dist_4198.csv") #Creating Semester Object
    spring19 = Semester("Grd_Dist_4192.csv") #Creating Semester Object

    #MANUAL INPUT INTO BACKTRACKING ALGORITHM
    coursesLeft = makeCourseList(testUser.courseAndPreReqs)
    semesters = createSemesters(testUser.numSemesters, testUser.nextTerm, testUser.classesTaken)
    frontload = testUser.frontLoad

    #SOLVE PROGRAM
    solveSchedule()
    printSemesters(semesters)
