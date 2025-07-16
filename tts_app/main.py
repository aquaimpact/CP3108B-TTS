import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # return main

if __name__ == "__main__":
    main()