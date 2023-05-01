from PyQt5 import QtWidgets


def singleton(cls):
    """Give an ability to creation singleton classes"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class Window(QtWidgets.QMainWindow):
    """Interface for all window-like classes"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.__init_UI__()

    def __init_UI__(self, *args, **kwargs) -> None:
        """Add the implementation"""
        ...

    def _switch_windows_(self, another_window: QtWidgets.QMainWindow, *args, **kwargs) -> None:
        """Hide a current window and replace it by a caller"""

        self.hide()
        another_window.show()

    def __repr__(self) -> str:
        """Place the fields that constructor takes"""

        return f"Window()"


@singleton
class Menu(Window):
    def __init__(self):
        super().__init__()

        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for Menu Class"""
        ...


@singleton
class StudentWindow(Window):
    def __init__(self):
        super().__init__()

        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...


@singleton
class ProfessorWindow(Window):
    def __init__(self):
        super().__init__()

        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...
