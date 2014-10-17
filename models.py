###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   models.py      7/8/2014   Archana Bahuguna  Db table design/models 
#                                                for qzengine APIs 
#
#   Schema- models.db - tables: Users, Quizzes, Questions and Answer choices
#
###########################################################################

from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
import textwrap, os
from views import app, bcrypt

file_path = os.path.abspath(os.getcwd())+"/models.db"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+file_path
app.config['SQLALCHEMY_RECORD_QUERIES']=True
db = SQLAlchemy(app)

MAXUSRS = 1000
MAXQZ = 100
MAXQS = 10000
MAXANS = 50000
MAXRST = 10000

class User(db.Model):
    """ Defines the columns and keys for User table """
    userid    = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(32))
    password  = db.Column(db.String(16))

    def generate_userid():
        """Generator fn for unique quiz id"""
        for index in range(1, MAXUSRS, 1):
            yield index

    gen_userid = generate_userid()

    quizzes = db.relationship("Quiz", backref = "user")
    quizzes = db.relationship("QResult", backref = "user")

    def __init__ (self, username, password):
        self.userid = self.gen_userid.next()
        self.username = username
        self.password = password

    def __repr__(self):
        return '%i        %s            %s' % (self.userid, self.username, self.password)

    
class Quiz(db.Model):
    """ Defines the columns and keys for Quiz table """
    qzid    = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(80), unique = True)
    difficulty_level = db.Column(db.String(80))
    text    = db.Column(db.String(80))
    userid  = db.Column(db.Integer, db.ForeignKey('user.userid'))
    no_ques = db.Column(db.Integer)

    questions = db.relationship("Question", backref = "quiz")

    def generate_qzid():
        """Generator fn for unique quiz id"""
        for index in range(1, MAXQZ, 1):
            yield index

    gen_qzid = generate_qzid()

    def __init__ (self, title, difficulty_level, text, userid, no_ques=0):
        self.qzid = self.gen_qzid.next()
        self.title = title
        self.difficulty_level = difficulty_level
        self.text = text
        self.userid = userid
        self.no_ques = no_ques

    def __repr__(self):
        return '%i   %s     %s     %s     %i    %i' % (self.qzid, self.title, \
        self.difficulty_level, (self.text).ljust(20), self.userid, self.no_ques)
                    

class Question(db.Model):
    """ Defines the columns and keys for Question table """
    qid      = db.Column(db.Integer, primary_key=True)
    ques_text= db.Column(db.String(80), unique = True)
    ans_text = db.Column(db.String(80))
    qzid     = db.Column(db.Integer, db.ForeignKey('quiz.qzid'))
    userid   = db.Column(db.Integer, db.ForeignKey('user.userid'))

    anschoices = db.relationship("Anschoice", backref = "question")

    def generate_quesid():
        """Generator fn for unique ques id"""
        for index in range(1, MAXQS, 1):
            yield index

    gen_qid = generate_quesid()

    def __init__ (self, ques_text, ans_text, qzid, userid):
        self.qid  = self.gen_qid.next()
        self.ques_text = ques_text
        self.ans_text  = ans_text
        self.qzid = qzid
        self.userid = userid

    def __repr__(self):
        return '%i     %i          %s   %s    %i' % (self.qid, self.qzid, \
                self.ques_text, self.ans_text, self.userid)

class Anschoice(db.Model):
    """ Defines the columns and keys for Answer Choices table """
    ansid      = db.Column(db.Integer, primary_key = True)
    qzid       = db.Column(db.Integer, db.ForeignKey('quiz.qzid'))
    qid        = db.Column(db.Integer, db.ForeignKey('question.qid'))
    ans_choice = db.Column(db.String(80))
    correct    = db.Column(db.Boolean)

    def generate_ansid():
        """Generator fn for unique ans id"""
        for index in range(1, MAXANS, 1):
            yield index

    gen_ansid = generate_ansid()

    def __init__ (self, qzid, qid, ans_choice, correct):
        self.ansid      = self.gen_ansid.next()
        self.qzid       = qzid
        self.qid        = qid
        self.ans_choice = ans_choice
        self.correct    = correct

    def __repr__(self):
        return '%i        %i     %i     %s      %r' % (self.ansid, self.qzid, \
                self.qid, self.ans_choice, self.correct)


class QResult(db.Model):
    """ Defines the columns and keys for User table """
    qscoreid  = db.Column(db.Integer, primary_key=True)
    userid    = db.Column(db.Integer,db.ForeignKey('user.userid'))
    qzid      = db.Column(db.Integer,db.ForeignKey('quiz.qzid'))
    qid       = db.Column(db.Integer,db.ForeignKey('question.qid'))
    qzattemptid = db.Column(db.Integer)
    timestamp = db.Column(db.String)
    score     = db.Column(db.Integer)

    def generate_qscoreid():
        """Generator fn for unique quiz id"""
        for index in range(1, MAXRST, 1):
            yield index

    gen_qscoreid = generate_qscoreid()

    def __init__ (self, userid, qzid, qid, qzattemptid, score=0):
        self.qscoreid = self.gen_qscoreid.next()
        self.userid = userid
        self.qzid = qzid
        self.qid = qid
        self.qzattemptid = qzattemptid
        self.timestamp = datetime.now()
        self.score = score

    def __repr__(self):
        return '%i   %i  %i %i  %s   %i' % (self.userid, self.qzid, self.qid, self.qzattemptid, self.timestamp, self.score)


