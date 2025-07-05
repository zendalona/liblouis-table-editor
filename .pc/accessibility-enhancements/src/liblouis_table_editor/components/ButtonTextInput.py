from PyQt5.QtWidgets import *

class ButtonTextInput(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.input = QLineEdit()
        self.button = QPushButton()
        
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)
