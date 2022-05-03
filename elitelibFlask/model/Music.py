from model.DatabasePool import DatabasePool
import pandas as pd

ensembleList = ["Concert Band", "Marching Band", "Solo", "Ensemble", "Big Band", "Study", "Reference", "Others"]

class Music:

    # GET all Music
    @classmethod
    def getAllMusic(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music ORDER BY catalogueNo'
            cursor.execute(sql)
            allMusic = cursor.fetchall()
            return allMusic
        finally:
            dbConn.close()
            print('Connection released')


    # GET music by categoryID
    @classmethod
    def getMusicByCatID(cls, catID):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music WHERE categoryID=%s ORDER BY catalogueNo'
            cursor.execute(sql, (catID,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')


    # GET music by ensemble type
    @classmethod
    def getMusicByEnsembleType(cls, ensemble):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music WHERE ensembleID=%s ORDER BY catalogueNo'
            cursor.execute(sql, (ensemble,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')


    # Get music by musicID
    @classmethod
    def getMusicByID(cls, musicID):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music WHERE musicID=%s ORDER BY catalogueNo'
            cursor.execute(sql, (musicID,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')


    # Get music by catNo
    @classmethod
    def getMusicByCatNo(cls, catNo):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT * FROM music WHERE catalogueNo=%s ORDER BY catalogueNo'
            cursor.execute(sql, (catNo,))
            music = cursor.fetchone()
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
            sql = "SELECT * from music WHERE title LIKE concat('%', %s, '%') ORDER BY catalogueNo"
            cursor.execute(sql, (substring,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')

    # SEARCH music by composer/arranger
    @classmethod
    def searchMusicByCompArr(cls, substring):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT * from music WHERE composer LIKE concat('%', %s, '%') OR arranger LIKE concat('%', %s, '%') ORDER BY catalogueNo"
            cursor.execute(sql, (substring, substring))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')

    # SEARCH music by Publisher
    @classmethod
    def searchMusicByPublisher(cls, substring):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT * from music WHERE publisher LIKE concat('%', %s, '%') ORDER BY catalogueNo"
            cursor.execute(sql, (substring,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')

    # SEARCH music by Featured Instrument
    @classmethod
    def searchMusicByFeatInstru(cls, substring):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT * from music WHERE featuredInstrument LIKE concat('%', %s, '%') ORDER BY catalogueNo"
            cursor.execute(sql, (substring,))
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
            cursor.execute(sql, (
                jsonMusic['catalogueNo'],
                jsonMusic['categoryID'],
                jsonMusic['title'],
                jsonMusic['composer'],
                jsonMusic['arranger'],
                jsonMusic['publisher'],
                jsonMusic['featuredInstrument'],
                jsonMusic['ensembleID'],
                jsonMusic['parts'],
                jsonMusic['remarks']
                ))
            dbConn.commit()
            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released.")


    # DELETE music by CatNo
    @classmethod
    def deleteMusicByCatNo(cls, catNo):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql="DELETE from music WHERE catalogueNo=%s"
            cursor.execute(sql, (catNo,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")


    # Wipe out current table and create new with CSV data
    @classmethod
    def parseCSV(cls, filePath):
        rows = 0
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)

            # Wipe out current Table
            sql = "TRUNCATE TABLE music;"
            cursor.execute(sql)
            dbConn.commit()

            # CVS Column Names
            col_names = ['Catalogue Number','Title','Composer', 'Arranger', 'Publisher', 'Featured Instrument(s)', 'Ensemble Type', 'Parts', 'Remarks']
            # Use Pandas to parse the CSV file
            csvData = pd.read_csv(filePath,names=col_names, header=None)

            # Loop through the Rows
            for i,row in csvData.iterrows():

                catalogueNo = row['Catalogue Number']
                categoryID = int((row['Catalogue Number'])[:2]) + 1     # extract catID from catNo
                title = row['Title']
                composer = row['Composer']
                arranger = row['Arranger']
                publisher = row['Publisher']
                featuredInstrument = row['Featured Instrument(s)']
                ensembleID = ensembleList.index(row['Ensemble Type'])   # convert ensemble into ensembleID
                parts = row['Parts']
                remarks = row['Remarks']

                sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleID`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (catalogueNo, categoryID, title, composer, arranger, publisher, featuredInstrument, ensembleID, parts, remarks)
                cursor.execute(sql, values)
                dbConn.commit()
                rows += 1
            return rows
        finally:
            dbConn.close()
            print("Connection released")