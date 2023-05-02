class Answer:
    def __init__(self, text: str):
        """Add the implementation"""

        self._text_ = text

    def get_text(self) -> str:
        return self._text_

    def __repr__(self) -> str:
        return f"{self.__class__}(_text_: {self._text_})"


class RightAnswer(Answer):
    def __init__(self, text: str):
        super().__init__(text)

        """Add the implementation"""
        ...


class WrongAnswer(Answer):
    def __init__(self, text: str):
        super().__init__(text)

        """Add the implementation"""
        ...
