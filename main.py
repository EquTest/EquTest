import sys

from PyQt5.QtWidgets import QApplication

from Source.window import Window


def hello_test():
    print('Hello EquTest')


def main():
    application = QApplication(sys.argv)
    window = Window()

    window.show()
    application.exec_()


if __name__ == "__main__":
    main()

