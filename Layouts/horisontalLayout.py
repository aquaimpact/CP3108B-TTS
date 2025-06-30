from PyQt5.QtWidgets import QLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout

class Horisontal(QWidget):
    def __init__(self, label_Text, hasComboBox=False, comboBoxItems=None, hasLineEdit=False, hasSearch=False, searchName=""):
        super().__init__()
        widget = QHBoxLayout()
        widget.addWidget(QLabel(label_Text))
        if(hasLineEdit):
            widget.addWidget(QLineEdit())
        if(hasComboBox):
            comboBox = QComboBox()
            comboBox.addItems(comboBoxItems if comboBoxItems else [])
            widget.addWidget(comboBox)
        if(hasSearch):
            widget.addWidget(QPushButton(searchName))
        