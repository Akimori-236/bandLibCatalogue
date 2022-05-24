from model.DatabasePool import DatabasePool

# Data Cleaner?
def clean(x):
    x = x.strip()
    if x == '-':
        x = ''
    x = x.replace(',', ';')
    return x



class Music:
    #CREATE
    # INSERT new music
    @classmethod
    def insertMusic(cls, jsonMusic):
        # clean values of commas, prevent csv problems
        catalogueNo = clean(jsonMusic['catalogueNo'])
        categoryID = clean(jsonMusic['categoryID'])
        title = clean(jsonMusic['title'])
        composer = clean(jsonMusic['composer'])
        arranger = clean(jsonMusic['arranger'])
        publisher = clean(jsonMusic['publisher'])
        feat = clean(jsonMusic['featuredInstrument'])
        ensemble = clean(jsonMusic['ensembleType'])
        parts = clean(jsonMusic['parts'])
        remarks = clean(jsonMusic['remarks'])

        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleType`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
                catalogueNo,
                categoryID,
                title,
                composer,
                arranger,
                publisher,
                feat,
                ensemble,
                parts,
                remarks
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


    #GET list of ensemble types
    @classmethod
    def getEnsembleTypes(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = 'SELECT DISTINCT ensembleType FROM music'
            cursor.execute(sql)
            ensembleTypes = cursor.fetchall()
            return ensembleTypes
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



    # SEARCH music
    @classmethod
    def searchMusic(cls, searchType, query):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            if searchType=='title':
                sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE title LIKE concat('%', %s, '%') ORDER BY catalogueNo"
                cursor.execute(sql, (query,))
            elif searchType=='comparr':
                sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE composer LIKE concat('%', %s, '%') OR arranger LIKE concat('%', %s, '%') ORDER BY catalogueNo"
                cursor.execute(sql, (query, query))
            elif searchType=='publisher':
                sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE publisher LIKE concat('%', %s, '%') ORDER BY catalogueNo"
                cursor.execute(sql, (query,))
            elif searchType=='feat':
                sql = "SELECT catalogueNo, title, composer, arranger, publisher, featuredInstrument, ensembleType, parts, remarks from music WHERE featuredInstrument LIKE concat('%', %s, '%') ORDER BY catalogueNo"
                cursor.execute(sql, (query,))
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

    # Search similar pieces from same composer
    @classmethod
    def searchSimilarMusic(cls, composer, title):
        title = title.split()
        determiners = ['a','an','the','this','that','these','those','my','your','his','her','its','our','their']
        keywords = ""
        # take out common words
        for i in title:
            if i not in determiners:
                keywords += i

        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "SELECT catalogueNo, title FROM music WHERE composer=%s AND MATCH(title) AGAINST(%s)"
            cursor.execute(sql, (composer, keywords))
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
        # clean values of commas, prevent csv problems
        title = clean(jsonMusic['title'])
        composer = clean(jsonMusic['composer'])
        arranger = clean(jsonMusic['arranger'])
        publisher = clean(jsonMusic['publisher'])
        feat = clean(jsonMusic['featuredInstrument'])
        ensemble = clean(jsonMusic['ensembleType'])
        parts = clean(jsonMusic['parts'])
        remarks = clean(jsonMusic['remarks'])

        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)
            sql = "UPDATE `music` SET `title` = %s, `composer` = %s, `arranger` = %s, `publisher` = %s, `featuredInstrument` = %s, `ensembleType` = %s, `parts` = %s, `remarks` = %s WHERE (`catalogueNo` = %s);"
            cursor.execute(sql, (
                title,
                composer,
                arranger,
                publisher,
                feat,
                ensemble,
                parts,
                remarks,
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
    def resetDB(cls, data):
        # print(data)
        rowcounter = 0
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)

            # Wipe out current Table
            sql = "TRUNCATE TABLE music;"
            cursor.execute(sql)
            dbConn.commit()

            # Loop through the Rows
            for i in range(1,len(data)): # skip header
                rows = data[i].split(',')
                # Data pts
                catalogueNo = rows[0]
                categoryID = (rows[0])[:2]           # extract catID from catNo
                title = rows[1]
                composer = rows[2]
                arranger = rows[3]
                publisher = rows[4]
                feat = rows[5]
                ensemble = rows[6]
                parts = rows[7]
                remarks = rows[8].strip('\n')
                # clean data pts
                catalogueNo = clean(catalogueNo)
                categoryID = clean(categoryID)
                composer = clean(composer)
                arranger = clean(arranger)
                publisher = clean(publisher)
                feat = clean(feat)
                ensemble = clean(ensemble)
                parts = clean(parts)
                remarks = clean(remarks)
                # INSERT ENTRY
                sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleType`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (catalogueNo, categoryID, title, composer, arranger, publisher, feat, ensemble, parts, remarks)
                # print(values)
                cursor.execute(sql, values)
                dbConn.commit()
                rowcounter += 1
            # RETURN no of successful entries
            return rowcounter
        finally:
            dbConn.close()
            print("Connection released")


    # Bulk entry by CSV file
    @classmethod
    def bulkEntry(cls, data):
        # print(data)
        rowcounter = 0
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(buffered=True)

            # Loop through the Rows
            for i in range(1,len(data)): # skip header
                rows = data[i].split(',')
                # Data pts
                catalogueNo = rows[0]
                categoryID = (rows[0])[:2]           # extract catID from catNo
                title = rows[1]
                composer = rows[2]
                arranger = rows[3]
                publisher = rows[4]
                feat = rows[5]
                ensemble = rows[6]
                parts = rows[7]
                remarks = rows[8].strip('\n')
                # clean data pts
                catalogueNo = clean(catalogueNo)
                categoryID = clean(categoryID)
                composer = clean(composer)
                arranger = clean(arranger)
                publisher = clean(publisher)
                feat = clean(feat)
                ensemble = clean(ensemble)
                parts = clean(parts)
                remarks = clean(remarks)
                # INSERT ENTRY
                sql = "INSERT INTO `music` (`catalogueNo`, `categoryID`, `title`, `composer`, `arranger`, `publisher`, `featuredInstrument`, `ensembleType`, `parts`, `remarks`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (catalogueNo, categoryID, title, composer, arranger, publisher, feat, ensemble, parts, remarks)
                # print(values)
                cursor.execute(sql, values)
                dbConn.commit()
                rowcounter += 1
            # RETURN no of successful entries
            return rowcounter
        finally:
            dbConn.close()
            print("Connection released")