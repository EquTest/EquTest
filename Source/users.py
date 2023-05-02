class User:
    def __init__(self, name: str):
        self._name_ = name


class Student(User):
    def __init__(self, name):
        super().__init__(name)

        """Add the implementation"""


class Professor(User):
    def __init__(self, name):
        super().__init__(name)

        """Add the implementation"""
