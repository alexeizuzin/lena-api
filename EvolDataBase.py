import sqlite3, random
from datetime import datetime

class EvolDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getUser(self, id):
        try:
            self.__cur.execute(f"SELECT name FROM users WHERE id='{id}'")
            res = self.__cur.fetchone()
            if res: return res
        except:
            print('error reading from db')
        return []

    def getUsers(self):
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('error reading from db')
        return []

    def getUserId(self, login):
        try:
            self.__cur.execute(f" SELECT id FROM users WHERE login='{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except:
            print('error reading from db')
        return []


    def checkAddingUser(self, login):
        self.__cur.execute(f" SELECT COUNT() as 'count' FROM users WHERE login LIKE '{login}' ")
        res = self.__cur.fetchone()
        if res['count'] > 0:
            print('error - such email already exists')
            return False
        return True


    def addUser(self, name, hpsw, login, email):
        try:
            if self.checkAddingUser(login):
                self.__cur.execute( "INSERT INTO users VALUES(null, ?, ?, ?, ?)", (name, login, hpsw, email,) )
                self.__db.commit()
        except sqlite3.Error as e:
            print( 'error adding '+ str(e) )
            return False
        return True

    
    # AIUTHORIZED USERS

    def getAuthUsers(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM auth_users")
            res = self.__cur.fetchone()
            if res: return res
        except:
            print('error reading from db')
        return []

    def getAuthUser(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM auth_users WHERE id='{id}'")
            res = self.__cur.fetchone()
            if res: return res
        except:
            print('error reading from db')
        return []

    def checkAuthUserById(self, id):
        self.__cur.execute(f"SELECT COUNT() as 'count' FROM auth_users WHERE id='{id}' ")
        res = self.__cur.fetchone()
        #print('FUNCTION CHECK')
        if res['count'] > 0:
            return False
        return True






    def updateAuthUser(self, code, id):
        try:
            self.__cur.execute(f"UPDATE auth_users SET code='{code}' WHERE id='{id}'")
            print('ROW COUNT', self.__cur.rowcount)
            self.__db.commit()
            if self.__cur.rowcount == 0: return False
        except sqlite3.Error as e:
            print( 'error adding '+ str(e) )
            return False
        return True


    def addAuthUser(self, id):
        code = ''
        try:
            lst = random.sample(range(0, 10), 10)  
            for n in lst:
                code+=str(n)
            is_auth_updated = self.updateAuthUser(code, id)
            if not is_auth_updated:   
                self.__cur.execute( "INSERT INTO auth_users VALUES(?, ?)", (id, code,) )
                self.__db.commit()
        except sqlite3.Error as e:
            print( 'error adding '+ str(e) )
            return False
        print('CODE:', code)
        return code



    def userVerificationWhenSendingMessage(self, id, code):
        self.__cur.execute(f"SELECT COUNT() as 'count' FROM auth_users WHERE id='{id}' AND code='{code}'")
        res = self.__cur.fetchone()
        if res['count'] > 0:
            return True
        return False
        

    # MESSAGES 

    def addMessageInDB(self, id, msg):
        try:
            self.__cur.execute( "INSERT INTO messages VALUES(?, ?, ?)", (id, msg, datetime.now(), ) )
            self.__db.commit()
        except sqlite3.Error as e:
            print( 'error adding '+ str(e) )
            return False
        return True

    def getMessages(self):
        try:
            self.__cur.execute(f"SELECT * FROM messages")
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('error reading from db')
        return []


    def getUserPsw(self, id):
        try:
            print('ID:', id)
            self.__cur.execute(f"SELECT psw FROM users WHERE id='{id}'")
            res = self.__cur.fetchone()
            print('result:', res)
            if res: return res
        except:
            print('error reading from db')
        return []


    def isAuthValid(self, id, code):
        try:
            self.__cur.execute(f"SELECT * FROM auth_users WHERE id='{id}' AND code='{code}'")
            res = self.__cur.fetchone()
            print('AUTH USER:', res, None, res!=None)
            if res != None: return True
        except:
            print('error reading from db')
        return False