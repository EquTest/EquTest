# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class MenuUI(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setStyleSheet("")
        self.__central__ = QtWidgets.QWidget(MainWindow)
        self.__central__.setObjectName("__central__")
        self.background = QtWidgets.QFrame(self.__central__)
        self.background.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.background.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(198, 198, 198, 255), stop:1 rgba(234, 234, 234, 255));")
        self.background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.background.setObjectName("background")
        self.__login_background__ = QtWidgets.QFrame(self.background)
        self.__login_background__.setGeometry(QtCore.QRect(320, 290, 640, 430))
        self.__login_background__.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(225, 112, 111, 255), stop:1 rgba(195, 96, 96, 255));\n"
            "border-top-left-radius: 30px;\n"
            "border-top-right-radius: 30px;\n"
            "border: 2px solid black;\n"
            "border-bottom: 0;")
        self.__login_background__.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__login_background__.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__login_background__.setObjectName("__login_background__")
        self.__title__ = QtWidgets.QLabel(self.__login_background__)
        self.__title__.setGeometry(QtCore.QRect(220, 50, 211, 35))
        self.__title__.setStyleSheet("background: transparent;\n"
                                     "border: 0;\n"
                                     "\n"
                                     "font-size: 24px;\n"
                                     "font-family: montserrat;\n"
                                     "font-weight: 500;")
        self.__title__.setObjectName("__title__")
        self.login_field = QtWidgets.QLineEdit(self.__login_background__)
        self.login_field.setGeometry(QtCore.QRect(190, 175, 270, 50))
        self.login_field.setStyleSheet("border: 2px solid black;\n"
                                       "border-radius: 17px;\n"
                                       "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(198, 198, 198, 255), stop:1 rgba(234, 234, 234, 255));\n"
                                       "\n"
                                       "padding: 5px;")
        self.login_field.setObjectName("login_field")
        self.__password_field__ = QtWidgets.QLineEdit(self.__login_background__)
        self.__password_field__.setGeometry(QtCore.QRect(190, 245, 270, 50))
        self.__password_field__.setStyleSheet("border: 2px solid black;\n"
                                              "border-radius: 17px;\n"
                                              "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(198, 198, 198, 255), stop:1 rgba(234, 234, 234, 255));\n"
                                              "\n"
                                              "padding: 5px;")
        self.__password_field__.setObjectName("__password_field__")
        self.button = QtWidgets.QPushButton(self.__login_background__)
        self.button.setGeometry(QtCore.QRect(220, 340, 200, 50))
        self.button.setStyleSheet("border: 2px solid black;\n"
                                  "border-radius: 17px;\n"
                                  "background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(198, 198, 198, 255), stop:1 rgba(234, 234, 234, 255));\n"
                                  "\n"
                                  "font-size: 18px;\n"
                                  "font-family: montserrat;\n"
                                  "font-weight: 400;")
        self.button.setObjectName("button")
        MainWindow.setCentralWidget(self.__central__)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EquTest"))
        self.__title__.setText(_translate("MainWindow", "Login to EquTest"))
        self.button.setText(_translate("MainWindow", "Login"))
