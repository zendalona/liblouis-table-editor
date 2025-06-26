from PyQt5.QtWidgets import QListWidgetItem, QPushButton, QVBoxLayout, QWidget


class ButtonListItem(QListWidgetItem):
    def __init__(self, text, button_text, parent=None):
        super(ButtonListItem, self).__init__(parent)
        
        layout = QVBoxLayout()

        self.widget = QWidget()
        self.button = QPushButton(button_text)
        
        layout.addWidget(self.button)
        self.widget.setLayout(layout)
        self.setSizeHint(self.widget.sizeHint())

    def add_listener(self, event, action):
        if event == "click":
            self.button.clicked.connect(action)
