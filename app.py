from dbManager import DBManager
from student import Student
from teacher import Teacher
from classes import Class
from teacherclass import TeacherClass
from lesson import Lesson

from datetime import datetime
import re

class App:
    def __init__(self):
        
        self.db = DBManager()
        self.studentNumbers = []
        self.teacherIds = []
        self.classids = []
        self.lessonids = []
    
    def initApp(self):
        message = "1-Student Menu\n2-Teacher Menu\n3.Class Menu\n4-Lesson Menu\ne-Exit\n"
        while True:
            print("\n")
            print("Main Menu".center(50,"_"))
            print(message)
            choice = input("Choice => ")

            if(choice=="e"):
                self.db.connection.close()
                break

            match(choice):
                case "1":
                    self.studentMenu()
                
                case "2":
                    self.teacherMenu()

                case "3":
                    self.classMenu()
                
                case "4":
                    self.lessonMenu()

                case _:
                    print("Invalid Choice\n")



    #STUDENTS
    def studentMenu(self):
        message = "1-Display Student\n2-Add Student\n3-Edit Student\n4-Delete Student\ne-Exit\n"
        while True:

            print("\n")
            print("Student menu".center(50,"_"))
            print(message)

            choice = input("Choice => ")

            if choice == "e":
                break
                
            match(choice):

                case "1":
                    self.displayStudents()
                    self.studentNumbers = []

                case "2":
                    self.addStudent()

                case "3":
                    self.editStudent()
                
                case "4":
                    self.deleteStudent()

                case _:
                    print("Invalid Choice\n")

    def displayClasses(self):
        classes = self.db.getClasses()
        for c in classes:
            print(f"id: {c.id}   |   name: {c.name}")
            self.classids.append(str(c.id))

        if len(self.classids) == 0:
            print("There is no class!\n")
            return 0
        input("\nPress any key to continue: ")

    def selectClass(self):
        while True:
            if(self.displayClasses()!=0):

                classid = input("\nSelect class id: ")
                if classid == "":
                    continue
                elif self.classids.__contains__(classid):
                    break
                else:
                    print("Invalid class id!\n")
            else:
                classid = "0"
                break

            

        self.classids = []
        return int(classid)

    def displayStudents(self):
        classid = self.selectClass()
        if classid == 0:
            return 0
        studentList = self.db.getStudents(classid)

        if len(studentList) == 0:
            print("There is no student!")
            return 0

        for student in studentList:
            print(f"Number: {student.studentNumber} | Fullname: {student.name} {student.surname} | TC: {student.TC} | Birthdate: {student.birthdate} | Gender: {student.gender}")
            self.studentNumbers.append(student.studentNumber)

        input("\nPress any key to continue: ")
        
    def addStudent(self):
        while True:

            print("\n")
            print("Add Student".center(50,"_"))
            try:

                classid = self.selectClass()
                if classid == 0:
                    break

                name = input("Name: ")
                surname = input("Surname: ")
                studentNo = self.inputStudentNumber(sql="select * from students where StudentNumber = %s")
                TC = self.inputTC(sql="select * from students where TC = %s")
                gender = self.inputGender()
                birthdate = self.inputBirthdate()
                self.checkNameSurname([name,surname])

            except Exception as ex:
                print("Error:",ex)
            else:
                student = Student(None,studentNo,name,surname,TC,birthdate,gender,classid)
                self.db.addStudent(student)
            finally:
                if input("Press any key to continue to add student or press 'e' to exit!\n-> ") =="e":
                    break

    def selectStudentNumberByClassId(self):
        self.displayStudents()
        if len(self.studentNumbers) == 0:
            return 0

        while True:
            try:
                studentNo = int(input("Select student No: "))
                if self.studentNumbers.__contains__(studentNo):
                    break
                else:
                    continue
            except:
                print("Invalid Student Number!")

        self.studentNumbers = []
        return studentNo

    def editStudent(self):
        while True:
            try:
                print("\n")
                print("Edit Student".center(50),"_")

                studentNo = self.selectStudentNumberByClassId()
                if studentNo == 0:
                    break

                hold = studentNo

                student = self.db.getStudentByNumber(studentNo)
                print("For information that you do not want to change, you can press the 'ENTER' key!")
                student.name = input("Name: ") or student.name
                student.surname = input("Surname ") or student.surname
                
                student.studentNumber = self.inputStudentNumber("select * from students where StudentNumber = %s and StudentNumber != "+str(hold),student.studentNumber) 
                student.TC = self.inputTC("select * from students where TC = %s and StudentNumber != "+str(hold),student.TC) 
                student.gender = self.inputGender(student.gender) 

                while True:
                    try:
                        print("Birthdate: ")
                        year = input("Year: ") or student.birthdate.year
                        month = input("Month: ") or student.birthdate.month
                        day = input("Day: ") or student.birthdate.day
                        student.birthdate = datetime(int(year),int(month),int(day))  
                    except:
                        print("Invalid birthdate! Try again!")
                    else:
                        break

                choice = input("Press 'y' if you want to change the student's class or press any key to continue: ")
                if choice.lower() == "y":
                    student.classid = self.selectClass() or student.classid

            except Exception as ex:
                print("Error:",ex)
            
            else:
                choice = input(f"Press 'ENTER' key to update the student or press any key to cancel: ")
                if(choice == ""):
                     self.db.editStudent(student)
                else: print("The operation is canceled!")

            finally:
                if input("Press any key to continue to update student or press 'e' to exit!\n-> ") =="e":
                    break

    def deleteStudent(self):
        while True:
            try:
                print("\n")
                print("Delete Student".center(50,"_"))
                studentNo = self.selectStudentNumberByClassId()
                if studentNo == 0:
                    break
            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to delete the student or press any key to cancel: ")
                if(choice == ""):
                     self.db.deleteStudentByNumber(studentNo)
                else: print("The operation is canceled!")            
            finally:
                if input("Press any key to continue to delete student or press 'e' to exit!\n-> ") =="e":
                    break          

    def inputStudentNumber(self,sql,alternateNumber = 0):
        while True:
            try:
                studentNo = input("Student No: ") or alternateNumber
                studentNo = int(studentNo)
                values = (studentNo,)
                if(self.db.isValueExist(sql,values)):
                    print("Entered student number already using!")
                    continue
                elif (studentNo<0):
                    print("Student number cannot lower than 0!")
                    continue

            except Exception as ex:
                print("Error:",ex)
            else:
                break

        return studentNo



    #TEACHERS
    def teacherMenu(self):
        message = "1-Display Teachers\n2-Add Teacher\n3-Edit Teacher\n4-Delete Teacher\ne-Exit\n"
        while True:

            print("\n")
            print("Teacher menu".center(50,"_"))
            print(message)

            choice = input("Choice => ")

            if choice == "e":
                break
                
            match(choice):

                case "1":
                    branchid = self.selectLessonId()
                    sql = "select * from teachers where BranchId = %s order by Id"
                    values = (branchid,)
                    self.displayTeachers(sql=sql,values=values)
                    self.teacherIds = []

                case "2":
                    self.addTeacher()

                case "3":
                    self.editTeacher()
                
                case "4":
                    self.deleteTeacher()

                case _:
                    print("Invalid Choice\n")

    def displayLessons(self):
        lessons = self.db.getLessons()

        for l in lessons:
            print(f"id: {l.id}  |  name: {l.name}")
            self.lessonids.append(str(l.id))

        if len(self.lessonids) == 0:
            print("There is no lesson!\n")
            return 0

        input("\nPress any key to continue: ")

    def selectLessonId(self):       

        if(self.displayLessons() == 0):
            self.lessonids = []
            return 0

        while True:
            lessonid = input("\nSelect lesson id: ")
            if lessonid == "":
                continue
            elif self.lessonids.__contains__(lessonid):
                break
            else:
                print("Invalid lessonid id!\n")
        self.lessonids = []
        return int(lessonid)

    def displayTeachers(self,sql,values):
        teacherList = self.db.getTeachers(sql,values)

        if len(teacherList) == 0:
            print("There is no teacher!")
            return 0

        for teacher in teacherList:
            print(f"Id: {teacher.id} | Fullname: {teacher.name} {teacher.surname} | TC: {teacher.TC} | Birthdate: {teacher.birthdate} | Gender: {teacher.gender}")
            self.teacherIds.append(teacher.id)

        input("\nPress any key to continue: ")

    def addTeacher(self):
        while True:
            print("\n")
            print("Add Teacher".center(50,"_"))
            try:
                branchid = self.selectLessonId()
                if branchid == 0:
                    break
                name = input("Name: ")
                surname = input("Surname: ")
                
                TC = self.inputTC(sql="select * from teachers where TC = %s")
                gender = self.inputGender()
                birthdate = self.inputBirthdate()
                self.checkNameSurname([name,surname])

            except Exception as ex:
                print("Error:",ex)
            else:
                teacher = Teacher(None,name,surname,TC,birthdate,gender,branchid)
                self.db.addTeacher(teacher)
            finally:
                if input("Press any key to continue to add teacher or press 'e' to exit!\n-> ") =="e":
                    break

    def selectTeacherById(self,sql,values):

        if(self.displayTeachers(sql = sql,values=values) == 0):
            return 0

        while True:
            try:
                teacherid = int(input("Select teacher id: "))
                if self.teacherIds.__contains__(teacherid):
                    break
                else:
                    continue
            except:
                print("Invalid teacher id!")

        self.teacherIds = []
        return teacherid

    def editTeacher(self):
        while True:
            try:
                print("\n")
                print("Edit Teacher".center(50,"_"))

                branchid = self.selectLessonId()
                if branchid == 0:
                    break
                sql = "select * from teachers where BranchId = %s order by Id"
                values = (branchid,)
                teacherid = self.selectTeacherById(sql=sql,values = values)
                if teacherid == 0:
                    break

                teacher = self.db.getTeacherById(teacherid)
                print("For information that you do not want to change, you can press the 'ENTER' key!")

                teacher.name = input("Name: ") or teacher.name
                teacher.surname = input("Surname ") or teacher.surname
                
                teacher.TC = self.inputTC("select * from teachers where TC = %s and Id != "+str(teacherid),teacher.TC) 
                teacher.gender = self.inputGender(teacher.gender) 

                while True:
                    try:
                        print("Birthdate: ")
                        year = input("Year: ") or teacher.birthdate.year
                        month = input("Month: ") or teacher.birthdate.month
                        day = input("Day: ") or teacher.birthdate.day
                        teacher.birthdate = datetime(int(year),int(month),int(day))  
                    except:
                        print("Invalid birthdate! Try again!")
                    else:
                        break

                choice = input("Press 'y' if you want to change the teacher's branch or press any key to continue: ")
                if choice.lower() == "y":
                    teacher.branchid = self.selectLessonId() or teacher.branchid

            except Exception as ex:
                print("Error:",ex)
            
            else:
                choice = input(f"Press 'ENTER' key to update the teacher or press any key to cancel: ")
                if(choice == ""):
                     self.db.editTeacher(teacher)
                else: print("The operation is canceled!")

            finally:
                if input("Press any key to continue to update teacher or press 'e' to exit!\n-> ") =="e":
                    break

    def deleteTeacher(self):
        while True:
            try:
                print("\n")
                print("Delete Teacher".center(50,"_"))
                branchid = self.selectLessonId()
                if branchid == 0:
                    break
                sql = "select * from teachers where BranchId = %s order by Id"
                values = (branchid,)
                teacherid = self.selectTeacherById(sql=sql,values=values)
                if teacherid == 0:
                    break

            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to delete the teacher or press any key to cancel: ")
                if(choice == ""):
                     self.db.deleteTeacherById(teacherid)
                else: print("The operation is canceled!")            
            finally:
                if input("Press any key to continue to delete teacher or press 'e' to exit!\n-> ") =="e":
                    break        



    #CLASSES
    def classMenu(self):
        message = "1-Display Classes\n2-Add Class\n3-Edit Class\n4-Delete Class\n5-Assign a teacher to class\n6-Change assigned teacher to class\ne-Exit\n"
        while True:

            print("\n")
            print("Class menu".center(50,"_"))
            print(message)

            choice = input("Choice => ")

            if choice == "e":
                break
                
            match(choice):
                case "1":
                    self.displayClasses()

                case "2":
                    self.addClass()

                case "3":
                    self.editClass()

                case "4":
                    self.deleteClass()

                case "5":
                    self.assignTeacherToClass()

                case "6":
                    self.changeAssignedTeacher()

                case _:
                    print("Invalid Choice\n")

    def addClass(self):
        while True:
            print("\n")
            print("Add Class".center(50,"_"))
            self.displayClasses()
            try:
                className = input("\nEnter class name: ")
                if(self.db.isValueExist("select lower(Name) from classes where Name = %s",(className.lower(),))):
                    print("Entered class name already using!")
                    continue
            except Exception as ex:
                print("Error:",ex)
            else:
                newclass = Class(None,className.upper())
                self.db.addClass(newclass)
            finally:
                if input("Press any key to continue to add class or press 'e' to exit!\n-> ") =="e":
                    break

    def editClass(self):
        while True:
            print("\n")
            print("Edit Class".center(50,"_"))
            try:
                classid = self.selectClass()
                if classid == 0:
                    break
                className = input("\nEnter class name: ")
                if(self.db.isValueExist("select lower(Name) from classes where Name = %s and Id!= %s",(className.lower(),classid,))):
                    print("Entered class name already using!")
                    continue
            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to update the class or press any key to cancel: ")
                if(choice == ""):
                    self.db.editClass(classid,className)
                else: print("The operation is canceled!")
            finally:
                if input("Press any key to continue to update class or press 'e' to exit!\n-> ") =="e":
                    break

    def deleteClass(self):
        while True:
            try:
                classid = self.selectClass()
                if classid == 0:
                    break
            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to delete the class or press any key to cancel: ")
                if(choice == ""):
                    self.db.deleteClassById(classid)

                else: print("The operation is canceled!")
                
            finally:
                if input("Press any key to continue to delete class or press 'e' to exit!\n-> ") =="e":
                    break
           
    def assignTeacherToClass(self):
        while True:
            print("\n")
            print("Assign Teacher to Class".center(50,"_"))
            try:
                classid = self.selectClass()
                if classid == 0:
                    break
                branchid = self.selectLessonId()
                if branchid == 0:
                    break
                sql = "select * from teachers where BranchId = %s order by Id"
                values = (branchid,)
                teacherid = self.selectTeacherById(sql=sql,values=values)
                if teacherid == 0:
                    break
                

                if(self.db.isValueExist("select * from teachersclasses where ClassId = %s and TeacherId = %s",(classid,teacherid,))):
                    print("Selected teacher already assigned to the selected class!")
                    continue
            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to assign teacher to class or press any key to cancel: ")
                if(choice == ""):
                    teacherclass = TeacherClass(teacherid,classid)
                    self.db.assignTeacherToClass(teacherclass)

                else: print("The operation is canceled!")

            finally:
                if input("Press any key to continue to assign teacher to class or press 'e' to exit!\n-> ") =="e":
                    break

    def changeAssignedTeacher(self): 
        while True:
            print("\n")
            print("Change the teacher assigned to the class".center(50,"_"))
            try:
                print("\nSelect Current Teacher Id!\n")
                classid = self.selectClass()
                if classid == 0:
                    break
                sql = "select Id,Name,Surname,TC,Birthdate,Gender,Branchid from teachers inner join teachersclasses on teachersclasses.TeacherId = teachers.Id where ClassId = %s"
                values = (classid,)
                currentTeacherId = self.selectTeacherById(sql=sql,values=values)

                print("\nSelect the New Teacher Id!\n")
                branchid = self.displayLessons()
                sql = "select * from teachers where BranchId = %s order by Id"
                values = (branchid,)
                newTeacherid = self.selectTeacherById(sql=sql,values = values)
                
                if(self.db.isValueExist("select * from teachersclasses where ClassId = %s and TeacherId = %s",(classid,newTeacherid,))):
                    print("Selected teacher already assigned to the selected class!")
                    continue

            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to assign teacher to class or press any key to cancel: ")
                if(choice == ""):
                    self.db.changeAssignedTeacher(classid,currentTeacherId,newTeacherid)

                else: print("The operation is canceled!")

            finally:
                if input("Press any key to continue to change assigned teacher or press 'e' to exit!\n-> ") =="e":
                    break



    # LESSONS
    def lessonMenu(self):
        message = "1-Display Lessons\n2-Add Lesson\n3-Edit Lesson\n4-Delete Lesson\ne-Exit\n"
        while True:

            print("\n")
            print("Lesson menu".center(50,"_"))
            print(message)

            choice = input("Choice => ")

            if choice == "e":
                break
                
            match(choice):
                case "1":
                    self.displayLessons()

                case "2":
                    self.addLesson()

                case "3":
                    self.editLesson()

                case "4":
                    self.deleteLesson()

                case _:
                    print("Invalid Choice\n")

    def addLesson(self):
        while True:
            try:
                name = input("Lesson Name: ")
                
                if(self.db.isValueExist("select lower(Name) from lessons where lower(Name) = %s",(name.lower(),))):
                    print("Entered lesson name already using!")
                    continue

            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to add lesson or press any key to cancel: ")
                if(choice == ""):
                    lesson = Lesson(None,name.capitalize())
                    self.db.addLesson(lesson)
                else: print("The operation is canceled!")
            finally:
                if input("Press any key to continue to add lesson or press 'e' to exit!\n-> ") =="e":
                    break

    def editLesson(self):
        while True:
            try:
                lessonid = self.selectLessonId()
                if lessonid == 0:
                    break
                name = input("New Lesson Name: ")
                
                if(self.db.isValueExist("select lower(Name) from lessons where lower(Name) = %s and Id != %s",(name.lower(),lessonid,))):
                    print("Entered lesson name already using!")
                    continue

            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to update lesson or press any key to cancel: ")
                if(choice == ""):
                    lesson = Lesson(lessonid,name.capitalize())
                    self.db.editLesson(lesson)
                else: print("The operation is canceled!")
            finally:
                if input("Press any key to continue to update lesson or press 'e' to exit!\n-> ") =="e":
                    break

    def deleteLesson(self):
        while True:
            try:
                lessonid = self.selectLessonId()
                if lessonid == 0:
                    break
            except Exception as ex:
                print("Error:",ex)
            else:
                choice = input(f"Press 'ENTER' key to delete lesson or press any key to cancel: ")
                if(choice == ""):
                    self.db.deleteLessonById(lessonid)
                else: print("The operation is canceled!")
            finally:
                if input("Press any key to continue to delte lesson or press 'e' to exit!\n-> ") =="e":
                    break



    #Global Functions
    def inputBirthdate(self):
        while True:
            try:
                print("Birthdate: ")
                year = input("Year: ")
                month = input("Month: ")
                day = input("Day: ")
                birthdate = datetime(int(year),int(month),int(day))
            except:
                print("Invalid birthdate! Try again!")
            else:
                break
        return birthdate

    def inputGender(self,alternate = ""):
        while True:
            gender = input("Gender (Female = f / Male = m): ") or alternate
            gender = gender.lower()
            if(gender == 'm'  or gender == 'f'):
                break
            else: print("Invalid gender! Please try again!")
        return gender

    def inputTC(self,sql,alternate = ""):
        while True:
            try:
                TC = input("TC: ") or alternate

                if len(TC) != 11:
                    continue

                int(TC)

                if(self.db.isValueExist(sql,(TC,))):
                    print("Entered TC already using!")
                    continue

            except Exception as ex:
                print("Error:",ex)
            else:
                break

        return TC
    
    def checkNameSurname(self,list): 
        for value in list:
            if value == "":
                raise Exception("Please fill all the informations!")

        if re.search("[1-9]",list[0]) or re.search("[1-9]",list[1]):
            raise Exception("Name and surname cannot contain a numerical values!")
        elif not list[0].isalpha() or not list[1].isalpha(): 
            raise Exception("Invalid Characters in name or surname!")

try:
    app = App()
except Exception as ex:
    print("\nError:",ex)
else:
    app.initApp()
