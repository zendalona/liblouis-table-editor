from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt
from utils.ApplyStyles import apply_styles

class BrailleInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)

        self.braille_input = QLineEdit()
        self.braille_input.setPlaceholderText("Enter Braille Dots (e.g., 12-34-56)")
        
        braille_regex = QRegExp("^(?:1?2?3?4?5?6?)(?:-(?:1?2?3?4?5?6?))*$")
        validator = QRegExpValidator(braille_regex, self.braille_input)
        self.braille_input.setValidator(validator)
        
        self.braille_input.textChanged.connect(self.updateBraillePreview)
        self.layout.addWidget(self.braille_input)

        self.braille_preview_container = QHBoxLayout()
        self.layout.addLayout(self.braille_preview_container)

        self.setLayout(self.layout)

        apply_styles(self)

    def updateBraillePreview(self):
        text = self.braille_input.text()
        clearLayout(self.braille_preview_container)

        braille_sequences = text.split('-')
        for sequence in braille_sequences:
            if self.is_valid_braille_sequence(sequence):
                preview_label = QLabel(self.get_braille_representation(sequence))
                preview_label.setAlignment(Qt.AlignCenter)
                self.braille_preview_container.addWidget(preview_label)

    def is_valid_braille_sequence(self, sequence):
        return all(digit in '123456' for digit in sequence) and len(set(sequence)) == len(sequence)

    def get_braille_representation(self, sequence):
        braille_representation = [['○', '○'], ['○', '○'], ['○', '○']]
        if '1' in sequence:
            braille_representation[0][0] = '●'
        if '2' in sequence:
            braille_representation[1][0] = '●'
        if '3' in sequence:
            braille_representation[2][0] = '●'
        if '4' in sequence:
            braille_representation[0][1] = '●'
        if '5' in sequence:
            braille_representation[1][1] = '●'
        if '6' in sequence:
            braille_representation[2][1] = '●'

        return (f"{braille_representation[0][0]} {braille_representation[0][1]}\n"
                f"{braille_representation[1][0]} {braille_representation[1][1]}\n"
                f"{braille_representation[2][0]} {braille_representation[2][1]}")

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
