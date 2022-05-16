from model.DatabasePool import DatabasePool
import pandas as pd

class Music:
    #CREATE
    # INSERT new music
    @classmethod
    def insertMusic(cls, jsonMusic):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleType`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                jsonMusic['catalogueNo'],
                jsonMusic['categoryID'],
                jsonMusic['title'],
                jsonMusic['composer'],
                jsonMusic['arranger'],
                jsonMusic['publisher'],
                jsonMusic['featuredInstrument'],
                jsonMusic['ensembleType'],
                jsonMusic['parts'],
                jsonMusic['remarks']
                ))
            dbConn.commit()
            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released.")

    ##################################################
    # READ
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

    # Print all Music
    @classmethod
    def printAllMusic(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks FROM music ORDER BY catalogueNo'
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
            sql = 'SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks FROM music WHERE categoryID=%s ORDER BY catalogueNo'
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
            sql = 'SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks FROM music WHERE ensembleType=%s ORDER BY catalogueNo'
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
            sql = 'SELECT * FROM music WHERE catalogueNo=%s'
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
            sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE title LIKE concat('%', %s, '%') ORDER BY catalogueNo"
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
            sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE composer LIKE concat('%', %s, '%') OR arranger LIKE concat('%', %s, '%') ORDER BY catalogueNo"
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
            sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE publisher LIKE concat('%', %s, '%') ORDER BY catalogueNo"
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
            sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE featuredInstrument LIKE concat('%', %s, '%') ORDER BY catalogueNo"
            cursor.execute(sql, (substring,))
            music = cursor.fetchall()
            return music
        finally:
            dbConn.close()
            print('Connection released')

    # GET Boxes
    @classmethod
    def getBoxes(cls, catNo):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT catalogueNo FROM music WHERE categoryID=%s ORDER BY catalogueNo"
            cursor.execute(sql, (catNo,))
            catalogueNoList = cursor.fetchall()
            boxList = []
            for num in catalogueNoList:
                boxList.append(num[0][3:])
            return boxList
        finally:
            dbConn.close()
            print('Connection released')

    ##################################################
    # UPDATE
    # EDIT music by CatNo
    @classmethod
    def editMusicByCatNo(cls, catNo, jsonMusic):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "UPDATE `music` SET `title` = %s, `composer` = %s, `arranger` = %s, `publisher` = %s, `featuredInstrument` = %s, `ensembleType` = %s, `parts` = %s, `remarks` = %s WHERE (`catalogueNo` = %s);"
            cursor.execute(sql, (
                jsonMusic['title'],
                jsonMusic['composer'],
                jsonMusic['arranger'],
                jsonMusic['publisher'],
                jsonMusic['featuredInstrument'],
                jsonMusic['ensembleType'],
                jsonMusic['parts'],
                jsonMusic['remarks'],
                catNo
                ))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")

    ##################################################
    # DELETE music by CatNo
    @classmethod
    def deleteMusicByCatNo(cls, catNo):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "DELETE from music WHERE catalogueNo=%s"
            cursor.execute(sql, (catNo,))
            dbConn.commit()
            rows=cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released")



    ##################################################
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
                ensemble = row['Ensemble Type']
                parts = row['Parts']
                remarks = row['Remarks']

                # can we call insertMusic()???
                sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleType`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (catalogueNo, categoryID, title, composer, arranger, publisher, featuredInstrument, ensemble, parts, remarks)
                cursor.execute(sql, values)
                dbConn.commit()
                rows += 1
            return rows
        finally:
            dbConn.close()
            print("Connection released")