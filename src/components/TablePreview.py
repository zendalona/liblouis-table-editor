from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from components.AddEntry.EntryWidget import EntryWidget
from utils.ApplyStyles import apply_styles

class TablePreview(QWidget):
    def __init__(self, table_editor, parent=None):
        super().__init__(parent)
        self.table_editor = table_editor
        self.entries = []
        self.entry_widgets = []  
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
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_area.setWidget(self.scroll_widget)
        
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        
    def update_content(self):
        self.clear_layout()
        self.entry_widgets = []  
        for entry in self.entries:
            entry_widget = EntryWidget(entry, self.table_editor)
            self.entry_widgets.append(entry_widget)  
            self.scroll_layout.addWidget(entry_widget)
            
    def add_entry(self, entry):
        self.entries.append(entry)
        self.update_content()

    def select_entry(self, index):
        if 0 <= index < len(self.entry_widgets):
            for i, widget in enumerate(self.entry_widgets):
                if i == index:
                    widget.setStyleSheet("background-color: #e6f7ff; border: 1px solid #1890ff;")
                else:
                    widget.setStyleSheet("")
            
            self.scroll_area.ensureWidgetVisible(self.entry_widgets[index])
            
            if hasattr(self.table_editor, 'load_entry_into_editor'):
                self.table_editor.load_entry_into_editor(self.entries[index])

    def clear_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
    def update_font_size(self, size):
        """Update the font size for all widgets in the preview."""
        font = QFont()
        font.setPointSize(size)
        
        self.scroll_area.setFont(font)
        
        for widget in self.entry_widgets:
            widget.update_font_size(size)
            
        self.scroll_widget.adjustSize()
        self.scroll_area.updateGeometry()
        self.update()
