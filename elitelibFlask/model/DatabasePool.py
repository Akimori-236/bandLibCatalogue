import sqlalchemy.pool as pool
import psycopg2

class DatabasePool:

    def getconn():
        c = psycopg2.connect(
            user='elitelib22',
            password = 'librarydb',
            host='elitelib22.mysql.pythonanywhere-services.com',
            dbname='elitelib22$libcatalogue'
            )
        return c

    mypool = pool.QueuePool(getconn, max_overflow=2, pool_size=1)

    @classmethod
    def getConnection(cls):
        dbConn = cls.mypool.connect()
        return dbConn
