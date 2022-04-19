import mysql.connector

class DatabasePool:

    def getConnection():
        connection = mysql.connector.connect(
            host = 'elitelib22.mysql.pythonanywhere-services.com',
            database = 'elitelib22$test', # connection to test for testing
            user = 'elitelib22',
            password = 'librarydb'
            )

        cursor = connection.cursor(buffered=True)
        return connection, cursor