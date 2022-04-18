from model.DatabasePool import DatabasePool

class Category:

    # GET all Categories
    @classmethod
    def getAllCategory(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'SELECT * FROM category'
            cursor.execute(sql)
            allCategories = cursor.fetchall()
            return allCategories
        finally:
            dbConn.close()
            print('Connection released')



    # INSERT new category
    @classmethod
    def insertCategory(cls, jsonCategory):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "INSERT INTO category(name, description) VALUES (%s, %s)"
            cursor.execute(sql,(jsonCategory['name'], jsonCategory['description']))
            dbConn.commit()
            rows = cursor.rowcount
            return rows
        finally:
            dbConn.close()
            print("Connection released.")