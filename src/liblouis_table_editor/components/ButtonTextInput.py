from PyQt5.QtWidgets import *

class ButtonTextInput(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.input = QLineEdit()
        self.input.setAccessibleName("Button Text Input Field")
        self.button = QPushButton()
        self.button.setAccessibleName("Button Text Input Button")
        
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)
