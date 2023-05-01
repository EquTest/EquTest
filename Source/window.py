from PyQt5 import QtWidgets


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.__init_UI__()

    def __init_UI__(self):
        """Add the implementation"""
        ...

    def __repr__(self):
        """Place the fields that constructor takes"""
        return f"Window()"
