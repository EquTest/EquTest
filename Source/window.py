from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from Source.singleton import singleton

from UI.Menu.menu_ui import MenuUI
from UI.Window.window_ui import WindowUI
from UI.RegisterWindow.register_window_ui import RegisterUI
from UI.StudentWindow.student_window_ui import StudentWindowUI
from UI.ProfessorWindow.professor_window_ui import ProfessorWindowUI
from UI.TestUI.test_ui import TestWidget

from Source.containers import Test, Question
from Source.answers import WrongAnswer, RightAnswer

from Database.database import Database
from Source.constants import PROFESSOR_TYPE, STUDENT_TYPE


class Window(QtWidgets.QMainWindow):
    """Interface for all window-like classes"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._database_ = Database()
        self.__ui__ = WindowUI()

    def __init_UI__(self, *args, **kwargs) -> None:
        """Add the implementation"""
        self.__ui__.setupUi(self)

    def switch_windows(self, another_window: QtWidgets.QMainWindow, hide: bool = True) -> None:
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

        #
        # self._database_.set_sequences_value(True)

    def __init_UI__(self) -> None:
        """Implementation for Menu Class"""
        self.__ui__.setupUi(self)
        self.__student_window__ = StudentWindow()
        self.__professor_window__ = ProfessorWindow(self)
        self.__dialogue__ = RegisterWindow()

        self.__ui__.button.clicked.connect(self._check_enter_data_)

    def _check_enter_data_(self) -> None:
        is_student = self._check_user_(STUDENT_TYPE)
        is_professor = self._check_user_(PROFESSOR_TYPE)

        if is_student:
            self.switch_windows(self.__student_window__)
        elif is_professor:
            self.switch_windows(self.__professor_window__)
        else:
            self.__dialogue__.set_enter_data(*self.get_enter_data())
            self.__dialogue__.show()

        self.__ui__.login_field.setText("")
        self.__ui__.__password_field__.setText("")

    def get_enter_data(self) -> tuple[str, str]:
        return self.__ui__.login_field.text(), self.__ui__.__password_field__.text()

    def _check_user_(self, user_type: str) -> bool:
        user = self._database_.get_users(user_type)
        login, password = self.get_enter_data()

        return (login, password,) in user


@singleton
class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self._database_ = Database()

        self.__login__ = ""
        self.__password__ = ""

        self.__ui__ = RegisterUI()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Add the UI"""
        self.__ui__.setupUi(self)

        self.__ui__.start_button.clicked.connect(self._add_user_)
        self.__ui__.no_button.clicked.connect(self.hide)

    def set_enter_data(self, login: str, password: str) -> None:
        self.__login__ = login
        self.__password__ = password

    def _add_user_(self) -> None:
        """Adding the user to database"""
        self._database_.add_user(self.__login__, self.__password__)

        self.hide()


@singleton
class StudentWindow(Window):
    def __init__(self):
        super().__init__()

        self.__test_windows__ = []
        self.__init_tests__()

        self.__ui__ = StudentWindowUI()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        self.__ui__.setupUi(self)
        self.__ui__.header.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__ui__.header.setFixedSize(1280, 65)

        self.__scroll_area__ = QtWidgets.QScrollArea()

        self.__layout__ = QtWidgets.QGridLayout()
        self.__layout__.setSpacing(30)

        for index, test in enumerate(self.__test_windows__):
            self.__layout__.addWidget(test, index // 2, index % 2)

        self.__ui__.background.setLayout(self.__layout__)

        self.__scroll_area__.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__scroll_area__.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area__.setWidgetResizable(True)
        self.__scroll_area__.setWidget(self.__ui__.background)

        self.setCentralWidget(self.__scroll_area__)
        self.setGeometry(320, 180, 1280, 720)

    def __init_tests__(self) -> None:
        tests = self._database_.get_tests()

        for test in tests:
            test = TestWidget(test.get_name(), len(test.get_questions()), TestWindow(test), self)
            test.setFixedSize(580, 300)

            self.__test_windows__.append(test)


@singleton
class ProfessorWindow(Window):
    def __init__(self, menu: Menu):
        super().__init__()

        self.__ui__ = ProfessorWindowUI()
        self.__init_UI__()

        self.__menu__ = menu

        self.__tests__ = []

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        self.__ui__.setupUi(self)

        self.__ui__.add_question.clicked.connect(self.__add_question__)
        self.__ui__.done.clicked.connect(self.__add_test__)

    def __add_question__(self) -> None:
        test_name = self.__ui__.test_name.text()
        test_index = self.__check_test__(test_name)

        if test_index == -1:
            test = Test(test_name)
            self.__tests__.append(test)
        else:
            test = self.__tests__[test_index]

        question_text = self.__ui__.question.text()

        if not self.__check_question__(question_text, test):
            test.add_question(Question(question_text, [
                WrongAnswer(self.__ui__.wrong_answer_one.text()),
                WrongAnswer(self.__ui__.wrong_answer_two.text()),
                WrongAnswer(self.__ui__.wrong_answer_three.text()),
                RightAnswer(self.__ui__.correct_answer.text()),
            ]))

        self.__clear_fields__()

    def __clear_fields__(self) -> None:
        self.__ui__.wrong_answer_one.setText("")
        self.__ui__.wrong_answer_two.setText("")
        self.__ui__.wrong_answer_three.setText("")
        self.__ui__.correct_answer.setText("")
        self.__ui__.question.setText("")

    def __add_test__(self) -> None:
        self._database_.add_tests(self.__tests__)

        self.__ui__.test_name.setText("")

        self.switch_windows(self.__menu__)

    def __check_test__(self, test_name: str) -> int:
        try:
            return [test.get_name() for test in self.__tests__].index(test_name)
        except ValueError:
            return -1

    @staticmethod
    def __check_question__(question_text: str, test: Test) -> bool:
        return any([question_text == question.get_name() for question in test.get_questions()])


@singleton
class TestWindow(Window):
    def __init__(self, test: Test):
        super().__init__()

        self.__test__ = test

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
