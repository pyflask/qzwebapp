###########################################################################
#
#   File Name      Date        Owner           Description
#   ---------    -------     ---------        ------------
#   utls.py     7/8/2014   Archana Bahuguna  Utility fuctions for 
#                                            qzengine restful APIs
#
###########################################################################

from sqlalchemy.exc import InvalidRequestError
import models
import logs

def display_tables():
    """ Displays db table entries after processing request """
    prompt = '__________________________________________\n'\
             'To view tables enter Yes/yes/y/No/no/n:'
    #i = raw_input(prompt)
    i = "yes"
    if i.lower() in ('yes','y'):
        import os
        os.system('clear')
        try:
            #import pdb; pdb.set_trace()
            qry = models.User.query.all()
            logs.debug_ ('User Table\n=============:\nUserid  Username'\
                         '           Pwd\n')
            for i in qry:
                logs.debug_ (i)
                logs.debug_ ('\n------------------------------------------'\
                     '-----------------')
        except InvalidRequestError:
            print "Invalid request error in query in display tables"

        qry = models.User.query.all()
        logs.debug_ ('User Table\n=============:\nUserid  Username'\
                     '     Pwd     Role\n')
        for i in qry:
            logs.debug_ (i)
        logs.debug_ ('\n------------------------------------------'\
                     '-----------------')
        qry = models.Quiz.query.all()
        logs.debug_ ('Quiz Table\n=============:\n Qzid'\
                     'Title DifficultyLevel   Quiztext userid no_ques\n')
        for i in qry:
            logs.debug_ (i)
        logs.debug_ ('\n------------------------------------------'\
                     '-----------------')

        qry = models.Question.query.all()
        logs.debug_ ('Questions Table\n================:\nQid Qzid      QText'\
                      'Ans Text   Userid\n')
        for i in qry:
            logs.debug_ (i)
        logs.debug_ ('\n------------------------------------------------------')

        qry = models.Anschoice.query.all()
        logs.debug_ ('Ans Choices Table\n================:\nAnsid  Qzid'
                     '  Qid         Choices                          Correct\n')
        for i in qry:
            logs.debug_ (i)
        logs.debug_ ('\n------------------------------------------------------')

        qry = models.QResult.query.all()
        logs.debug_ ('Result Table\n=============:\nUserid  Qzid'\
                     'Quesid  Attemptid   Timestamp Score\n')
        for i in qry:
            logs.debug_ (i)
        logs.debug_ ('\n------------------------------------------'\
                     '-----------------')
    else:
        pass
    return None

