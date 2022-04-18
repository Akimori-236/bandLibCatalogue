from model.DatabasePool import DatabasePool

class Music:
    
    # GET all Music
    @classmethod
    def getAllMusic(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'SELECT * FROM music'
            cursor.execute(sql)
            allMusic = cursor.fetchall()
            return allMusic
        finally:
            dbConn.close()
            print('Connection released')
            
            
            
    # Get music by musicID
    @classmethod
    def getMusicById(cls, musicid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'SELECT * from music WHERE musicid=%s'
            inputTerms = tuple(musicid)
            cursor.execute(sql,inputTerms)
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')
    
            
            
    # INSERT new music
    @classmethod
    def insertMusic(cls, jsonMusic):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "INSERT INTO music(name, description, releaseDate, imageURL, genreID) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(jsonMusic['name'], jsonMusic['description'], jsonMusic['releaseDate'], jsonMusic['imageURL'], jsonMusic['genreID']))
            dbConn.commit()
            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released.")



    @classmethod
    def deleteMusic(cls, musicid):
        try: 
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql="DELETE from music WHERE musicid=%s"
            cursor.execute(sql,(musicid,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")



    # SEARCH music by substring
    @classmethod
    def getMusicBySubstring(cls, substring):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "SELECT * from music WHERE name LIKE concat('%', %s, '%')"
            cursor.execute(sql,(substring,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')