import nltk
from SQLHandler import SQLHandler

class NLTKHandler:
    
    def __init__(self):
        self.sql = SQLHandler()
        return
    
    def tokenize(self, sentence):
        tokenizedSentence = nltk.word_tokenize(sentence)
        
        return tokenizedSentence
    
    def tag(self, tokenizedSentence):
        tagTuple = nltk.pos_tag(tokenizedSentence)
        
        return tagTuple
    
    def getTopThenTags(self):
        return self.sql.getTopThenTags()
    
    def getTopThanTags(self):
        return self.sql.getTopThanTags()
    
    def findThenThanIndex(self, words, thenorthan):
        return words.index(thenorthan)
    
    def checkRange(self, words, index, thenthanIndex):
        if (index + thenthanIndex) >= len(words):
            return False
        elif (index + thenthanIndex) < 0:
            return False
        
        return True
    
    def findWord(self, words, word, index, thenthanIndex):
        if (self.checkRange(words, index, thenthanIndex)):
            if (words[index + thenthanIndex] == word):
                return True
            
        return False
    
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
    
    def processSentence(self, comment, words, thenorthan):
        self.sql.newView(comment[1])
        thenthanIndex = self.findThenThanIndex(words, thenorthan)
        index = 0
        
        tokenizedWords = self.tokenize(words)
        tags = self.tag(tokenizedWords)
        
        for tup in tags:
            if (thenorthan == "then"):
                exists = self.sql.thenTagExists(tup[0], index - thenthanIndex)
                
                if (index - thenthanIndex <= 3 and index - thenthanIndex >= -3 and index - thenthanIndex != 0):
                    if (exists):
                        self.sql.updateThenTag(tup[1], index - thenthanIndex)
                    else:
                        self.sql.newThenTag(tup[1], index - thenthanIndex)
            else:
                exists = self.sql.thanTagExists(tup[0], index - thenthanIndex)
                
                if (index - thenthanIndex <= 3 and index - thenthanIndex >= -3 and index - thenthanIndex != 0):
                    if (exists):
                        self.sql.updateThanTag(tup[1], index - thenthanIndex)
                    else:
                        self.sql.newThanTag(tup[1], index - thenthanIndex)
            index += 1
    
    def analyze(self, reddit, comment, words, thenorthan):
        commented = self.sql.getComments()
        
        if (comment[1] in commented):
            return False
        
        thenthanIndex = self.findThenThanIndex(words, thenorthan)
        threshold = self.sql.getConfidence()
        thresholdN = threshold[1]
        threshold = threshold[0]
        then = self.getTopThenTags()
        than = self.getTopThanTags()
        
        if (thenorthan == "then"):
            confidence = self.getThenConfidence(then, than, words, thenthanIndex)
        elif (thenorthan == "than"):
            confidence = self.getThanConfidence(then, than, words, thenthanIndex)
            
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
                self.sql.newComment(comment[1])
                
                if (confidence < threshold):
                    thresholdN += 1
                    threshold += confidence
                    self.sql.updateConfidence(threshold, thresholdN)
                
            elif (confirm.lower() == "n"):
                if (confidence > threshold):
                    thresholdN += 1
                    threshold += confidence
                    self.sql.updateConfidence(threshold, thresholdN)
        
        return True