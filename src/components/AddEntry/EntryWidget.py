from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QMenu, QAction, QLineEdit, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase

class EntryWidget(QFrame):
    def __init__(self, entry, table_editor, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.table_editor = table_editor
        self.current_font_size = 12 
        self.setObjectName("entry_frame")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(2)
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
        font.setPointSize(self.current_font_size)
        font_families = ["Arial Unicode MS", "Nirmala UI", "Mangal", "Arial", "Segoe UI"]
        db = QFontDatabase()
        for family in font_families:
            if family in db.families():
                font.setFamily(family)
                break
        
        font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferDefault)
        self.label_text.setFont(font)
        
        self.label_text.setTextFormat(Qt.PlainText)
        
        self.layout.addWidget(self.label_text, alignment=Qt.AlignVCenter)
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
        
        parent = self.parentWidget()
        if parent:
           
            new_entry_widget = EntryWidget(self.entry, self.table_editor, parent=parent)
            new_entry_widget.update_font_size(self.current_font_size)
            
           
            table_preview = parent
            while table_preview and not hasattr(table_preview, 'entries'):
                table_preview = table_preview.parentWidget()
            
            if table_preview and hasattr(table_preview, 'entries'):
               
                table_preview.entries.append(self.entry)
                table_preview.update_content()
                
                new_index = len(table_preview.entries) - 1
                table_preview.select_entry(new_index)

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
            pass

    def onHoverLeave(self, event):
        if not self.property("selected"):
            pass

    def load_into_editor(self, event=None):
        self.table_editor.load_entry_into_editor(self.entry)

    def update_font_size(self, size):
        self.current_font_size = size
        label_font = self.label_text.font()
        edit_font = self.edit_line.font()
        label_font.setPointSize(size)
        edit_font.setPointSize(size)
        self.label_text.setFont(label_font)
        self.edit_line.setFont(edit_font)
        
        self.set_entry_frame_style(self.property("selected"))
        
        self.label_text.update()
        self.edit_line.update()
        self.update()
        self.repaint()

    def setSelected(self, selected):
        self.setProperty("selected", selected)
        self.set_entry_frame_style(selected)

    def set_entry_frame_style(self, selected):
        self.setProperty("selected", selected)
        self.setStyleSheet(f"""
            QFrame#entry_frame {{
                background-color: {'#eaf4fb' if selected else 'white'};
                border: {'2px solid #339af0' if selected else 'none'};
                border-radius: 6px;
            }}
            QFrame#entry_frame QLabel {{
                background-color: transparent;
                font-size: {self.current_font_size}pt;
            }}
            QFrame#entry_frame QLineEdit {{
                background-color: transparent;
                font-size: {self.current_font_size}pt;
            }}
        """)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()