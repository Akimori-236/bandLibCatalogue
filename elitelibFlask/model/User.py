from model.DatabasePool import DatabasePool

class User:
    # User LOG IN
    @classmethod
    def loginUser(cls, username, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM user WHERE username=%s AND password=%s'
            cursor.execute(sql,(username, password))
            user = cursor.fetchone() # should only return 1 entry

            if user == None:
                auth = False
            else:
                auth = True
            return auth
        finally:
            dbConn.close()
            print('Connection released')

    # INSERT new user [Hashed password]
    # @classmethod
    # def insertUser(cls, jsonUser):
    #     try:
    #         dbConn = DatabasePool.getConnection()
    #         cursor = dbConn.cursor(buffered=True)

    #         #Hashing
    #         passwordBytes = jsonUser['password'].encode() #convert string to bytes
    #         hashed = bcrypt.hashpw(passwordBytes, bcrypt.gensalt())

    #         sql = "INSERT INTO user(username, password) VALUES (%s, %s)"
    #         cursor.execute(sql,(jsonUser['username'], hashed))
    #         dbConn.commit()
    #         rows = cursor.rowcount
    #         return rows
    #     finally:
    #         dbConn.close()
    #         print("Connection released.")

    # # DELETE user by username
    # @classmethod
    # def deleteUsername(cls, username):
    #     try:
    #         dbConn = DatabasePool.getConnection()
    #         cursor = dbConn.cursor(buffered=True)
    #         sql="DELETE from user WHERE username=%s"
    #         cursor.execute(sql,(username,))
    #         dbConn.commit() #effect the database modification
    #         rows=cursor.rowcount
    #         return rows
    #     finally:
    #         dbConn.close()
    #         print("Connection released")