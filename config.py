###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   config.py      8/20/2014   Archana Bahuguna  Populates tables for  
#                                                Quizngn Database  
#
###########################################################################

import models, utls
from sqlalchemy.exc import IntegrityError, InvalidRequestError

def db_init():

    models.db.drop_all()
    models.db.create_all()
    utls.display_tables()

    #populate Quiz table
    qz1 = models.Quiz( "Python Basics  ", "Simple  ", "Explanation", 1, 2)
    qz2 = models.Quiz( "Python Advanced", "Moderate", "No text    ", 1)
    models.db.session.add_all([qz1,qz2])

    #populate models.Questions table
    #Quiz 1
    ques1 = models.Question("What does 'def foo(): pass do", 
                     "A fn which does nothing",1,1)
    ques2 = models.Question("Is python an OOP l           ", 
                     "Yes python is an OOP l",1,1)
    ques3 = models.Question("What is operator overloading?", 
                     "Operator overloading is a concept in OOPS",1,1)
    ques4 = models.Question("Is python dynmaically typed? ", 
                     "Yes python is a dynmaically typed language",1,1)
    models.db.session.add_all([ques1, ques2, ques3, ques4])

    #Quiz 1
    ques5 = models.Question("What is the use of an assertion?",
                     "A fn which does nothing",2,1)
    ques6 = models.Question("What is python library scrapy used for?",
                     "Yes python is an OOP l",2,1)
    models.db.session.add_all([ques5, ques6])

    #populate Answer choices table
    #Quiz 1
    ans1  = models.Anschoice(1, 1, "(a) This function does nothing      ", True)
    ans2  = models.Anschoice(1, 1, "(b) This function returns a fn pass ", False)
    ans3  = models.Anschoice(1, 1, "(c) This function is not yet defined", False)
    ans4  = models.Anschoice(1, 2, "(a) Yes Python is object oriented   ", True)
    ans5  = models.Anschoice(1, 2, "(b) No Python is not object oriented", False)
    ans6  = models.Anschoice(1, 2, "(c) Python may not be used as OOP l ", False)
    ans7  = models.Anschoice(1, 3, "(a) This function does nothing      ", True)
    ans8  = models.Anschoice(1, 3, "(b) This function returns a fn pass ", False)
    ans9  = models.Anschoice(1, 3, "(c) This function is not yet defined", False)
    ans10  = models.Anschoice(1, 4, "(a) Yes Python is object oriented   ", True)
    ans11  = models.Anschoice(1, 4, "(b) No Python is not object oriented", False)
    ans12  = models.Anschoice(1, 4, "(c) Python may not be used as OOP l ", False)
    models.db.session.add_all([ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8,\
                        ans9, ans10, ans11, ans12])
    #Quiz 2
    ans13  = models.Anschoice(2, 5, "(a) This function does nothing      ", False)
    ans14  = models.Anschoice(2, 5, "(b) This function returns a fn pass ", True)
    ans15  = models.Anschoice(2, 5, "(c) This function is not yet defined", False)
    ans16  = models.Anschoice(2, 6, "(a) Yes Python is object oriented   ", False)
    ans17  = models.Anschoice(2, 6, "(b) No Python is not object oriented", True)
    ans18  = models.Anschoice(2, 6, "(c) Python may not be used as OOP l ", False)
    models.db.session.add_all([ans13, ans14, ans15, ans16, ans17, ans18])
    try:
        models.db.session.commit()
    except IntegrityError:
        print "Arch: Caught SQL Alchemy exception Integrity Error"
    except InvalidRequestError:
        print "Arch: Caught SQL Alchemy exception InvalidRequestError"

    return None
