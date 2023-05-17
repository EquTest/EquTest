from Source.singleton import singleton


class User:
    def __init__(self, name: str):
        self._name_ = name

    def __repr__(self) -> str:
        return f"{self.__class__}(_name_: {self._name_})"

    def get_current_user(self) -> str:
        return self._name_


@singleton
class Student(User):
    def __init__(self, name: str = None):
        super().__init__(name)

        self.__current_student__ = name

    def get_current_student(self) -> str:
        return self.__current_student__


@singleton
class Professor(User):
    def __init__(self, name: str = None):
        super().__init__(name)

        self.__current_professor__ = name

    def get_current_professor(self) -> str:
        return self.__current_professor__
