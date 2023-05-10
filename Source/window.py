from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from Source.singleton import singleton
from UI.Menu.menu_ui import MenuUI
from UI.Window.window_ui import WindowUI
from UI.RegisterWindow.register_window_ui import RegisterUI
from Database.database import Database
from Source.constants import PROFESSOR_TYPE, STUDENT_TYPE


class Window(QtWidgets.QMainWindow):
    """Interface for all window-like classes"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__database__ = Database()
        self.__ui__ = WindowUI()

    def __init_UI__(self, *args, **kwargs) -> None:
        """Add the implementation"""
        self.__ui__.setupUi(self)

    def _switch_windows_(self, another_window: QtWidgets.QMainWindow, hide: bool = True) -> None:
        """Hide a current window and replace it by a caller"""

        if hide:
            self.hide()
        another_window.show()

    def __repr__(self) -> str:
        """Place the fields that constructor takes"""

        return f"Window()"


@singleton
class Menu(Window):
    def __init__(self):
        super().__init__()

        self.__ui__ = MenuUI()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for Menu Class"""
        self.__ui__.setupUi(self)
        self.__student_window__ = StudentWindow()
        self.__professor_window__ = ProfessorWindow()
        self.__dialogue__ = RegisterWindow()

        self.__ui__.__button__.clicked.connect(self._check_enter_data_)

    def _check_enter_data_(self) -> None:
        is_student = self._check_user_(STUDENT_TYPE)
        is_professor = self._check_user_(PROFESSOR_TYPE)

        print(is_student, is_professor)

        if is_student:
            self._switch_windows_(self.__student_window__, False)  # change hide to True
        elif is_professor:
            self._switch_windows_(self.__professor_window__, False)  # change hide to True
        else:
            self.__dialogue__.show()

    def _check_user_(self, user_type: str) -> bool:
        user = self.__database__.get_users(user_type)
        login, password = self.__ui__.__login_field__.text(), self.__ui__.__password_field__.text()

        return (login, password,) in user


@singleton
class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.__ui__ = RegisterUI()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Add the UI"""
        self.__ui__.setupUi(self)

    def _add_user_(self) -> None:
        """Adding the user to database"""
        ...


@singleton
class StudentWindow(Window):
    def __init__(self):
        super().__init__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...


@singleton
class ProfessorWindow(Window):
    def __init__(self):
        super().__init__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...


@singleton
class AddTestWindow(Window):
    def __init__(self):
        super().__init__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...


@singleton
class StudentStatisticWindow(Window):
    def __init__(self):
        super().__init__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        ...
