class User:
    def __init__(self, name: str):
        self._name_ = name

    def __repr__(self) -> str:
        return f"{self.__class__}(_name_: {self._name_})"


class Student(User):
    def __init__(self, name):
        super().__init__(name)

        """Add the implementation"""


class Professor(User):
    def __init__(self, name):
        super().__init__(name)

        """Add the implementation"""
