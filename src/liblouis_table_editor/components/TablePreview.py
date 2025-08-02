from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QFontDatabase
from liblouis_table_editor.components.AddEntry.EntryWidget import EntryWidget
from liblouis_table_editor.utils.ApplyStyles import apply_styles

class TablePreview(QWidget):
    def __init__(self, table_editor, parent=None):
        super().__init__(parent)
        self.table_editor = table_editor
        self.entries = []
        self.entry_widgets = []  
        self.current_index = -1
        self.entry_font_size = 12 
        self.min_font_size = 8
        self.max_font_size = 24
        apply_styles(self)
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus)  

    def initUI(self):
        self.setObjectName("table_preview")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setAccessibleName("Table Preview Scroll Area")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFocusPolicy(Qt.NoFocus)  
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setAccessibleName("Table Preview Scroll Widget")
        self.scroll_widget.setFocusPolicy(Qt.NoFocus)  
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(2)

        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

        initial_font = QFont()
        initial_font.setPointSize(self.entry_font_size)
        self.scroll_area.setFont(initial_font)
        
        self.scroll_area.viewport().installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.scroll_area.viewport() and event.type() == event.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(obj, event)
        
    def update_content(self):
        self.clear_layout()
        self.entry_widgets = []  
        for i, entry in enumerate(self.entries):
            entry_widget = EntryWidget(entry, self.table_editor)
            entry_widget.update_font_size(self.entry_font_size) 
            entry_widget.mousePressEvent = lambda e, w=entry_widget: self.handle_entry_click(w, e)
            entry_widget.setFocusPolicy(Qt.NoFocus) 
            self.entry_widgets.append(entry_widget)  
            self.scroll_layout.addWidget(entry_widget)
            if i < len(self.entries) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Plain)
                line.setObjectName("entry_line")
                self.scroll_layout.addWidget(line)
        
        if self.current_index >= 0 and self.current_index < len(self.entry_widgets):
            self.select_entry(self.current_index)
            
    def add_entry(self, entry):
        self.entries.append(entry)

        def extract_number(e):
            parts = e.split()
            try:
                return int(parts[0])
            except (ValueError, IndexError):
                return float('inf')
        self.entries.sort(key=extract_number)
        self.update_content()
        self.select_entry(self.entries.index(entry))

    def handle_entry_click(self, widget, event):
        if event.button() == Qt.LeftButton:
            index = self.entry_widgets.index(widget)
            self.select_entry(index)
            # Ensure the TablePreview widget has focus for keyboard navigation
            self.setFocus()
        elif event.button() == Qt.RightButton:
            widget.contextMenuEvent(event)

    def ensure_widget_visible(self, widget, margin=10):
        if not widget:
            return

        widget_rect = QRect(widget.mapTo(self.scroll_area.viewport(), widget.rect().topLeft()),
                          widget.size())
        
        viewport = self.scroll_area.viewport()
        viewport_height = viewport.height()
        scrollbar = self.scroll_area.verticalScrollBar()
        current_scroll = scrollbar.value()

        top_margin = margin
        bottom_margin = viewport_height - margin

        if widget_rect.top() < top_margin:
            new_scroll = current_scroll + widget_rect.top() - top_margin
            scrollbar.setValue(int(new_scroll))
        
        elif widget_rect.bottom() > bottom_margin:
            new_scroll = current_scroll + widget_rect.bottom() - bottom_margin
            scrollbar.setValue(int(new_scroll))

    def select_entry(self, index):
        if 0 <= index < len(self.entry_widgets):
            if 0 <= self.current_index < len(self.entry_widgets):
                self.entry_widgets[self.current_index].setSelected(False)
            self.current_index = index  
            widget = self.entry_widgets[index]
            widget.setSelected(True)
            self.ensure_widget_visible(widget)
            if hasattr(self.table_editor, 'load_entry_into_editor'):
                self.table_editor.load_entry_into_editor(self.entries[index])

    def clear_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
    def update_font_size(self, size):
       
        scroll_font = QFont()
        scroll_font.setPointSize(size)
        font_families = ["Arial Unicode MS", "Nirmala UI", "Mangal", "Arial", "Segoe UI"]
        db = QFontDatabase()
        for family in font_families:
            if family in db.families():
                scroll_font.setFamily(family)
                break
        scroll_font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferDefault)
        
        self.scroll_area.setFont(scroll_font)
        
        for widget in self.entry_widgets:
            widget.update_font_size(size)
            
        self.scroll_widget.adjustSize()
        self.scroll_area.updateGeometry()
        
        self.scroll_area.update()
        self.scroll_widget.update()
        self.update()
        self.repaint()
        
        for widget in self.entry_widgets:
            widget.update()
            widget.repaint()

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        if modifiers == Qt.ControlModifier:
            if key == Qt.Key_BracketRight or key == Qt.Key_Equal: 
                new_size = min(self.max_font_size, self.entry_font_size + 2)
                if new_size != self.entry_font_size:
                    self.entry_font_size = new_size
                    self.update_font_size(self.entry_font_size)
                event.accept()
                return
            elif key == Qt.Key_BracketLeft or key == Qt.Key_Minus:  
                new_size = max(self.min_font_size, self.entry_font_size - 2)
                if new_size != self.entry_font_size:
                    self.entry_font_size = new_size
                    self.update_font_size(self.entry_font_size)
                event.accept()
                return
            elif key == Qt.Key_0:  
                self.entry_font_size = 12 
                self.update_font_size(self.entry_font_size)
                event.accept()
                return

        if not self.entry_widgets:
            event.ignore()
            return
        
        if key == Qt.Key_Up:
            if self.current_index > 0:
                self.select_entry(self.current_index - 1)
                event.accept()
                return
        elif key == Qt.Key_Down:
            if self.current_index < len(self.entry_widgets) - 1:
                self.select_entry(self.current_index + 1)
                event.accept()
                return
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):

            if 0 <= self.current_index < len(self.entry_widgets):
                entry_widget = self.entry_widgets[self.current_index]
                if hasattr(entry_widget, 'load_into_editor'):
                    entry_widget.load_into_editor()
                event.accept()
                return
        elif key == Qt.Key_Tab and not event.isAutoRepeat():
            if modifiers == Qt.ShiftModifier:
                if self.current_index == 0:
                    if hasattr(self.table_editor, 'add_entry_widget'):
                        self.table_editor.add_entry_widget.setFocus()
                        event.accept()
                        return
                else:
                    self.select_entry(self.current_index - 1)
                    event.accept()
                    return
            else:
                if self.current_index == len(self.entry_widgets) - 1:
                    if hasattr(self.table_editor, 'add_entry_widget'):
                        self.table_editor.add_entry_widget.setFocus()
                        event.accept()
                        return
                else:
                    self.select_entry(self.current_index + 1)
                    event.accept()
                    return
        elif key == Qt.Key_Home:
            self.select_entry(0)
            event.accept()
            return
        elif key == Qt.Key_End:
            self.select_entry(len(self.entry_widgets) - 1)
            event.accept()
            return
        elif key == Qt.Key_PageUp:
            visible_height = self.scroll_area.viewport().height()
            widget_height = self.entry_widgets[0].height() if self.entry_widgets else 0
            items_per_page = max(1, (visible_height - 20) // widget_height)
            new_index = max(0, self.current_index - items_per_page)
            self.select_entry(new_index)
            event.accept()
            return
        elif key == Qt.Key_PageDown:
            visible_height = self.scroll_area.viewport().height()
            widget_height = self.entry_widgets[0].height() if self.entry_widgets else 0
            items_per_page = max(1, (visible_height - 20) // widget_height)
            new_index = min(len(self.entry_widgets) - 1, self.current_index + items_per_page)
            self.select_entry(new_index)
            event.accept()
            return

        event.ignore()

    def focusInEvent(self, event):
        super().focusInEvent(event)

        if self.current_index == -1 and self.entry_widgets:
            self.select_entry(0)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
            
