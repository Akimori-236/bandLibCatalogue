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


    # GET music by pages
    @classmethod
    def getMusicByPage(cls, page, rowCount):
        offset = (page-1)*rowCount
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music LIMIT %s, %s'
            values = tuple(offset, rowCount)
            cursor.execute(sql, values)
            pageOfMusic = cursor.fetchall()
            return pageOfMusic
        finally:
            dbConn.close()
            print('Connection released')

    # GET total count of music
    @classmethod
    def getTotalMusicCount(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT COUNT(musicID) FROM music'
            cursor.execute(sql)
            musicCount = cursor.fetchall()
            return musicCount
        finally:
            dbConn.close()
            print('Connection released')





    # Get music by musicID
    @classmethod
    def getMusicByID(cls, musicID):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * from music WHERE musicID=%s'
            values = tuple(str(musicID))
            cursor.execute(sql, values)
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')


    # SEARCH music by title
    @classmethod
    def searchMusicByTitle(cls, substring):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT * from music WHERE title LIKE concat('%', %s, '%')"
            values = tuple(substring)
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
            sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleID`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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


    # DELETE music by musicID
    @classmethod
    def deleteMusicByID(cls, musicID):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql="DELETE from music WHERE musicID=%s"
            values = tuple(musicID)
            cursor.execute(sql, values)
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")




