import sys

from PyQt5.QtWidgets import QApplication

from Source.window import Menu


from Database.database import Database


def main():
    application = QApplication(sys.argv)
    window = Menu()

    window.show()
    application.exec_()


if __name__ == "__main__":
    main()
