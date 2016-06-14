from SQLHandler import SQLHandler
from Reddit import Reddit
from NLTKHandler import NLTKHandler
import time                

def thenOrThan(words):
    return "then" if "then" in words else "than"

count = 0

while True:
    sql = SQLHandler()
    reddit = Reddit()
    nltk = NLTKHandler()
    
    count += 1
    
    print "Beginning Iteration " + str(count)
    print "Gathering Comments"
    
    comments = reddit.getNewComments()
    views = sql.getViews()
    
    print "Processing Data"
    for comment in comments:
        flag = True
        words = [x.lower().strip() for x in comment[0].split()]
        thenorthan = thenOrThan(words)
        
        for i in views:
            if comment[1] == i[0]:
                flag = False
                break
        
        if (flag):
            flag = nltk.analyze(reddit, comment, words, thenorthan)
        
        if (flag):
            nltk.processSentence(comment, words, thenorthan)

    print "Sleeping for 1 minute"
    time.sleep(60)