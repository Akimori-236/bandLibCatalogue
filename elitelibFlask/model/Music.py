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


    # Wipe out current table and create new with CSV data
    @classmethod
    def DBReset(cls, filePath):
        rows = 0
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            
            # Wipe out current Table
            sql = "DROP TABLE music;"
            cursor.execute(sql)
            dbConn.commit()
            # Make new Table
            sql = "CREATE TABLE `music` (`musicID` INT NOT NULL AUTO_INCREMENT, `catalogueNo` VARCHAR(45) NOT NULL, `categoryID` INT NOT NULL , `title` VARCHAR(255) NOT NULL, `composer` VARCHAR(255) NULL, `arranger` VARCHAR(255) NULL, `publisher` VARCHAR(255) NULL, `featuredInstrument` VARCHAR(255) NULL, `ensembleID` INT NULL, `parts` VARCHAR(255) NULL, `remarks` VARCHAR(255) NULL, PRIMARY KEY (`musicID`), UNIQUE INDEX `catalogueNo_UNIQUE` (`catalogueNo` ASC));"
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