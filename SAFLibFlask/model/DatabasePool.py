from mysql.connector import pooling
from config.settings import Settings

class DatabasePool:
    # class variable
    connection_pool = pooling.MySQLConnectionPool(
        pool_name = 'ws_pool',
        pool_size = 5,
        host = 'localhost',
        database = Settings.database,
        user = Settings.user,
        password = Settings.password
    )
    
    @classmethod
    def getConnection(cls): #cls = current class
        dbConn = cls.connection_pool.get_connection() # Gets a connection from the connection_pool
        return dbConn