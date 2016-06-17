import string, unicodedata
from __builtin__ import True

class Analyzer:
    def __init__(self):
        return
    
    def removePunctuation(self, s):
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore")
        return s.translate(string.maketrans("",""), string.punctuation).strip()
    
    def findThenThanIndex(self, words, thenorthan):
        return words.index(thenorthan)
    
    def findWord(self, words, word, index, thenthanIndex):
        if (self.checkRange(words, index, thenthanIndex)):
            if (words[index + thenthanIndex] == word):
                return True
            
        return False
    
    def checkRange(self, words, index, thenthanIndex):
        if (index + thenthanIndex) >= len(words):
            return False
        elif (index + thenthanIndex) < 0:
            return False
        
        return True

    def confidenceWeight(self, index):
        index = abs(index)
        
        if (index == 1):
            return 1
        elif (index == 2):
            return .66
        elif (index == 3):
            return .33

    def getThenConfidence(self, then, than, words, thenthanIndex):
        confidence = 0
        
        i = 0
        for t in than:
            index = t[1]
            word = t[0]
            
            if (self.findWord(words, word, index, thenthanIndex)):
                confidence = (100 - (i * 10)) * self.confidenceWeight(index)
                
            i += 1
        
        if (confidence > 0):
            i = 0
            for t in then:
                index = t[1]
                word = t[0]
                
                if (self.findWord(words, word, index, thenthanIndex)):
                    confidence = confidence - ((100 -(i * 10)) * self.confidenceWeight(index))
                i += 1
                
        return confidence

    def getThanConfidence(self, then, than, words, thenthanIndex):
        confidence = 0
        
        i = 0
        for t in then:
            index = t[1]
            word = t[0]
                
            if (self.findWord(words, word, index, thenthanIndex)):
                confidence = (100 - (i * 10)) * self.confidenceWeight(index)
            i += 1
                
        if (confidence > 0):
            i = 0
            for t in than:
                index = t[1]
                word = t[0]
            
                if (self.findWord(words, word, index, thenthanIndex)):
                    confidence = confidence - ((100 - (i * 10)) * self.confidenceWeight(index))
                i += 1
                    
        return confidence
    
    def processWordsForDB(self, sql, reddit, comment, words, thenorthan):
        sql.newView(comment[1])
        thenthanIndex = self.findThenThanIndex(words, thenorthan)
        index = 0
        
        for word in words:
            
            if (word == "the" or len(word) < 3 or len(word) > 15):
                continue
            
            if (index - thenthanIndex <= 3 and index - thenthanIndex >= -3):
                word = self.removePunctuation(word)
                
                if (thenorthan == "then"):
                    exists = sql.thenExists(word, index - thenthanIndex)
                    
                    if (exists):
                        sql.updateThen(word, index - thenthanIndex)
                    else:
                        sql.newThen(word, index - thenthanIndex)
                else:
                    exists = sql.thanExists(word, index - thenthanIndex)
                    
                    if (exists):
                        sql.updateThan(word, index - thenthanIndex)
                    else:
                        sql.newThan(word, index - thenthanIndex)
        
            index += 1
    
    def analyze(self, sql, reddit, comment, words, thenorthan):
        try:
            commented = sql.getComments()
            
            if (comment[1] in commented):
                return False
            
            thenthanIndex = self.findThenThanIndex(words, thenorthan)
            threshold = sql.getConfidence()
            thresholdN = threshold[1]
            threshold = threshold[0]
            then = sql.getTopThens()
            than = sql.getTopThans()
            
            if (thenorthan == "then"):
                confidence = self.getThenConfidence(then, than, words, thenthanIndex)
            elif (thenorthan == "than"):
                confidence = self.getThanConfidence(then, than, words, thenthanIndex)
                
            if (confidence > threshold / thresholdN):
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
        
                reddit.postComment(comment[1])
                sanitizedComment = self.removePunctuation(comment[0])
                sql.newComment(comment[1], sanitizedComment, comment[2])
            
            return True
        except:
            print "Error with unicode encoding."
            return False