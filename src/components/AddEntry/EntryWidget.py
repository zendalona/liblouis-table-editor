from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QMenu, QAction, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class EntryWidget(QWidget):
    def __init__(self, entry, table_editor, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.table_editor = table_editor
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus) 

    def convert_unicode(self, hex_str):
        try:
            hex_str = hex_str.replace('\\x', '')
            hex_codes = [hex_str[i:i+4] for i in range(0, len(hex_str), 4)]
            result = ''
            for code in hex_codes:
                if code:
                    char_code = int(code, 16)
                    char = chr(char_code)
                    result += char
            return result
        except Exception as e:
            print(f"Error converting {hex_str}: {e}")
            return ''

    def initUI(self):
        self.layout = QHBoxLayout(self)
        
        display_text = self.entry
        parts = self.entry.split()
        if len(parts) >= 2:  
            opcode = parts[0]
            unicode_part = parts[1]
            
            if unicode_part.startswith('\\x'):
                unicode_chars = self.convert_unicode(unicode_part)
                if unicode_chars:
                    remaining_parts = parts[2:] if len(parts) > 2 else []
                    
                    dots_part = []
                    comment_part = []
                    
                    for part in remaining_parts:
                        if part.startswith('#'):
                            comment_idx = remaining_parts.index(part)
                            comment_part = remaining_parts[comment_idx:]
                            dots_part = remaining_parts[:comment_idx]
                            break
                        else:
                            dots_part = remaining_parts
                    
                    display_text = f"{opcode}  {unicode_chars}  {unicode_part}"
                    
                    if dots_part:
                        display_text += f"  {' '.join(dots_part)}"
                    
                    if comment_part:
                        display_text += f"  {' '.join(comment_part)}"
                
        self.label_text = QLabel(display_text)
        self.label_text.setWordWrap(False)
        
        font = QFont()
        font.setPointSize(9)
        font_families = ["Arial Unicode MS", "Nirmala UI", "Mangal", "Arial", "Segoe UI"]
        for family in font_families:
            if family in QFont().families():
                font.setFamily(family)
                break
        
        font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferDefault)
        self.label_text.setFont(font)
        
        self.label_text.setTextFormat(Qt.PlainText)
        
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.type() == event.MouseButtonDblClick:
                event.accept()
                return
            self.load_into_editor()
        elif event.button() == Qt.RightButton:
            self.contextMenuEvent(event)

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
        if not self.property("selected"):
            self.setStyleSheet("padding: 10px; background-color: #f0f8ff; margin: 0px")

    def onHoverLeave(self, event):
        if not self.property("selected"):
            self.setStyleSheet("padding: 10px; background-color: white; margin: 0px")

    def load_into_editor(self, event=None):
        self.table_editor.load_entry_into_editor(self.entry)

    def update_font_size(self, size):
        font = QFont()
        font.setPointSize(size)
        self.label_text.setFont(font)
        self.edit_line.setFont(font)
        
        selected = self.property("selected")
        base_style = """
            QWidget {
                padding: 8px;
                margin: 0px;
                background-color: %s;
                border: %s;
                font-size: %spt;
            }
        """ % (
            "#e6f7ff" if selected else "white",
            "1px solid #1890ff" if selected else "none",
            size
        )
        self.setStyleSheet(base_style)
        
        self.adjustSize()
        self.updateGeometry()
        self.update()

    def setSelected(self, selected):
        self.setProperty("selected", selected)
        base_style = """
            QWidget {
                padding: 8px;
                margin: 0px;
                background-color: %s;
                border: %s;
            }
        """ % (
            "#e6f7ff" if selected else "white",
            "1px solid #1890ff" if selected else "none"
        )
        self.setStyleSheet(base_style)
