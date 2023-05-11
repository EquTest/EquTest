from typing import Any

from Source.singleton import singleton
from Database.database_constants import HOST, DATABASE, PORT, USER, PASSWORD
from Source.constants import PROFESSOR_TYPE, STUDENT_TYPE

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

        print(f"[INFO] Database {DATABASE} successfully connected")

        self.__tables__ = self.get_tables()

    def __del__(self):
        """Closes the connection when Database is shut"""
        self.__cursor__.close()
        self.__connection__.close()

        print(f"[INFO] Connection to {DATABASE} successfully closed")

    def get_tables(self) -> list[str]:
        self.__cursor__.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        return [table[0] for table in self.__cursor__.fetchall()]

    def get_users(self, user_type: str) -> tuple[tuple, ...]:
        if user_type not in (PROFESSOR_TYPE, STUDENT_TYPE):
            return ()

        self.__cursor__.execute(f"SELECT ({user_type}.{user_type}_name, {user_type}.{user_type}_password) FROM {user_type}")

        return self.__get_return__(self.__cursor__.fetchall())

    def add_user(self, login: str, password: str) -> None:
        print(f"INSERT INTO student (student_name, student_password) VALUES ('{login}', '{password}');")
        self.__cursor__.execute(f"INSERT INTO student (student_name, student_password) VALUES ('{login}', '{password}');")
        self.__connection__.commit()
        print("Successfully.")

    @staticmethod
    def __get_return__(fetched: list[tuple[Any, ...]]) -> tuple[tuple, ...]:
        return tuple(tuple(item[0][1:-1].split(',')) for item in fetched)
