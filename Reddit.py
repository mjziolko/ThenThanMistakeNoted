import praw
from config import *
import string
import unicodedata

class Reddit:
    
    def __init__(self):
        userAgent = ("ThenThan 0.5")
        self.r = praw.Reddit(user_agent = userAgent)
        self.r.login(REDDIT_USERNAME, REDDIT_PASS)
        self.subs = open("subreddits", "r")
        
    def convertToString(self, s):
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore")
        
    def removePunctuation(self, s):
        return s.translate(string.maketrans("",""), string.punctuation).strip()
        
    def getNewComments(self):
        comments = []
        filteredComments = []
        ids = []
        
        for sub in self.subs:
            s = self.r.get_subreddit(sub.strip())
            comments = s.get_comments()
                                   
            for comment in comments:
                for split in comment.body.split('.'):
                    sanitizedString = self.removePunctuation(self.convertToString(split))
                    
                    if " then " in split or " than " in split:
                        if (comment.id not in ids):
                            index = 0
                            ids.append(comment.id)
                            filteredComments.append([sanitizedString, comment.id])
                        else:
                            index += 1
                            filteredComments.append([sanitizedString, comment.id + "-" + str(index)])
                            
        
        return filteredComments
    
    def postComment(self, commentId):
        try:
            if ('-' in commentId):
                commentId = commentId.split('-')[0]
            
            commentId = "t1_" + commentId
            comment = self.r.get_info(thing_id=commentId)
            comment.reply("[ ](http://grammarist.com/usage/than-then/)")
        except:
            print "Could not find submission with id " + commentId + "\n Try posting manually."