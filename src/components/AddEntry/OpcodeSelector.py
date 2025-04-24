import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from utils.ApplyStyles import apply_styles

data = json.load(open('./src/assets/data/opcodes.json', 'r'))
opcodes = data["codes"]

class OpcodeSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Opcode Selection Tool')
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search for Opcode (hover for details)")
        self.search.textChanged.connect(self.filter_list)

        label = QLabel("Double click opcode to select")

        self.list = QListWidget()
        self.list.setMouseTracking(True)
        self.list.installEventFilter(self)

        self.description_label = QLabel("")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("QLabel { margin-top: 10px; }")

        layout.addWidget(self.search)
        layout.addWidget(label)
        layout.addWidget(self.list)
        layout.addWidget(self.description_label)

        self.populate_list()

        self.setLayout(layout)
        apply_styles(self)

    def populate_list(self):
        self.list.clear()
        for i, opcode in enumerate(opcodes):
            item = QListWidgetItem(f"{i}. {opcode['code']}")
            item.setToolTip(opcode["description"])
            self.list.addItem(item)

    def filter_list(self):
        query = self.search.text().lower()
        self.list.clear()
        for i, opcode in enumerate(opcodes):
            if query in opcode['code'].lower() or query in opcode['description'].lower():
                item = QListWidgetItem(f"{i}. {opcode['code']}")
                item.setToolTip(opcode["description"])
                self.list.addItem(item)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove and source == self.list:
            item = self.list.itemAt(event.pos())
            if item:
                self.display_description(item)
        return super().eventFilter(source, event)

    def display_description(self, item):
        index = int(item.text().split('.')[0])
        self.description_label.setText(opcodes[index]['description'])

    def on_select(self, cb):
        def callback(code):
            cb(code)
            self.hide()
        self.list.itemDoubleClicked.connect(lambda x: callback(opcodes[int(x.text().split('.')[0])]))

