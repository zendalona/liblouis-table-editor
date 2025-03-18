from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from components.AddEntry.EntryWidget import EntryWidget
from utils.ApplyStyles import apply_styles

class TablePreview(QWidget):
    def __init__(self, table_editor, parent=None):
        super().__init__(parent)
        self.table_editor = table_editor
        self.entries = []
        apply_styles(self)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white; border-bottom: 1px solid #b0c6cf;")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        #self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_area.setWidget(self.scroll_widget)
        
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        
    def update_content(self):
        self.clear_layout()
        for entry in self.entries:
            entry_widget = EntryWidget(entry, self.table_editor)
            self.scroll_layout.addWidget(entry_widget)
            
    def add_entry(self, entry):
        self.entries.append(entry)
        self.update_content()


    def clear_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
