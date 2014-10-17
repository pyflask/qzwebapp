###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   views.py      8/20/2014   Archana Bahuguna  View fns for qzngn web app
#
#  Handles HTTP requests for a qzengine using Flask/SQLAlchemy. 
#  Flask session is implemented, Flask bcrypt is used for pwd encryption.
#  Jinja templatig is used for ui of web app
#
###########################################################################

import os, logging
from pprint import pprint
from flask import Flask, request, render_template, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy
from flask.ext.bcrypt import Bcrypt


import models 
import config 
import utls 
import logs 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index.html', methods = ['GET'])
def index():

    # GET /
    if request.method == 'GET':
        error = None
        """Get index.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("index.html get fn: %s" %(request))

        # Return response
        utls.display_tables()
        return render_template('login.html', error=error)

@app.route('/login', methods = ['POST'])
def login():

    # POST
    if request.method == 'POST':
        error = None
        """Post """
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login get fn: %s" %(request))

        username = request.form["username"]
        pwd = request.form["password"]
        encrypted_pwd = bcrypt.generate_password_hash(pwd)

        user_obj=models.User.query.filter_by(username=username).all()

        if (not user_obj):
            user_obj = models.User(username,bcrypt.\
                                          generate_password_hash(pwd))
            models.db.session.add(user_obj)
            models.db.session.commit()

        # Create Flask session
        if 'username' not in session:
            session['username'] = username

        # Return response
        utls.display_tables()
        location = "/quizzes"
        response = make_response(render_template('login.html', error=error),
                                 303)
        response.location=location
        return response

@app.route('/logout')
def logout():

    # GET /
    error = None
    logs.debug_ ("_______________________________________________")
    logs.debug_ ("QuizzesAPI post fn: %s" %(request))

    session.pop('username',None)

    # Return response
    utls.display_tables()
    return render_template('logout.html', error=error)

@app.route('/quizzes', methods = ['GET'])
def quizzes():

    # GET /quizzes
    if request.method == 'GET':
        error = None
        """Get all quiz questions"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("QuizzesAPI get fn: %s" %(request))

        username = session['username']
        # Return response
        utls.display_tables()
        response= make_response(render_template('welcome.html', 
                                                username=username, 
                                                error=error),
                                                200)
        return response
    
@app.route('/quizzes/<int:qzid>/questions', methods = ['GET', 'POST'])
def quiz_questions(qzid):

    # GET /quizzes/qzid/questions
    if request.method == 'GET':
        error = None
        """Get all quiz questions"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("QuizzesAPI get fn: %s" %(request))

        # Query Question table
        ques = models.Question.query.join(models.Anschoice).filter\
                         (models.Question.qzid == qzid).all()

        # Return response
        utls.display_tables()
        return render_template('questions.html', ques=ques, error=error)
    
    #POST /quizzes/qzid/questions
    else:
        error = None
        """ Post answers to all quiz questions"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("QuizzesAPI Post fn: %s" %(request))

        #get all questions from db
        ques_obj = models.Question.query.join(models.Anschoice).filter\
                         (models.Question.qzid == qzid).all()

        #User must tick one checkbox per ques and only one
        ansidlist = request.form.getlist("choices")

        #Getting a list of qid, ansid answeres- [[qid, ansid, anstext],...]
        qanslist = []
        for i in range(len(ques_obj)):
            tmplist = ansidlist[i].encode('utf-8').split(',')
            qanslist.append([int(tmplist[0]), int(tmplist[1]),tmplist[2]])

        # Just for testing setting userid = 1
        username = session['username']
        user_obj = models.User.query.filter_by(username=username).first()
        userid = user_obj.userid

        #Check the attempt no for the quiz taker  
        qzattemptid_obj = models.QResult.query.with_entities(\
                   sqlalchemy.func.max(models.QResult.qzattemptid)).\
                   filter_by(qzid=qzid, userid=userid).first()
        if (qzattemptid_obj == (None,)):
            qzattemptid = 1
        else:
            qzattemptid = qzattemptid_obj[0] + 1

        #Check quiz taker's answers against ones in the table
        qindex = 0
        Resultlist = []
        for index in range(len(qanslist)):

            qid=qanslist[index][0]

            qscore = 0
            for ans in ques_obj[index].anschoices:
                if ((ans.qid == qanslist[index][0]) and
                    (ans.ansid == qanslist[index][1]) and
                    (ans.correct == True)):

                    #Correct ans increment score
                    qscore = 1
            #Update results table with qz question score for user with timestmp
            Resultlist.append(models.QResult(userid, qzid, qid, qzattemptid, \
                                                                     qscore))
        models.db.session.add_all(Resultlist)
        models.db.session.commit()

        utls.display_tables()

        # Return response
        response = make_response(render_template('answers.html', 
                                                 ques_obj=ques_obj, 
                                                 qzid=qzid, 
                                                 qanslist=qanslist, 
                                                 error=error), 
                                                 200
                                )
        return response


@app.route('/quizzes/<int:qzid>/result', methods = ['GET', 'POST'])
def quiz_result(qzid):

    # GET /user/quizzes/{qzid}/result
    if ((request.method == 'GET') or (request.method == 'POST')):
        error = None
        """Get result for taker of this  quiz"""
        logs.debug_ ("_________________________________________________")
        logs.debug_ ("UsrQuizRtAPI get fn: %s" %(request))

        # get user id for user - in this case just create default?
        username = session['username']
        user_obj = models.User.query.filter_by(username=username).first()
        userid = user_obj.userid


        # Find quiz result for session
        qz_obj = models.Quiz.query.filter_by(qzid=qzid).first()
        qztitle = qz_obj.title

        qzattemptid = models.QResult.query.with_entities(sqlalchemy.func.max\
                                  (models.QResult.qzattemptid)).\
                                  filter_by(userid=userid, qzid=qzid).first()

        if (qzattemptid[0] == None):
            return render_template('result.html')

        cur_qscore_obj = models.QResult.query.with_entities(models.QResult.qid,\
                          models.QResult.score).filter_by(userid=userid, \
                          qzid=qzid, qzattemptid=qzattemptid[0]).all()

        allqscore_obj = models.QResult.query.with_entities(models.QResult.qid,\
                          sqlalchemy.func.sum(models.QResult.score).\
                          label("score")).filter_by(userid=userid, qzid=qzid).\
                          group_by(models.QResult.qid).all()

        cur_qzscore = 0
        for index in range(len(cur_qscore_obj)):
            cur_qzscore += cur_qscore_obj[index][1]

        # Return response
        location = "/quizzes/%d/%d/result" % (qzid , userid)
        response = make_response(render_template('result.html', 
                                                 username=username,
                                                 qztitle=qztitle,
                                                 cur_qscore_obj=cur_qscore_obj,
                                                 cur_qzscore=cur_qzscore,
                                                 qzattemptid=qzattemptid[0],
                                                 allqscore_obj=allqscore_obj,
                                                 error=error),
                                                 200)
        response.location=location
        return response


if __name__ == '__main__':

    config.db_init()
    #Initial config for db, this can be disabled
    utls.display_tables()

    app.debug = True
    app.run('192.168.33.10', 5001)

