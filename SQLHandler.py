import MySQLdb
import datetime
from config import *
from __builtin__ import True

class SQLHandler:
    db = MySQLdb.connect(SQL_SERVER, SQL_USERNAME, SQL_PASS, SQL_DB)
    cursor = db.cursor()
    
    def __init__(self):
        return
    
    def getThens(self):
        self.cursor.execute("SELECT word, count, position FROM thenthandb.then")
        results = self.cursor.fetchall()
        return results
    
    def getTopThens(self):
        self.cursor.execute("SELECT word, position, count as sum FROM thenthandb.then \
            WHERE word != 'then' \
            ORDER BY count desc \
            LIMIT 10")
        results = self.cursor.fetchall()
        return results
    
    def getTopThenTags(self):
        self.cursor.execute("SELECT tag, position FROM thenthandb.thentag \
            ORDER BY count desc \
            LIMIT 10")
        results = self.cursor.fetchall()
        return results
    
    def getTopThans(self):
        self.cursor.execute("SELECT word, position, count FROM thenthandb.than \
            WHERE word != 'than' \
            ORDER BY count desc \
            LIMIT 10")
        results = self.cursor.fetchall()
        return results
    
    def getTopThanTags(self):
        self.cursor.execute("SELECT tag, position FROM thenthandb.thantag \
            ORDER BY count desc \
            LIMIT 10")
        results = self.cursor.fetchall()
        return results
    
    def countTopThens(self):
        self.cursor.execute("SELECT SUM(count) FROM \
            (SELECT count FROM thenthandb.then WHERE word != 'then' ORDER BY count desc LIMIT 10) \
            as totalcount")
        results = self.cursor.fetchall()
        return results[0][0]
    
    def countTopThans(self):
        self.cursor.execute("SELECT SUM(count) FROM \
            (SELECT count FROM thenthandb.than WHERE word != 'than' ORDER BY count desc LIMIT 10) \
            as totalcount")
        results = self.cursor.fetchall()
        return results[0][0]
    
    def getThans(self):
        self.cursor.execute("SELECT word, count, position FROM thenthandb.than")
        results = self.cursor.fetchall()
        return results
    
    def newThen(self, word, position):
        try:
            self.cursor.execute("INSERT INTO thenthandb.then(word, count, position) \
                VALUES('%s', '%d', '%d')" % \
                (word, 0, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def newThenTag(self, tag, position):
        try:
            self.cursor.execute("INSERT INTO thenthandb.thentag(tag, count, position) \
                VALUES('%s', '%d', '%d')" % \
                (tag, 0, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            print "Tag: " + tag
            print "Pos: " + str(position)
            self.db.rollback()
            raise e
        
    def newThan(self, word, position):
        try:
            self.cursor.execute("INSERT INTO thenthandb.than(word, count, position) \
                VALUES('%s', '%d', '%d')" % \
                (word, 0, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def newThanTag(self, tag, position):
        try:
            self.cursor.execute("INSERT INTO thenthandb.thantag(tag, count, position) \
                VALUES('%s', '%d', '%d')" % \
                (tag, 0, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            print "Tag: " + tag
            print "Pos: " + str(position)
            self.db.rollback()
            raise e
    
    def updateThen(self, word, position):
        try:
            self.cursor.execute("UPDATE thenthandb.then SET count = count + 1 \
                WHERE word = '%s' AND position = '%d'" % \
                (word, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def updateThenTag(self, tag, position):
        try:
            self.cursor.execute("UPDATE thenthandb.thentag SET count = count + 1 \
                WHERE tag = '%s' AND position = '%d'" % \
                (tag, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def updateThan(self, word, position):
        try:
            self.cursor.execute("UPDATE thenthandb.than SET count = count + 1 \
                WHERE word = '%s' AND position = '%d'" % \
                (word, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def updateThanTag(self, tag, position):
        try:
            self.cursor.execute("UPDATE thenthandb.thantag SET count = count + 1 \
                WHERE tag = '%s' AND position = '%d'" % \
                (tag, position))
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
            
    def thenExists(self, word, position):
        try:
            self.cursor.execute("SELECT word FROM thenthandb.then \
                WHERE word = '%s' AND position = '%d'" % \
                (word, position))
            results = self.cursor.fetchall()
            
            if (len(results) > 0):
                return True
        
            return False
        
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
    
    def thenTagExists(self, tag, position):
        try:
            self.cursor.execute("SELECT tag FROM thenthandb.thentag \
                WHERE tag = '%s' AND position = '%d'" % \
                (tag, position))
            results = self.cursor.fetchall()
            
            if (len(results) > 0):
                return True
            
            return False
        
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
    
    def thanExists(self, word, position):
        try:
            self.cursor.execute("SELECT word FROM thenthandb.than \
                WHERE word = '%s' AND position = '%d'" % \
                (word, position))
            results = self.cursor.fetchall()
            
            if (len(results) > 0):
                return True
        
            return False
        
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def thanTagExists(self, tag, position):
        try:
            self.cursor.execute("SELECT tag FROM thenthandb.thantag \
                WHERE tag = '%s' AND position = '%d'" % \
                (tag, position))
            results = self.cursor.fetchall()
            
            if (len(results) > 0):
                return True
            
            return False
        
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
            
    def getViews(self):
        self.cursor.execute("SELECT id FROM thenthandb.viewed") #\
            #WHERE date > date_sub(CURDATE(), interval 12 hour)")
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

    def addFalsePositive(self):
        try:
            self.cursor.execute("UPDATE thenthandb.stats SET falsepositive = falsepositive + 1 \
                WHERE id = 1")
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def addFalseNegative(self):
        try:
            self.cursor.execute("UPDATE thenthandb.stats SET falsenegative = falsenegative + 1 \
                WHERE id = 1")
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def addTruePositive(self):
        try:
            self.cursor.execute("UPDATE thenthandb.stats SET truepositive = truepositive + 1 \
                WHERE id = 1")
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e
        
    def addTrueNegative(self):
        try:
            self.cursor.execute("UPDATE thenthandb.stats SET truenegative = truenegative + 1 \
                WHERE id = 1")
            self.db.commit()
            
        except MySQLdb.Error as e:
            self.db.rollback()
            raise e