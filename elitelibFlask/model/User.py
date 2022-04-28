from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:
    @classmethod
    def getAllUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM user'
            cursor.execute(sql)
            allUsers = cursor.fetchall()
            return allUsers
        finally:
            dbConn.close()
            print('Connection released')



    @classmethod
    def getUserById(cls, userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * from user WHERE userid=%s'
            cursor.execute(sql,(userid,))
            user = cursor.fetchall()
            return user
        finally:
            dbConn.close()
            print('Connection released')



    # User Authentication
    @classmethod
    def loginUser(cls, email, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * from user WHERE email=%s AND password=%s'
            cursor.execute(sql,(email, password))
            user = cursor.fetchone() #email as an unique field in database should only return 1 entry

            if user == None:
                jwtToken = ""   # wrong credentials = empty reply
            else:
                payload = {"role": user['role'], "userid": user['userID'], "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)} #expiry time for token
                jwtToken = jwt.encode(payload, Settings.secretKey, algorithm="HS256") #encryption

            return jwtToken
        finally:
            dbConn.close()
            print('Connection released')

    # INSERT new user [Hashed password]
    @classmethod
    def insertUser(cls, jsonUser):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)

            #Hashing
            passwordBytes = jsonUser['password'].encode() #convert string to bytes
            hashed = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())

            sql = "INSERT INTO user(email, name, role, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql,(jsonUser['email'], jsonUser['name'], jsonUser['role'], hashed))
            dbConn.commit()                 # to commit changes to the database
            rows = cursor.rowcount          # returns number of changed rows
            return rows
        finally:
            dbConn.close()
            print("Connection released.")



    # SEARCH user by name
    @classmethod
    def getUserByName(cls, name):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * from user WHERE name=%s'
            cursor.execute(sql,(name,))
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
            print('Connection released')


    # UPDATE user by ID with new email & password
    @classmethod
    def updateUser(cls, userid, jsonUser):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "UPDATE user SET email=%s,password=%s where userid=%s"
            cursor.execute(sql, (jsonUser['email'], jsonUser['password'], userid))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")


    @classmethod
    def deleteUser(cls, userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql="DELETE from user WHERE userid=%s"
            cursor.execute(sql,(userid,))
            dbConn.commit() #effect the database modification
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")