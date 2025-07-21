import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
# from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    # apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    sys.exit(app.exec_())
    # return main

if __name__ == "__main__":
    main()