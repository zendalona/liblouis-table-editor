from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QMenu, QAction, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EntryWidget(QWidget):
    def __init__(self, entry, table_editor, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.table_editor = table_editor
        self.initUI()

    def initUI(self):
        self.label_text = QLabel(self.entry)
        self.label_text.setWordWrap(False)
        font = self.label_text.font()
        font.setPointSize(9)  
        self.label_text.setFont(font)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label_text, alignment=Qt.AlignVCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)  
        self.layout.setSpacing(0)  
        self.setLayout(self.layout)
        self.setStyleSheet("padding: 10px; background-color: white; margin: 0px")
        self.setMouseTracking(True)
        self.enterEvent = self.onHoverEnter
        self.leaveEvent = self.onHoverLeave
        self.edit_line = QLineEdit(self.entry)
        self.edit_line.setVisible(False)
        self.edit_line.setFont(font)
        self.layout.addWidget(self.edit_line)
        self.edit_line.editingFinished.connect(self.save_entry)
        self.label_text.mousePressEvent = self.load_into_editor

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        duplicate_action = QAction('Duplicate', self)
        duplicate_action.triggered.connect(self.duplicate_entry)
        menu.addAction(duplicate_action)

        edit_action = QAction('Edit', self)
        edit_action.triggered.connect(self.edit_entry)
        menu.addAction(edit_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_entry)
        menu.addAction(delete_action)

        menu.exec_(self.mapToGlobal(event.pos()))

    def duplicate_entry(self):
        new_entry_widget = EntryWidget(self.entry, self.table_editor, parent=self.parentWidget())
        self.parentWidget().layout().insertWidget(self.parentWidget().layout().indexOf(self) + 1, new_entry_widget)

    def edit_entry(self):
        self.label_text.setVisible(False)
        self.edit_line.setVisible(True)
        self.edit_line.setText(self.entry)
        self.edit_line.setFocus()
        self.edit_line.selectAll()

    def save_entry(self):
        self.entry = self.edit_line.text()
        self.label_text.setText(self.entry)
        self.edit_line.setVisible(False)
        self.label_text.setVisible(True)
        self.load_into_editor()

    def delete_entry(self):
        self.setParent(None)
        self.deleteLater()

    def onHoverEnter(self, event):
        self.setStyleSheet("padding: 10px; background-color: #f0f8ff; margin: 0px")

    def onHoverLeave(self, event):
        self.setStyleSheet("padding: 10px; background-color: white; margin: 0px")

    def load_into_editor(self, event=None):
        self.table_editor.load_entry_into_editor(self.entry)

    def update_font_size(self, size):
        font = QFont()
        font.setPointSize(size)
        self.label_text.setFont(font)
        self.edit_line.setFont(font)
        
        base_style = f"padding: 10px; background-color: white; margin: 0px; font-size: {size}pt;"
        self.setStyleSheet(base_style)
        
        self.adjustSize()
        self.updateGeometry()
        self.update()
