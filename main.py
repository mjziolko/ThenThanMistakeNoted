from SQLHandler import SQLHandler
from Reddit import Reddit
from Analyzer import Analyzer
import time

def thenOrThan(words):
    return "then" if "then" in words else "than"

count = 0

while True:
    sql = SQLHandler()
    reddit = Reddit()
    analyzer = Analyzer()
    
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
            flag = analyzer.analyze(sql, reddit, comment, words, thenorthan)
        
        if (flag):
            analyzer.processWordsForDB(sql, reddit, comment, words, thenorthan)

    print "Sleeping for 1 minute"
    time.sleep(60)