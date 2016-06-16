import praw
from config import *
import unicodedata

class Reddit:
    
    def __init__(self):
        userAgent = ("ThenThan 0.5")
        self.r = praw.Reddit(user_agent = userAgent)
        self.r.login(REDDIT_USERNAME, REDDIT_PASS)
        self.subs = open("subreddits", "r")
        
    def convertToString(self, s):
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore")
    
    def removeRedditQuotes(self, s):
        lines = s.split('\n')
        restructuredString = ""
        
        for line in lines:
            line = line.strip()
            if (len(line) > 0 and line[0] != '>'):
                restructuredString = restructuredString + line + '\n'
                                
        return restructuredString
        
    def getNewComments(self):
        comments = []
        filteredComments = []
        ids = []
        
        for sub in self.subs:
            s = self.r.get_subreddit(sub.strip())
            comments = s.get_comments()
                                   
            for comment in comments:
                quotelessString = self.removeRedditQuotes(comment.body)
                for split in quotelessString.split('.'):
                    if " then " in split or " than " in split:
                        if (comment.id not in ids):
                            index = 0
                            ids.append(comment.id)
                            filteredComments.append([split, comment.id, sub])
                        else:
                            index += 1
                            filteredComments.append([split, comment.id + "-" + str(index), sub])
                            
        
        return filteredComments
    
    def postComment(self, commentId):
        try:
            if ('-' in commentId):
                commentId = (commentId.split('-')[0]).strip()
            
            commentId = "t1_" + commentId
            comment = self.r.get_info(thing_id=commentId)
            comment.reply("[ ](http://grammarist.com/usage/than-then/)")
        except:
            print "Could not find submission with id " + commentId + "\n Try posting manually."