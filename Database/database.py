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

        print(f"Database {DATABASE} successfully connected")

        self.__tables__ = self.get_tables()

        self.__cursor__.close()
        self.__connection__.close()

        print(f"Connection to {DATABASE} successfully closed")

    def get_tables(self):
        self.__cursor__.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        return [table[0] for table in self.__cursor__.fetchall()]
