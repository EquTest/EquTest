import sys

from PyQt5.QtWidgets import QApplication

from Source.window import Window


def main():
    application = QApplication(sys.argv)
    window = Window()

    window.show()
    application.exec_()

def equ_test():
    print("Hello EquTest!")

if __name__ == "__main__":
    main()
    equ_test()
