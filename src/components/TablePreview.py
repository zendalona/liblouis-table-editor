from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
from components.AddEntry.EntryWidget import EntryWidget
from utils.ApplyStyles import apply_styles

class TablePreview(QWidget):
    def __init__(self, table_editor, parent=None):
        super().__init__(parent)
        self.table_editor = table_editor
        self.entries = []
        self.entry_widgets = []  
        self.current_index = -1 
        apply_styles(self)
        self.initUI()
        self.setFocusPolicy(Qt.StrongFocus)

    def initUI(self):
        self.setStyleSheet("background-color: white; border-bottom: 1px solid #b0c6cf;")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFocusPolicy(Qt.NoFocus) 
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        
        self.scroll_area.viewport().installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.scroll_area.viewport() and event.type() == event.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(obj, event)
        
    def update_content(self):
        self.clear_layout()
        self.entry_widgets = []  
        for entry in self.entries:
            entry_widget = EntryWidget(entry, self.table_editor)
            entry_widget.mousePressEvent = lambda e, w=entry_widget: self.handle_entry_click(w, e)
            entry_widget.setFocusPolicy(Qt.NoFocus) 
            self.entry_widgets.append(entry_widget)  
            self.scroll_layout.addWidget(entry_widget)
        
        if self.current_index >= 0 and self.current_index < len(self.entry_widgets):
            self.select_entry(self.current_index)
            
    def add_entry(self, entry):
        self.entries.append(entry)
        self.update_content()
        self.select_entry(len(self.entries) - 1)

    def handle_entry_click(self, widget, event):
        if event.button() == Qt.LeftButton:
            index = self.entry_widgets.index(widget)
            self.select_entry(index)
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
        font = QFont()
        font.setPointSize(size)
        
        self.scroll_area.setFont(font)
        
        for widget in self.entry_widgets:
            widget.update_font_size(size)
            
        self.scroll_widget.adjustSize()
        self.scroll_area.updateGeometry()
        self.update()

    def keyPressEvent(self, event):
        if not self.entry_widgets:
            event.ignore()
            return

        key = event.key()
        
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
        elif key == Qt.Key_Tab and not event.isAutoRepeat():
            if event.modifiers() == Qt.ShiftModifier:
                if self.current_index > 0:
                    self.select_entry(self.current_index - 1)
                    event.accept()
                    return
            else:
                if self.current_index < len(self.entry_widgets) - 1:
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
