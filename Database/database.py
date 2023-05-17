from typing import Any
from collections import defaultdict

import psycopg2

from Database.database_constants import HOST, DATABASE, PORT, USER, PASSWORD
from Source.constants import PROFESSOR_TYPE, STUDENT_TYPE, TEST_TYPE, QUESTION_TYPE
from Source.containers import Test, Question
from Source.singleton import singleton
from Source.answers import RightAnswer, WrongAnswer


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

        self.__tests__ = []
        self.__tests_data__ = defaultdict(lambda: defaultdict(lambda: (set(), [],)))

        self.__init_tests__()

        print(f"[INFO] Database {DATABASE} successfully connected")

    def __del__(self):
        """Closes the connection when Database is shut"""
        self.__cursor__.close()
        self.__connection__.close()

        print(f"[INFO] Connection to {DATABASE} successfully closed")

    def get_tables(self) -> list[str]:
        self.__cursor__.execute("SELECT table_name FROM inselfation_schema.tables WHERE table_schema = 'public'")

        return [table[0] for table in self.__cursor__.fetchall()]

    def get_users(self, user_type: str) -> tuple[tuple, ...]:
        if user_type not in (PROFESSOR_TYPE, STUDENT_TYPE):
            return ()

        self.__cursor__.execute(
            f"SELECT ({user_type}.{user_type}_name, {user_type}.{user_type}_password) FROM {user_type}")

        return self.__get_return__(self.__cursor__.fetchall())

    def get_containers(self, container_type: str):
        if container_type not in (TEST_TYPE, QUESTION_TYPE):
            return ()

        self.__cursor__.execute(f"SELECT {container_type}.{container_type}_text FROM {container_type}")

        return [container[0] for container in self.__cursor__.fetchall()]

    def get_grades(self, student_name: str, is_professor: bool) -> list[tuple[Any, ...]]:
        if is_professor:
            self.__cursor__.execute("""
                            SELECT student.student_name, test.test_text, grade.test_grade, COUNT(question.question_id) AS question_count
                            FROM test
                            JOIN question ON test.test_id = question.test_id
                            JOIN grade ON test.test_id = grade.test_id
                            JOIN student ON grade.student_id = student.student_id
                            GROUP BY test.test_text, grade.test_grade, student_name
                            ORDER BY student.student_name;
                        """)
        else:
            self.__cursor__.execute("""
                SELECT test.test_text, grade.test_grade, COUNT(question.question_id) AS question_count
                FROM test
                JOIN question ON test.test_id = question.test_id
                JOIN grade ON test.test_id = grade.test_id
                JOIN student ON grade.student_id = student.student_id
                WHERE student.student_name = %s
                GROUP BY test.test_text, grade.test_grade;
            """, (student_name,))

        return self.__cursor__.fetchall()

    def add_user(self, login: str, password: str) -> None:
        self.__cursor__.execute(
            f"INSERT INTO student (student_name, student_password) VALUES ('{login}', '{password}');")
        self.__connection__.commit()
        print("Successfully.")

    def set_sequences_value(self, restart: bool = False) -> None:
        self.__cursor__.execute(
            "SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public'")

        sequences = self.__cursor__.fetchall()
        if restart:
            for sequence in sequences:
                self.__cursor__.execute(f"ALTER SEQUENCE {sequence[0]} RESTART WITH 1")

    def add_tests(self, tests: list[Test]) -> None:
        self.set_sequences_value()

        test_names = set(self.get_containers(TEST_TYPE))
        question_names = set(self.get_containers(QUESTION_TYPE))

        for test in tests:
            if test.get_name() in test_names:
                continue

            self.__cursor__.execute(
                "INSERT INTO test (test_text) VALUES (%s) RETURNING test_id;",
                (test.get_name(),)
            )
            test_id = self.__cursor__.fetchone()[0]

            question_values = []
            answer_values = []

            for question in test.get_questions():
                if question.get_name() in question_names:
                    continue

                self.__cursor__.execute(
                    "INSERT INTO question (question_text, test_id) VALUES (%s, %s) RETURNING question_id;",
                    (question.get_name(), test_id)
                )
                question_id = self.__cursor__.fetchone()[0]

                for answer in question.get_answers():
                    if isinstance(answer, RightAnswer):
                        answer_values.append((answer.get_text(), question_id))
                    elif isinstance(answer, WrongAnswer):
                        question_values.append((answer.get_text(), question_id))

                question_names.add(question.get_name())

            if answer_values:
                self.__cursor__.executemany(
                    "INSERT INTO right_answer (right_answer_text, question_id) VALUES (%s, %s);",
                    answer_values
                )

            if question_values:
                self.__cursor__.executemany(
                    "INSERT INTO wrong_answer (wrong_answer_text, question_id) VALUES (%s, %s);",
                    question_values
                )

            test_names.add(test.get_name())

        self.__connection__.commit()

    def __init_tests_data__(self):
        self.__cursor__.execute("""
                    SELECT test.test_id, test.test_text, question.question_id, question.question_text,
                    right_answer.right_answer_text, wrong_answer.wrong_answer_text
                    FROM test
                    JOIN question ON test.test_id = question.test_id
                    JOIN right_answer ON question.question_id = right_answer.question_id
                    JOIN wrong_answer ON question.question_id = wrong_answer.question_id
                    ORDER BY question.question_id;
                """)

        for row in self.__cursor__:
            test_id, test_text, question_id, question_text, right_answer_text, wrong_answer_text = row

            self.__tests_data__[test_text][question_text][0].add(right_answer_text)
            self.__tests_data__[test_text][question_text][1].append(wrong_answer_text)

    def __init_tests__(self):
        self.__init_tests_data__()

        for test_text, questions in self.__tests_data__.items():
            test = Test(test_text)

            for question_text, answers in questions.items():
                test.add_question(Question(question_text, [
                    RightAnswer(*answers[0]),
                    *[WrongAnswer(text) for text in answers[1]]
                ]))

            self.__tests__.append(test)

    def add_grade(self, student_name: str, test_text: str, grade: int) -> None:
        self.__cursor__.execute("SELECT student.student_id FROM student WHERE student.student_name = %s;",
                                (student_name,))
        student_id = self.__cursor__.fetchone()[0]

        self.__cursor__.execute("SELECT test.test_id FROM test WHERE test.test_text = %s;", (test_text,))
        test_id = self.__cursor__.fetchone()[0]

        self.__cursor__.execute("INSERT INTO grade (student_id, test_grade, test_id) VALUES (%s, %s, %s)",
                                (student_id, grade, test_id))
        self.__connection__.commit()

    def get_tests(self) -> list[Test]:
        return self.__tests__

    @staticmethod
    def __get_return__(fetched: list[tuple[Any, ...]]) -> tuple[tuple, ...]:
        return tuple(tuple(item[0][1:-1].split(',')) for item in fetched)
