import MySQLdb
import datetime
from config import *
from __builtin__ import True

class SQLHandler:
    db = MySQLdb.connect(SQL_SERVER, SQL_USERNAME, SQL_PASS, SQL_DB)
    cursor = db.cursor()
    
    def __init__(self):
        return
            
    def getViews(self):
        self.cursor.execute("SELECT id FROM thenthandb.viewed") #\
        results = self.cursor.fetchall()
        return [item for sublist in results for item in sublist]
    
    def getComments(self):
        self.cursor.execute("SELECT id, date FROM thenthandb.commented")
        results = self.cursor.fetchall()
        return [item for sublist in results for item in sublist]
    
    def newView(self, commentId):
        try:
            self.cursor.execute("INSERT INTO thenthandb.viewed(id, date) \
                VALUES('%s', '%s')" % \
                (commentId, datetime.datetime.now()))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
            
    def newComment(self, commentId):
        try:
            self.cursor.execute("INSERT INTO thenthandb.commented(id, date) \
                VALUES('%s', '%s')" % \
                (commentId, datetime.datetime.now()))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def getConfidence(self):
        try:
            self.cursor.execute("SELECT threshold, n FROM thenthandb.confidence \
                WHERE id = 3")
                
            results = self.cursor.fetchall()
            return results[0]
        
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def updateConfidence(self, threshold, n):
        try:
            self.cursor.execute("UPDATE thenthandb.confidence SET threshold = '%d', n = '%d' \
                WHERE id = 3" % \
                (threshold, n))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
    
    def cleanup(self):
        try:
            self.cursor.execute("DELETE thenthandb.than, thenthandb.then FROM thenthandb.than INNER JOIN thenthandb.then \
                WHERE than.word = then.word AND than.position = then.position AND then.count < 30 AND than.count < 30")
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e