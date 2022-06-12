from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app  = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class student(db.Model):
    student_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    roll_number = db.Column(db.Integer,unique=True,nullable=False)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80))
    courses = db.relationship("course", secondary="enrollments", back_populates="students")

    def __repr__(self) ->str:
        return f"{self.student_id} - {self.first_name}"

class course(db.Model):
    course_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    course_code = db.Column(db.String(80),unique=True,nullable=False)
    course_name = db.Column(db.String(80),nullable=False)
    course_description = db.Column(db.String(80))
    students = db.relationship("student", secondary="enrollments", back_populates="courses")

    def __repr__(self) ->str:
        return f"{self.course_id} - {self.course_name} - {self.course_description}"

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    estudent_id = db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
    ecourse_id = db.Column(db.Integer,db.ForeignKey('course.course_id'),nullable=False)

    
    

    def __repr__(self) ->str:
        return f"{self.enrollment_id}"

@app.route('/',methods=['GET','POST'])
def new():
    students = student.query.all()
    return render_template('index.html',students = students)
@app.route('/student/<int:stud_id>/delete')
def Delete(stud_id):
    data = student.query.filter_by(student_id=stud_id).first()
    datae = enrollments.query.filter_by(estudent_id=stud_id)
    for i in datae:
        db.session.delete(i)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')
@app.route('/student/<int:stud_id>/update',methods=['GET','POST'])
def Update(stud_id):
    stud = student.query.filter_by(student_id=stud_id).first()
    if request.method=='POST':
        new_f_name = request.form["f_name"]
        new_l_name = request.form["l_name"]
        stud.first_name = new_f_name
        stud.last_name = new_l_name
        stud.courses = []
        clist = request.form.getlist("courses")
        for i in clist:
            if i[-1] == '1':
                course_name = 'MAD1'
            elif i[-1] == '2':
                course_name = 'DBMS'
            elif i[-1] == '3':
                course_name = 'PDSA'
            else:
                course_name = 'BDM'
        
            course_n = course.query.filter_by(course_name=course_name).first()
            stud.courses.append(course_n)
        db.session.add(stud)
        db.session.commit()
        return redirect('/')

    return render_template('update.html',student=stud)
@app.route('/student/<int:stud_id>')
def details(stud_id):
    stud = student.query.filter_by(roll_number=stud_id).first()
    enroll_id = enrollments.query.filter_by(estudent_id=stud.student_id).all()
    course_list = []
    for i in enroll_id:
        
        course_list.append(course.query.filter_by(course_id=i.ecourse_id).first())
    return render_template('details.html',course_list=course_list,student=stud)
@app.route('/student/create',methods=['GET','POST'])
def new1():
    if request.method=="POST":
        nuke = student.query.all()
        roll_no = request.form["roll"]
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        clist = request.form.getlist("courses")
        for i in nuke:
            if str(roll_no) == str(i.roll_number):
                return render_template('error.html')
            else:
                stud = student(roll_number= roll_no,first_name=f_name,last_name=l_name)
                db.session.add(stud)
                for i in clist:
                    if i[-1] == '1':
                        course_name = 'MAD1'
                    elif i[-1] == '2':
                        course_name = 'DBMS'
                    elif i[-1] == '3':
                        course_name = 'PDSA'
                    else:
                        course_name = 'BDM' 
            
                    course_l = course.query.filter_by(course_name=course_name).first()
                    stud.courses.append(course_l)
                    db.session.add(stud)
        
        
        db.session.commit()
        
        return redirect('/')
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)