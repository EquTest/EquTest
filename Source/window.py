from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from Source.singleton import singleton

from UI.Menu.menu_ui import MenuUI
from UI.Window.window_ui import WindowUI
from UI.RegisterWindow.register_window_ui import RegisterUI
from UI.StudentWindow.student_window_ui import StudentWindowUI
from UI.ProfessorWindow.professor_window_ui import ProfessorWindowUI
from UI.TestUI.test_ui import TestWidget
from UI.TestWindow.question_ui import QuestionWidget
from UI.TestWindow.test_window_ui import TestWindowUI
from UI.StudentStatisticWindow.student_statistic_ui import StatisticUI
from UI.StudentStatisticWindow.statistic_widget_ui import TestStatisticWidget

from Source.containers import Test, Question
from Source.answers import WrongAnswer, RightAnswer
from Source.users import Student, Professor

from Database.database import Database
from Source.constants import PROFESSOR_TYPE, STUDENT_TYPE, LOGO_PATH


class Window(QtWidgets.QMainWindow):
    """Interface for all window-like classes"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._database_ = Database()
        self.__ui__ = WindowUI()

        self.setWindowIcon(QIcon(LOGO_PATH))

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

    def open_account(self) -> None:
        """Used for profiled windows"""
        self.switch_windows(StatisticWindow())


@singleton
class Menu(Window):
    def __init__(self):
        super().__init__()

        self.__ui__ = MenuUI()
        self.__init_UI__()

        self.__login__ = None
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
            Student(self.__login__)
            self.switch_windows(self.__student_window__)
        elif is_professor:
            Professor(self.__login__)
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

        self.__login__ = login

        return (login, password,) in user

    def open_account(self) -> None:
        pass


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
        self.__ui__.account.clicked.connect(self.open_account)

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

    def open_account(self) -> None:
        self.switch_windows(StatisticWindow())


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
        self.__ui__.account.clicked.connect(self.open_account)

        self.__scroll_area__.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__scroll_area__.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area__.setWidgetResizable(True)
        self.__scroll_area__.setWidget(self.__ui__.background)

        self.setCentralWidget(self.__scroll_area__)
        self.setGeometry(320, 180, 1280, 720)

    def __init_tests__(self) -> None:
        tests = self._database_.get_tests()

        for test in tests:
            test_widget = TestWidget(test.get_name(), len(test.get_questions()), TestWindow(test), self)
            test_widget.setFixedSize(580, 300)

            self.__test_windows__.append(test_widget)


class TestWindow(Window):
    def __init__(self, test: Test):
        super().__init__()

        self.__test__ = test
        self.__questions__ = []
        self.__init_questions__()
        self.__ui__ = TestWindowUI()

        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        self.__ui__.setupUi(self)
        self.__ui__.header.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__ui__.header.setFixedSize(1280, 65)

        self.__scroll_area__ = QtWidgets.QScrollArea()
        self.__layout__ = QtWidgets.QVBoxLayout()
        self.__layout__.setSpacing(30)

        for question_widget in self.__questions__:
            self.__layout__.addWidget(question_widget, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.answer_button = QtWidgets.QPushButton()
        self.answer_button.setText("Відповісти")
        self.answer_button.setFixedSize(200, 50)
        self.answer_button.setStyleSheet("border: 2px solid black;\n"
                                         "border-radius: 17px;\n"
                                         "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(198, 198, 198, 255), stop:1 rgba(234, 234, 234, 255));\n"
                                         "\n"
                                         "font-size: 18px;\n"
                                         "font-family: montserrat;\n"
                                         "font-weight: 400;"
                                         "\n"
                                         "padding: 0;")

        self.answer_button.clicked.connect(self.get_result)
        self.__layout__.addWidget(self.answer_button, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.__ui__.background.setLayout(self.__layout__)
        self.__ui__.account.clicked.connect(self.open_account)

        self.__scroll_area__.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__scroll_area__.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area__.setWidgetResizable(True)
        self.__scroll_area__.setWidget(self.__ui__.background)

        self.setCentralWidget(self.__scroll_area__)
        self.setGeometry(320, 180, 1280, 720)

    def get_result(self) -> None:
        right_answers = [question.get_result() for question in self.__questions__].count(1)

        self._database_.add_grade(Student().get_current_student(), self.__test__.get_name(), right_answers)

        self.switch_windows(StudentWindow())

    def __init_questions__(self) -> None:
        questions = self.__test__.get_questions()

        for question in questions:
            right_answer = question.get_right_or_wrong(RightAnswer)[0].get_text()
            wrong_answers = [wrong_answer.get_text() for wrong_answer in question.get_right_or_wrong(WrongAnswer)]

            question_widget = QuestionWidget(question.get_name(), right_answer, wrong_answers)
            question_widget.setFixedSize(1170, 330)

            self.__questions__.append(question_widget)


@singleton
class StatisticWindow(Window):
    def __init__(self):
        super().__init__()

        self.__current_user__ = Student().get_current_student() or Professor().get_current_professor()
        self.__is_professor__ = bool(Professor().get_current_professor())

        self.__ui__ = StatisticUI(self.__is_professor__)

        self.__statistic__ = []
        self.__init_statistic__()
        self.__init_UI__()

    def __init_UI__(self) -> None:
        """Implementation for StudentWindow Class"""
        self.__ui__.setupUi(self)
        self.__ui__.header.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.__ui__.header.setFixedSize(1280, 65)

        self.__scroll_area__ = QtWidgets.QScrollArea()

        self.__layout__ = QtWidgets.QVBoxLayout()
        self.__layout__.setSpacing(30)

        for statistic in self.__statistic__:
            self.__layout__.addWidget(statistic, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.__ui__.background.setLayout(self.__layout__)

        self.__scroll_area__.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.__scroll_area__.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area__.setWidgetResizable(True)
        self.__scroll_area__.setWidget(self.__ui__.background)

        self.setCentralWidget(self.__scroll_area__)
        self.setGeometry(320, 180, 1280, 720)

    def __init_statistic__(self) -> None:
        statistics = self._database_.get_grades(self.__current_user__, self.__is_professor__)

        for statistic in statistics:
            try:
                user, test_name, grade, max_grade = statistic
            except ValueError:
                test_name, grade, max_grade = statistic
                user = None

            statistic_widget = TestStatisticWidget(test_name, grade, max_grade, student_name=user, add_student_names=self.__is_professor__)
            statistic_widget.setFixedSize(1280, 60)

            self.__statistic__.append(statistic_widget)
        