from model.DatabasePool import DatabasePool

class Music:

    # GET all Music
    @classmethod
    def getAllMusic(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music'
            cursor.execute(sql)
            allMusic = cursor.fetchall()
            return allMusic
        finally:
            dbConn.close()
            print('Connection released')



    # Get music by Cat number
    @classmethod
    def getMusicByCatNo(cls, catno):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * from music WHERE catalogueNo=%s'
            values = tuple(catno)
            cursor.execute(sql, values)
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
            cursor = dbConn.cursor(buffered=True)
            sql = "INSERT INTO music(catalogueNo, categoryID, title, composer, arranger, publisher, featuredInstrument, ensembleID, parts, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = tuple(
                jsonMusic['catalogueNo'], 
                jsonMusic['categoryID'], 
                jsonMusic['title'], 
                jsonMusic['composer'], 
                jsonMusic['arranger'], 
                jsonMusic['publisher'], 
                jsonMusic['featuredInstrument'], 
                jsonMusic['ensembleID'], 
                jsonMusic['parts'], 
                jsonMusic['remarks'])
            cursor.execute(sql, values)
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
            cursor = dbConn.cursor(buffered=True)
            sql="DELETE from music WHERE musicid=%s"
            values = tuple(musicid)
            cursor.execute(sql, values)
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
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT * from music WHERE name LIKE concat('%', %s, '%')"
            values = tuple(substring)
            cursor.execute(sql, values)
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')