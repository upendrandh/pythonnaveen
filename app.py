from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/admin')
def admin_login_page():
    return render_template("admin_login.html")


@app.route('/validate_admin', methods=["POST"])
def validateAdmin():
    uname = request.form.get("inputEmail")
    upass = request.form.get("inputPassword")
    # print(uname)
    # print(upass)
    if uname == "admin" and upass == "Admin99":
        return render_template("Admin_welcome.html")
    else:
        message = {"error": "userNotValid"}
        return render_template("admin_login.html", message=message)


@app.route('/admin_home')
def adminHome():
    return render_template("Admin_welcome.html")


@app.route('/new_class')
def new_class():
    return render_template("new_class.html")


@app.route('/save_course', methods=['POST'])
def save_course():
    cname = request.form.get('c1')
    fname = request.form.get('c2')
    date = request.form.get('c3')
    time = request.form.get('c4')
    fee = request.form.get('c5')
    dur = request.form.get('c6')

    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute("select max(cno) from course")
    res = curs.fetchone()
    if res[0]:
        cno = res[0] + 1
    else:
        cno = 1001

    curs.execute("insert into course values (?,?,?,?,?,?,?)", (cno, cname, fname, date, time, fee, dur))
    conn.commit()
    conn.close()
    return render_template('new_class.html', message="Data inserted successfully")


@app.route('/view_schedule')
def view_schedule():
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course")
    result = curs.fetchall()
    conn.close()
    return render_template("admin_view_schedule.html", data=result)


@app.route('/update_course')
def update_course():
    idno = request.args.get('cid')
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course where cno=?", (idno,))
    resust = curs.fetchone()
    return render_template("admin_update_course.html", data=resust)


@app.route('/update_save_course', methods=['POST'])
def update_save_course():
    cid = request.form.get('c0')
    cname = request.form.get('c1')
    fname = request.form.get('c2')
    date = request.form.get('c3')
    time = request.form.get('c4')
    fee = request.form.get('c5')
    dur = request.form.get('c6')
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute(
        "update course set course_name = ?,faculty_name = ?,class_date = ?,class_time = ?,fee = ?,duration = ? where cno = ?",
        (cname, fname, date, time, fee, dur, cid))
    conn.commit()
    conn.close()
    return view_schedule()


@app.route('/delete_course')
def delete_course():
    cid = request.args.get('cid')
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute("delete from course where cno = ?", (cid,))
    conn.commit()
    conn.close()
    return view_schedule()


#
# @app.route('/')
# def main():
#     return render_template("home.html")
@app.route('/')
def home_view():
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute("select * from course")
    dataview = curs.fetchall()
    return render_template("home.html", data=dataview)


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/save_student_data', methods=['POST'])
def save_student_data():
    sname = request.form.get('sname')
    cnomber = request.form.get('cnomber')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = sql.connect("naveen.sqlite2")
    curs = conn.cursor()
    curs.execute(" select max(sid) from student_register")
    res = curs.fetchone()
    if res[0]:
        sid = res[0] + 1
    else:
        sid = 101
    curs.execute("insert into student_register values (?,?,?,?,?)", (sid, sname, cnomber, email, password))
    conn.commit()
    conn.close()

    return render_template('login.html')


@app.route('/validate_student',methods=['POST'])
def validate_student():
    email=request.form.get('email')
    password=request.form.get('password')
    conn=sql.connect('naveen.sqlite2')
    curs=conn.cursor()
    curs.execute("select * from student_register where email = ? and password = ?",(email,password))
    result=curs.fetchall()

    curs.execute("select * from course")
    dataview = curs.fetchall()
    if result:
        for i in result:
            res=i[2]
        return render_template("welcome_student.html",data=dataview,connom=res)
    else:
        return render_template('login.html',message="There was a problem logging in. Check your email and password or create an account.")





@app.route('/welcome_student')
def welcome_student():
    conn=sql.connect("naveen.sqlite2")
    curs=conn.cursor()
    curs.execute("select * from course")
    dataview=curs.fetchall()
    return render_template('welcome_student.html',data=dataview)

@app.route('/register')
def register():
    return render_template("login.html", signup_message="you must login/signup to register")

@app.route('/register_course')
def register_course():
    cid=request.args.get("cid")
    connom=request.args.get("connom")
    conn=sql.connect("naveen.sqlite2")
    curs=conn.cursor()
    curs.execute("select max(eid) from course_register")
    enroll=curs.fetchone()
    if enroll[0]:
        eid=enroll[0]+1
    else:
        eid=1



    curs.execute("insert into course_register values (?,?,?)",(cid,connom,eid))

    curs.execute("select * from course")
    dataview=curs.fetchall()
    conn.commit()
    conn.close()

    return render_template("welcome_student.html",message="your course registerd successfully",data=dataview)





@app.route("/contactus")
def contuctus():
    return render_template("contactus.html")


if __name__ == "__main__":
    app.run(debug=True, port="5002")
