import sqlite3 as sql

conn=sql.connect("naveen.sqlite2")
curs=conn.cursor()

def createCourseTable():
    curs.execute("create table course(cno number  primary key ,course_name text ,faculty_name text ,class_date date ,class_time time ,fee real ,duration number )")
    conn.close()
    print("table is created")
def createStudentDataTable():
    curs.execute("create table student_register(sid number primary key ,studnet_name text,contact_number number unique not null ,email text unique not null ,password text)")
    conn.close()
    print("table is created")
def registerCourse():
    curs.execute("create table course_register(eid number primary key ,student_number number ,course_id number )")
    conn.close()
    print("table is created")


