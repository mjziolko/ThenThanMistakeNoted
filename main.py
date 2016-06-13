from SQLHandler import SQLHandler
from Reddit import Reddit
import time

def findThenThanIndex(words, thenorthan):
    return words.index(thenorthan)

def thenOrThan(words):
    return "then" if "then" in words else "than"

def checkRange(words, index, thenthanIndex):
    if (index + thenthanIndex) >= len(words):
        return False
    elif (index + thenthanIndex) < 0:
        return False
    
    return True

def findWord(words, word, index, thenthanIndex):
    if (checkRange(words, index, thenthanIndex)):
        if (words[index + thenthanIndex] == word):
            return True
        
    return False

def confidenceWeight(index):
    index = abs(index)
    
    if (index == 1):
        return 1
    elif (index == 2):
        return .66
    elif (index == 3):
        return .33
    

def getThenConfidence(then, than, words, thenthanIndex):
    confidence = 0
    
    i = 0
    for t in than:
        index = t[1]
        word = t[0]
        
        if (findWord(words, word, index, thenthanIndex)):
            confidence = (100 - (i * 10)) * confidenceWeight(index)
            
        i += 1
    
    if (confidence > 0):
        i = 0
        for t in then:
            index = t[1]
            word = t[0]
            
            if (findWord(words, word, index, thenthanIndex)):
                confidence = confidence - ((100 -(i * 10)) * confidenceWeight(index))
            i += 1
            
    return confidence

def getThanConfidence(then, than, words, thenthanIndex):
    confidence = 0
    
    i = 0
    for t in then:
        index = t[1]
        word = t[0]
            
        if (findWord(words, word, index, thenthanIndex)):
            confidence = (100 - (i * 10)) * confidenceWeight(index)
        i += 1
            
    if (confidence > 0):
        i = 0
        for t in than:
            index = t[1]
            word = t[0]
        
            if (findWord(words, word, index, thenthanIndex)):
                confidence = confidence - ((100 - (i * 10)) * confidenceWeight(index))
            i += 1
                
    return confidence

def analyze(sql, reddit, comment, words, thenorthan):
    commented = sql.getComments()
    
    if (comment[1] in commented):
        return False
    
    thenthanIndex = findThenThanIndex(words, thenorthan)
    threshold = sql.getConfidence()
    thresholdN = threshold[1]
    threshold = threshold[0]
    then = sql.getTopThens()
    than = sql.getTopThans()
    
    if (thenorthan == "then"):
        confidence = getThenConfidence(then, than, words, thenthanIndex)
    elif (thenorthan == "than"):
        confidence = getThanConfidence(then, than, words, thenthanIndex)
        
    #if (confidence > threshold / thresholdN):
    if (confidence > 0):
        print "-----------------------------------------------"
        print "                  COMMENTING!                  "
        print "-----------------------------------------------"
        print "Confidence:"
        print confidence
        if (thresholdN != 0):
            print "Threshold:"
            print threshold/thresholdN
        print "Comment Text:\n"
        print comment[0]
        print "Words Compared From DB:\n"
        print "Then:"
        print then
        print "\nThan:"
        print than
        
        confirm = raw_input("Comment on this post? y/n: ")
        
        if (confirm.lower() == "y"):
            reddit.postComment(comment[1])
            sql.newComment(comment[1])
            
            if (confidence < threshold):
                thresholdN += 1
                threshold += confidence
                sql.updateConfidence(threshold, thresholdN)
            
        elif (confirm.lower() == "n"):
            if (confidence > threshold):
                thresholdN += 1
                threshold += confidence
                sql.updateConfidence(threshold, thresholdN)
    
    return True

def process(sql, reddit, comment, words, thenorthan):
    sql.newView(comment[1])
    thenthanIndex = findThenThanIndex(words, thenorthan)
    index = 0
    
    for word in words:
        
        if (word == "the" or len(word) < 3):
            continue
        
        if (thenorthan == "then"):
            exists = sql.thenExists(word, index - thenthanIndex)
            
            if (index - thenthanIndex <= 3 and index - thenthanIndex >= -3):
                if (exists):
                    sql.updateThen(word, index - thenthanIndex)
                else:
                    sql.newThen(word, index - thenthanIndex)
        else:
            exists = sql.thanExists(word, index - thenthanIndex)
            
            if (index - thenthanIndex <= 3 and index - thenthanIndex >= -3):
                if (exists):
                    sql.updateThan(word, index - thenthanIndex)
                else:
                    sql.newThan(word, index - thenthanIndex)
    
        index += 1
                

count = 0

while True:
    sql = SQLHandler()
    reddit = Reddit()
    
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
            flag = analyze(sql, reddit, comment, words, thenorthan)
        
        if (flag):
            process(sql, reddit, comment, words, thenorthan)

#    if (count % 2 == 1):
#        print "Cleaning up junk data..."
#        sql.cleanup()
#    else:
    print "Sleeping for 1 minute"
    time.sleep(60)