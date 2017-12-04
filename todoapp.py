#Praveen Lama

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import sqlite3

app = Flask(__name__)


class Student:
    def __init__(self, id, fname, lname):
        self.id = id
        self.fname = fname
        self.lname = lname


class Quiz:
    def __init__(self, id, subject, questionsNum, date):
        self.id = id
        self.subject = subject
        self.questionsNum = questionsNum
        self.date = date


class Results:
    def __init__(self, sid, qid, score):
        self.sid = sid
        self.qid = qid
        self.score = score


@app.route('/')
def showHomePage():
    # First check if the user is already logged in
    if 'loggedState' in session:
        return redirect("/dashboard")
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc

    username = request.form['username']
    password = request.form['password']
    login_failed = False

    if username == "admin" and password == "password":
        session['loggedState'] = True
        return redirect("/dashboard")  # redirect to dashboard
    else:
        login_failed = True
        return render_template("login.html",login_failed=login_failed)

    return redirect("/login")

@app.route('/login', methods=['GET'])
def showLogin():
    # First check if the user is already logged in
    if 'loggedState' in session:
        return redirect("/dashboard")
    return render_template('login.html')


@app.route('/dashboard')
def showDashboard():
    conn = sqlite3.connect("mydb.db")

    StudentsSQL = conn.execute("SELECT * FROM Students ORDER BY id ASC")
    QuizzesSQL = conn.execute("SELECT * FROM Quizzes ORDER BY id ASC")

    Students = []
    Quizzes = []

    for student in StudentsSQL.fetchall():
        Students.append(Student(student[0], student[1], student[2]))

    for quiz in QuizzesSQL.fetchall():
        Quizzes.append(Quiz(quiz[0], quiz[1], quiz[2], quiz[3]))

    conn.commit()
    conn.close()
    return render_template('dashboard.html',Students = Students, Quizzes = Quizzes)


@app.route('/student/add', methods=['GET'])
def showAddStudent():
    # Check if the user is not logged in
    if 'loggedState' not in session:
        return redirect("/login")
    return render_template('student.html')


@app.route('/student/add', methods=['POST'])
def addStudent():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc
    fname = request.form['fname']
    lname = request.form['lname']

    conn = sqlite3.connect("mydb.db")
    connStatement = 'INSERT INTO Students(id, fname, lname) VALUES(NULL, "%s", "%s");' % (fname, lname)
    conn.execute(connStatement)
    conn.commit()
    conn.close()

    return redirect('/dashboard')


@app.route('/quiz/add', methods=['GET'])
def showAddQuiz():
    # Check if the user is not logged in
    if 'loggedState' not in session:
        return redirect("/login")
    return render_template('quiz.html')


@app.route('/quiz/add', methods=['POST'])
def addQuiz():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc
    subject = request.form['subject']
    questionsNum = request.form['questionsNum']
    date = request.form['date']


    conn = sqlite3.connect("mydb.db")
    connStatement = 'INSERT INTO Quizzes(id, subject, questionsNum, date) VALUES(NULL, "%s", "%s", "%s");' % (subject,questionsNum,date)
    conn.execute(connStatement)
    conn.commit()
    conn.close()

    return redirect('/dashboard')


@app.route('/student/<id>', methods=['GET','POST'])
def showStudentResult(id):
    conn = sqlite3.connect("mydb.db")

    ResultsSQL = conn.execute("SELECT * FROM Results WHERE sid == " + id)

    StudentsSQL = conn.execute("SELECT * FROM Students WHERE id == " + id)

    ResultsArr = []
    StudentsArr = []

    for res in ResultsSQL.fetchall():
        ResultsArr.append(Results(res[0], res[1], res[2]))

    for res in StudentsSQL.fetchall():
        StudentsArr.append(Student(res[0], res[1], res[2]))

    StudentIndividual = StudentsArr[0]
    conn.commit()
    conn.close()
    return render_template('results.html', lname = StudentIndividual.lname, fname = StudentIndividual.fname, results=ResultsArr)


@app.route('/results/add', methods=['GET'])
def showAddResults():
    # Check if the user is not logged in
    if 'loggedState' not in session:
        return redirect("/login")

    conn = sqlite3.connect("mydb.db")

    StudentsSQL = conn.execute("SELECT * FROM Students ORDER BY id ASC")
    QuizzesSQL = conn.execute("SELECT * FROM Quizzes ORDER BY id ASC")

    Students = []
    Quizzes = []

    for student in StudentsSQL.fetchall():
        Students.append(Student(student[0], student[1], student[2]))

    for quiz in QuizzesSQL.fetchall():
        Quizzes.append(Quiz(quiz[0], quiz[1], quiz[2], quiz[3]))

    conn.commit()
    conn.close()

    return render_template('addResults.html', Students=Students, Quizzes=Quizzes)


@app.route('/results/add', methods=['POST'])
def addStudentResult():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc
    sid = request.form['sid']
    qid = request.form['qid']
    score = request.form['score']

    conn = sqlite3.connect("mydb.db")
    connStatement = 'INSERT INTO Results(sid, qid, score) VALUES("%s", "%s", "%s");' % (sid,qid,score)
    conn.execute(connStatement)
    conn.commit()
    conn.close()

    return redirect('/dashboard')


app.secret_key = '\x17\x96e\x94]\xa0\xb8\x1e\x8b\xee\xdd\xe9\x91^\x9c\xda\x94\t\xe8S\xa1Oe_'


def loadDatabase():
    conn = sqlite3.connect('mydb.db')
    f = open('schema.sql', 'r')
    sql = f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()


def main():
    loadDatabase()
    app.run()

if __name__ == '__main__':
    main()