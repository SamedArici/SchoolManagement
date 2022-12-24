try:
    from connection import connection
except Exception as ex:
    print("\nError:",ex)

from student import Student
from classes import Class
from lesson import Lesson
from teacher import Teacher
from teacherclass import TeacherClass

import mysql.connector

class DBManager:
    def __init__(self):
   
        self.connection = connection
        self.cursor =self.connection.cursor()

    def getStudentByNumber(self,number):
        try:
            sql = "select * from students where StudentNumber = %s "
            value = (number,)
            self.cursor.execute(sql,value)

            obj = self.cursor.fetchone()
            return Student.createStudent(obj)[0]
        except Exception as err:
            print("Error:",err)

    def getClasses(self):
        try:
            sql = "select * from classes order by Id"
            self.cursor.execute(sql)

            obj = self.cursor.fetchall()
            return Class.createClass(obj)
        except Exception as ex:
            print("Error:",ex)

    def getStudents(self,classid):
        try:
            sql = "select * from students where ClassId = %s"
            values = (classid,)
            self.cursor.execute(sql,values)

            obj = self.cursor.fetchall()
            return Student.createStudent(obj)
        except Exception as ex:
            print("Error:",ex)

    def addStudent(self,student:Student):
        try:
            sql = "insert into students (StudentNumber,Name,Surname,TC,BirthDate,Gender,ClassId) values (%s,%s,%s,%s,%s,%s,%s)"
            values = (student.studentNumber,student.name,student.surname,student.TC,student.birthdate,student.gender,student.classid)
            self.cursor.execute(sql,values)

            self.connection.commit()
            print(f"{self.cursor.rowcount} student(s) added!")
        except Exception as ex:
            print(ex)

    def editStudent(self,student:Student):
        try:
            sql = "update students set StudentNumber = %s, Name = %s, Surname = %s, TC = %s, Birthdate = %s, Gender = %s, Classid = %s where Id = %s"
            values = (student.studentNumber,student.name,student.surname,student.TC,student.birthdate,student.gender,student.classid,student.id)

            self.cursor.execute(sql,values)

            self.connection.commit()
            print(f"{self.cursor.rowcount} student(s) updated!")
        except Exception as ex:
            print(ex)

    def deleteStudentByNumber(self,studentNumber):
        try:
            sql = "delete from students where StudentNumber = %s"
            values = (studentNumber,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} student(s) deleted!")
        except:
            print("Selected student cannot deleted!")

    def isValueExist(self,sql,values):

        self.cursor.execute(sql,values)
        result = self.cursor.fetchone()
        if not result:
            return False
        return True




    def getLessons(self):
        try:
            sql = "select * from lessons"
            self.cursor.execute(sql)
            obj = self.cursor.fetchall()
            return Lesson.createLesson(obj)

        except Exception as ex:
            print("Error:",ex)

    def getTeachers(self,sql,values):
        try:
            self.cursor.execute(sql,values)

            obj = self.cursor.fetchall()

            return Teacher.createTeacher(obj)

        except Exception as ex:
            print("Error:",ex)

    def addTeacher(self,teacher:Teacher):
        try:
            sql = "insert into teachers (Name,Surname,TC,BirthDate,Gender,BranchId) values (%s,%s,%s,%s,%s,%s)"
            values = (teacher.name,teacher.surname,teacher.TC,teacher.birthdate,teacher.gender,teacher.branchid)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} teacher(s) added!")
        except Exception as ex:
            print(ex)

    def getTeacherById(self,id):
        try:
            sql = "select * from teachers where Id = %s"
            value = (id,)
            self.cursor.execute(sql,value)
            obj = self.cursor.fetchone()
            return Teacher.createTeacher(obj)[0]
        except Exception as err:
            print("Error:",err)

    def editTeacher(self,teacher:Teacher):
        try:
            sql = "update teachers set Name = %s, Surname = %s, TC = %s, Birthdate = %s, Gender = %s, BranchId = %s where Id = %s"
            values = (teacher.name,teacher.surname,teacher.TC,teacher.birthdate,teacher.gender,teacher.branchid,teacher.id)

            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} teacher(s) updated!")
        except Exception as ex:
            print(ex)

    def deleteTeacherById(self,teacherid):
        try:
            sql = "delete from teachers where Id = %s"
            values = (teacherid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} teacher(s) deleted!")
        except mysql.connector.IntegrityError: 
            print("\nThe teacher cannot be deleted because he/she is enrolled in a class.\nFirst, delete the teacher from the class to which he/she is assigned!\n")
        except Exception as ex:
            print("Error:",ex)




    def addClass(self,newclass:Class):
        try:
            sql = "insert into classes (Name) values (%s)"
            values = (newclass.name,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} class(s) added!")
        except Exception as ex:
            print(ex)

    def editClass(self,classid,name):
        try:
            sql = "update classes set Name = %s where Id = %s"
            values = (name,classid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} class(es) updated!")
        except Exception as ex:
            print("Error:",ex)

    def deleteClassById(self,classid):
        try:
            sql = "delete from classes where Id = %s"
            values = (classid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} class(es) deleted!")
        except mysql.connector.IntegrityError: 
            print("\nThe class cannot be deleted because there are students or teachers enrolled in the class!\n")
        except Exception as ex:
            print("Error:",ex)

    def assignTeacherToClass(self,teacherclass:TeacherClass):
        try:
            sql = "insert into teachersclasses (ClassId,TeacherId) values (%s,%s)"
            values = (teacherclass.classid,teacherclass.teacherid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} teacher(s) assigned!")
        except Exception as ex:
            print("Error:",ex)

    def changeAssignedTeacher(self,classid,currentTeacherId,NewTeacherId):
        try:
            sql = "update teachersclasses set TeacherId = %s where TeacherId = %s and ClassId = %s"
            values = (NewTeacherId,currentTeacherId,classid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} teacher(s) changed!")
        except Exception as ex:
            print("Error:",ex)




    def addLesson(self,lesson:Lesson):
        try:
            sql = "insert into lessons (Name) values (%s)"
            values = (lesson.name,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} lesson(s) added!")
        except Exception as ex:
            print("Error:",ex)

    def editLesson(self,lesson:Lesson):
        try:
            sql = "update lessons set Name = %s where Id = %s"
            values = (lesson.name,lesson.id,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} lesson(s) updated!")
        except Exception as ex:
            print("Error:",ex)

    def deleteLessonById(self,lessonid):
        try:
            sql = "delete from lessons where Id = %s"
            values = (lessonid,)
            self.cursor.execute(sql,values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} lesson(s) deleted!")
        except mysql.connector.IntegrityError: 
            print("\nThe lesson cannot be deleted because there are teachers enrolled!\n")
        except Exception as ex:
            print("Error:",ex)            