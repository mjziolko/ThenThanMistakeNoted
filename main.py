from SQLHandler import SQLHandler
from Reddit import Reddit
from WLMHandler import WLMHandler
import time                

count = 0

while True:
    sql = SQLHandler()
    reddit = Reddit()
    wlm = WLMHandler()
    
    count += 1
    
    print "Beginning Iteration " + str(count)
    print "Gathering Comments"
    
    comments = reddit.getNewComments()
    
    viewed = sql.getViews()
    commented = sql.getComments()
    
    print "Processing Data"
    for comment in comments:
        threshold = sql.getConfidence()
        thresholdN = threshold[1]
        threshold = threshold[0]
        
        if (comment[1] in commented):
            commented = sql.getComments()
            continue
        elif (comment[1] in viewed):
            continue
        else:
            sql.newView(comment[1])
            viewed = sql.getViews()
        
        thenthanIndex = 0
        startIndex = 0
        expected = None
        wordList = [x.lower().strip() for x in comment[0].split()]
        
        if ("then" in wordList):
            thenthanIndex = wordList.index("then")
            expected = "then"
        else:
            thenthanIndex = wordList.index("than")
            expected = "than"
        
        if (thenthanIndex - 4 < 0):
            startIndex = 0
        else:
            startIndex = thenthanIndex - 4
            
        words = " ".join(wordList[startIndex:thenthanIndex])
        
        result = wlm.determine(words)
        
        if (result == None or result[0] == expected):
            continue
        else:
            confidence = abs(result[1] - result[2])
            if (confidence > 1):
                print "-----------------------------------------------"
                print "                  COMMENTING!                  "
                print "-----------------------------------------------"
                print "Comment Text:\n"
                print comment[0]
                print "Probability Values: (update, old)"
                print str(result[1]) + ", " + str(result[2])
                print "Confidence:"
                print confidence
                if (thresholdN != 0):
                    print "Threshold:"
                    print threshold/thresholdN
                
                
                confirm = raw_input("Comment on this post? y/n ")
                
                if (confirm.lower() == "y"):
                    reddit.postComment(comment[1])
                    sql.newComment(comment[1])
                    
                    if (confidence < threshold/thresholdN):
                        thresholdN += 1
                        threshold += confidence
                        sql.updateConfidence(threshold, thresholdN)
                        sql.addFalseNegative()
                    else:
                        sql.addTruePositive()
                    
                elif (confirm.lower() == "n"):
                    if (confidence > threshold/thresholdN):
                        thresholdN += 1
                        threshold += confidence
                        sql.updateConfidence(threshold, thresholdN)
                        sql.addFalsePositive()
                    else:
                        sql.addTrueNegative()
        
    print "Sleeping for 1 minute"
    time.sleep(60)