from typing import Any

from Source.answers import RightAnswer, WrongAnswer


class Container:
    def __init__(self, object_name: str, _items_: list[Any] = None):
        if _items_ is None:
            _items_ = []

        self._name_ = object_name
        self._items_ = _items_

    def add_item(self, item) -> None:
        """Add the test to tests list if test not there already"""

        if item not in self._items_:
            self._items_.append(item)

    def get_name(self) -> str:
        return self._name_

    def __repr__(self) -> str:
        return f"{self.__class__}(_name_: {self._name_}, _items_: {self._items_})"


class Question(Container):
    def __init__(self, question_name: str, answers_list: list[RightAnswer | WrongAnswer] = None):

        super().__init__(question_name, answers_list)

    def add_answer(self, answers: RightAnswer | WrongAnswer) -> None:
        """Add the question to questions list if question not already there"""
        self.add_item(answers)

    def get_answers(self) -> list[RightAnswer | WrongAnswer]:
        return self._items_

    def get_right_or_wrong(self, right_or_wrong: RightAnswer | WrongAnswer) -> list[RightAnswer | WrongAnswer]:
        return [answer for answer in self._items_ if isinstance(answer, right_or_wrong)]


class Test(Container):
    def __init__(self, test_name: str, questions_list: list[Question] = None):
        super().__init__(test_name, questions_list)

    def add_question(self, question: Question) -> None:
        """Add the question to questions list if question not already there"""
        self.add_item(question)

    def get_questions(self) -> list[Question]:
        return self._items_


class Theme(Container):
    def __init__(self, theme_name: str, tests_list: list[Test] = None):
        super().__init__(theme_name, tests_list)

    def add_test(self, test: Test) -> None:
        """Add the test to test list if test not already there"""
        self.add_item(test)

    def get_tests(self) -> list[Test]:
        return self._items_
