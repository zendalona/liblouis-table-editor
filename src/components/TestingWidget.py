# TestingWidget.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class TestingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.forward_translation_input = QLineEdit(self)
        self.forward_translation_input.setPlaceholderText("Forward Translation")
        layout.addWidget(self.forward_translation_input)

        self.backward_translation_input = QLineEdit(self)
        self.backward_translation_input.setPlaceholderText("Backward Translation")
        layout.addWidget(self.backward_translation_input)

        self.translate_button = QPushButton("Translate", self)
        layout.addWidget(self.translate_button)

        self.setLayout(layout)
