# libra
# Introduction
### What is Libra? ###
Libra is a transcript planning tool. The main purpose of this application is to help students plan out their four years at IU. Libra will tell you exactly how to distribute the classes you need to take in order to graduate. This distribution is based entirely off of the average difficulty of each course, so as to give you the most balanced course load every semester. 
### How Does it Work? ###
Libra is an open source project, anybody can view the code and look at exactly how the project works, but in case you don't have the time to analyze a few pages of python script, here's a brief overview. 
* __Step One: Take User Input.__ This seems like a no-brainer but it is actually an important step to do correctly. Unsanitized inputs are just about the only thing that could cause trouble for the program, so we want to take as few inputs as possible. Here are the inputs:
    * __Credits Already Achieved.__ This info helps the program establish what prerequisites the user has. When assigning future classes, the program checks to ensure that prerequisites have already been met.
    * __Number of Planned Semesters.__ How many future semesters the user plans to enroll in. The program will distribute courses over this many semesters.
    * __Next Semester of Enrollment.__ Whether the user plans to enroll starting in the fall or spring. Some courses are only available in one of the two seasons, so this information is important.
    * __Frontload?__ Frontloading is when the program makes the first semester of enrollment a little more difficult than subsequent semesters, so as to lighten the load later on.
    * __Future Courses.__ These are the courses that will be distributed among the list of semesters.
* __Step Two: Assign Courses to Semesters.__ This is where the backtracking algorithm is used to assign courses to semesters greedily based on course difficulty and cumulative semester difficulty. The difficulty is assigned based on my heuristic as outlined below. More detail on the backtracking algorithm is discussed below as well.
* __Step Three: Present Information to the User.__ The most self-explanatory step, the finished plan is presented to the user.

# The Backtracking Algorithm.
### Algorithm Overview ###
This is the meat of the project, the backtracking algorithm is what assigns courses to each semester, and it does so in the steps outlined below.
* __Step One: Identify the Semester to Enroll In.__ The algorithm first looks at all of the available semesters and finds the semester with the lowest cumulative difficulty score.
* __Step Two: Identify the Course to Place.__ The algorithm then goes through the list of possible courses to place in that semester, it recursively tries every unassigned course until it finds a course that fits all of the constraints outlined below:
  * __1.__ A course cannot be placed in a semester where the course is not offered. i.e. a course only offered in fall cannot be assigned to a spring semester.
  * __2.__ A course cannot be placed in a semester if the prerequisites were not satisfied in previous semesters. i.e. if MATH-101 requires MATH-100, MATH-100 must be completed _before_ MATH-101 is scheduled.
* __Step Three: Place the Course.__ This involves updating the list of assigned courses as well as the list of semesters and list of unassigned courses.
* __Step Four: Repeat.__ Repeat steps 1-3 until a schedule is fully built and there are no more courses to assign, or return an error if a schedule cannot be created with the given information.
### Fail Scenarios ###
There are a few reasons the algorithm could be unable to create a schedule based on user input, if this happens, the algorithm may throw a run-time error, or it may not run at all. These scenarios are listed below:
* __Too Few Semesters__ Because certain courses have prerequisites, there is a lower limit on how many semesters a user must take. The number of semesters required is equal to the highest degree course that a user must take. The "degree" of a course is directly related to the number of semesters of enrollment required to get credit for the course. A first degree course, or "primary" course has no prerequisites, a second degree course has one or more prerequisites that can all be completed in the same semester, a third degree course has one or more prerequisites that also have a prerequisite, etc.
* __Incompatible Courses__ The semesters the user requested do not fit the constraints of the courses that the user listed. i.e. a user wants to build a schedule for Fall 2020 but he has courses that require a spring semester.

# The Heuristic (Defining a Difficulty Value)
### Problems With Course Difficulty Rankings ###
To calculate how difficult a course is, I have developed a ranking system which is somewhat analogous to the inverse of the GPA system. 4 is the most difficult course, and 0 is the easiest course. 
The easiest ranking system in this case would be to just take the average GPA for the course and subtract it from 4, however this poses two issues. __1.__ There are few to no courses at IU with a 100 percent fail rate. This ranking system would be somewhat biased, as the ranking of difficulties is not normally distributed. __2.__ We also need to account for the fact that classes with smarter students tend to have higher average course GPAs.
### My Solution to Ranking Course Difficulty ###
__To Solve the First Problem,__ I needed to assume that the distribution of average course GPAs per semester is normal around the mean course GPA. This is an assumption I can make because the data in question is a distribution of means. Although the individual GPAs may not be normally distributed within each course, and the courses aren't exactly "random samples," I can take a few liberties to make the calculations easier. After making my assumption, I can rank the course difficulty based on its distance from the mean. -2 Standard deviations means the course has a difficulty of 4, +2 Standard Deviations means it has a difficulty of 0, and the same applies for all numbers in between. __The Second Problem was Much Easier to Solve,__ All I had to do was take the average student GPA for each course at IU, and then scale the associated course GPA based on the average student GPA for IU as a whole. Essentially saying "What would this course GPA be if the class was filled with average students?" In summary, to get the difficulty score for a course, we first scale the course to the average student, then we place it on a normal distribution around a mean of 2, and floor any values above 2 standard deviations away from the mean in order to eliminate outliers and make the scale more legible.
