from Source.window import singleton
from Database.database_constants import HOST, DATABASE, PORT, USER, PASSWORD

import psycopg2


@singleton
class Database:
    def __init__(self):
        """Class representation of database"""
        self.__connection__ = psycopg2.connect(
            host=HOST,
            dbname=DATABASE,
            port=PORT,
            user=USER,
            password=PASSWORD,
        )
        self.__cursor__ = self.__connection__.cursor()

        self.__cursor__.close()
        self.__connection__.close()
