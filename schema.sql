DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quizzes;
DROP TABLE IF EXISTS Results;

CREATE TABLE Students (
    id INTEGER PRIMARY KEY,
	fname TEXT,
    lname TEXT
);

CREATE TABLE Quizzes (
	id INTEGER PRIMARY KEY,
	subject TEXT,
    questionsNum INTEGER,
    date DATE
);

CREATE TABLE Results (
	sid INTEGER,
    qid INTEGER,
	score REAL
);

INSERT INTO Students(id, fname, lname) VALUES(1, "John", "Smith");


INSERT INTO Quizzes(id, subject, questionsNum, date) VALUES(1, "Python Basics", 5, "2015-02-05");


INSERT INTO Results(sid, qid, score) VALUES(1, 1, 85);