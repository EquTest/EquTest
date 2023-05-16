# -*- coding: utf-8 -*-
import random

# Form implementation generated from reading ui file 'question_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class QuestionWidget(QtWidgets.QWidget):
    def __init__(self, question_text: str, right_answer: str, wrong_answers: list[str]):
        super().__init__()

        self.__question_text__ = question_text
        self.__right_answer__ = right_answer
        self.__wrong_answers__ = wrong_answers

        self.__answers__ = self.__wrong_answers__ + [self.__right_answer__]

        self.setupUi()

    def setupUi(self):
        self.resize(1170, 330)
        self.background = QtWidgets.QFrame(self)
        self.background.setGeometry(QtCore.QRect(0, 0, 1170, 330))
        self.background.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(225, 112, 111, 255), stop:1 rgba(195, 96, 96, 255));\n"
            "\n"
            "border-radius: 20px;\n"
            "border: 2px solid black;\n"
            "\n"
            "font-size: 14px;\n"
            "")
        self.background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.background.setObjectName("background")
        self.question = QtWidgets.QLabel(self.background)
        self.question.setGeometry(QtCore.QRect(35, 30, 1170, 31))
        self.question.setStyleSheet("background: transparent;\n"
                                    "border: 0;\n"
                                    "\n"
                                    "font-size: 18px;\n"
                                    "font-family: montserrat;\n"
                                    "font-weight: 500;")
        self.question.setObjectName("question")
        self.buttons = QtWidgets.QButtonGroup()
        self.first_answer = QtWidgets.QRadioButton(self.background)
        self.first_answer.setGeometry(QtCore.QRect(60, 90, 811, 31))
        self.first_answer.setStyleSheet("background: transparent;\n"
                                        "border: 0;\n"
                                        "")
        self.first_answer.setIconSize(QtCore.QSize(30, 30))
        self.first_answer.setObjectName("first_answer")
        self.second_answer = QtWidgets.QRadioButton(self.background)
        self.second_answer.setGeometry(QtCore.QRect(60, 140, 811, 31))
        self.second_answer.setStyleSheet("background: transparent;\n"
                                         "border: 0;\n"
                                         "")
        self.second_answer.setIconSize(QtCore.QSize(30, 30))
        self.second_answer.setObjectName("second_answer")
        self.third_answer = QtWidgets.QRadioButton(self.background)
        self.third_answer.setGeometry(QtCore.QRect(60, 190, 811, 31))
        self.third_answer.setStyleSheet("background: transparent;\n"
                                        "border: 0;\n"
                                        "")
        self.third_answer.setIconSize(QtCore.QSize(30, 30))
        self.third_answer.setObjectName("third_answer")
        self.fourth_answer = QtWidgets.QRadioButton(self.background)
        self.fourth_answer.setGeometry(QtCore.QRect(60, 240, 811, 31))
        self.fourth_answer.setStyleSheet("background: transparent;\n"
                                         "border: 0;\n"
                                         "")
        self.fourth_answer.setIconSize(QtCore.QSize(30, 30))
        self.fourth_answer.setObjectName("fourth_answer")

        self.buttons.addButton(self.first_answer)
        self.buttons.addButton(self.second_answer)
        self.buttons.addButton(self.third_answer)
        self.buttons.addButton(self.fourth_answer)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def get_result(self) -> int:
        checked = self.buttons.checkedButton()
        return int(checked.text() == self.__right_answer__) if checked else 0

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "EquTest"))
        self.question.setText(_translate("self", f"{self.__question_text__}"))

        answers = random.sample(self.__answers__, 4)
        radio_buttons = [self.first_answer, self.second_answer, self.third_answer, self.fourth_answer]

        for index, button in enumerate(radio_buttons):
            button.setText(_translate("self", answers[index]))
