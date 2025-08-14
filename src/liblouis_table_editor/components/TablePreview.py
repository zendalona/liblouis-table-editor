from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QApplication
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QClipboard
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
        self.copied_entry = None  
        self.is_editing_mode = False 
        self._maintain_position = False  
        self._fresh_load = True  
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
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFocusPolicy(Qt.NoFocus)
        self.scroll_area.mousePressEvent = self.scroll_area_click  
        
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
        
        self.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.scroll_area.viewport() and event.type() == event.KeyPress:
            self.keyPressEvent(event)
            return True
        elif obj == self and event.type() == event.MouseButtonPress:

            if event.button() == Qt.LeftButton:
                click_pos = event.pos()
                
                scroll_pos = self.scroll_widget.mapFromParent(click_pos)
                
                clicked_on_entry = False
                for widget in self.entry_widgets:
                    try:
                        widget_rect = widget.geometry()
                        if widget_rect.contains(scroll_pos):
                            clicked_on_entry = True
                            break
                    except RuntimeError:

                        continue
                
                if not clicked_on_entry:
                    self.clear_selection()
                    if hasattr(self.table_editor, 'clear_editor_form'):
                        self.table_editor.clear_editor_form()
                    return True
                    
        return super().eventFilter(obj, event)
        
    def update_content(self):

        scroll_position = self.scroll_area.verticalScrollBar().value()
        
        self.clear_layout()
        self.entry_widgets = []  
        for i, entry in enumerate(self.entries):
            entry_widget = EntryWidget(entry, self.table_editor)
            entry_widget.update_font_size(self.entry_font_size) 

            entry_widget._preview_index = i
            entry_widget.mousePressEvent = lambda e, idx=i: self.handle_entry_click_by_index(idx, e)
            entry_widget.setFocusPolicy(Qt.NoFocus) 
            self.entry_widgets.append(entry_widget)  
            self.scroll_layout.addWidget(entry_widget)
            if i < len(self.entries) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Plain)
                line.setObjectName("entry_line")
                self.scroll_layout.addWidget(line)
        
        # Restore scroll position after a short delay
        # Always restore position unless it's a fresh load
        if not hasattr(self, '_fresh_load') or not self._fresh_load:
            QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(scroll_position))
        else:
            self._fresh_load = False
            
        # Reset the maintain position flag
        if hasattr(self, '_maintain_position'):
            self._maintain_position = False
        
        # Re-select the current entry if it still exists
        if 0 <= self.current_index < len(self.entry_widgets):
            self.entry_widgets[self.current_index].setSelected(True)
            
    def add_entry(self, entry, sort_entries=True):
        self.entries.append(entry)

        if sort_entries:
            def extract_number(e):
                parts = e.split()
                try:
                    return int(parts[0])
                except (ValueError, IndexError):
                    return float('inf')
            self.entries.sort(key=extract_number)
        
        self.update_content()
        if sort_entries:
            self.select_entry(self.entries.index(entry))
        else:
            # For new entries added at the end, select the last one
            self.select_entry(len(self.entries) - 1)

    def copy_entry(self):
        """Copy the currently selected entry to clipboard and internal storage"""
        if 0 <= self.current_index < len(self.entries):
            self.copied_entry = self.entries[self.current_index]
            clipboard = QApplication.clipboard()
            clipboard.setText(self.copied_entry)
            if hasattr(self.table_editor, 'show_toast'):
                from liblouis_table_editor.utils.asset_utils import get_icon_for_toast
                self.table_editor.show_toast("Entry copied to clipboard", get_icon_for_toast('success'), 75, 175, 78)

    def paste_entry(self):
        """Paste the copied entry after the currently selected entry"""
        if self.copied_entry:
            # Save state for undo
            if hasattr(self.table_editor, '_save_state_for_undo'):
                self.table_editor._save_state_for_undo()
                
            # Insert after current selection, or at the end if nothing selected
            insert_index = self.current_index + 1 if self.current_index >= 0 else len(self.entries)
            self.entries.insert(insert_index, self.copied_entry)
            self.update_content()
            self.select_entry(insert_index)
            
            # Mark as unsaved
            if hasattr(self.table_editor, 'mark_as_unsaved'):
                self.table_editor.mark_as_unsaved()
                
            if hasattr(self.table_editor, 'show_toast'):
                from liblouis_table_editor.utils.asset_utils import get_icon_for_toast
                self.table_editor.show_toast("Entry pasted", get_icon_for_toast('success'), 75, 175, 78)

    def delete_entry(self):
        """Delete the currently selected entry"""
        if 0 <= self.current_index < len(self.entries):
            # Save state for undo
            if hasattr(self.table_editor, '_save_state_for_undo'):
                self.table_editor._save_state_for_undo()
                
            deleted_entry = self.entries.pop(self.current_index)
            self._maintain_position = True  # Maintain scroll position
            self.update_content()
            
            # Adjust selection
            if self.current_index >= len(self.entries) and self.entries:
                self.select_entry(len(self.entries) - 1)
            elif self.entries:
                self.select_entry(min(self.current_index, len(self.entries) - 1))
            else:
                self.current_index = -1
                
            # Mark as unsaved
            if hasattr(self.table_editor, 'mark_as_unsaved'):
                self.table_editor.mark_as_unsaved()
                
            if hasattr(self.table_editor, 'show_toast'):
                from liblouis_table_editor.utils.asset_utils import get_icon_for_toast
                self.table_editor.show_toast("Entry deleted", get_icon_for_toast('success'), 75, 175, 78)

    def update_current_entry(self, new_entry_text):
        """Update the currently selected entry with new text"""
        if 0 <= self.current_index < len(self.entries):
            self.entries[self.current_index] = new_entry_text
            self._maintain_position = True  # Flag to maintain scroll position
            self.update_content()
            self.select_entry(self.current_index)  # Re-select the updated entry
            if hasattr(self.table_editor, 'mark_as_unsaved'):
                self.table_editor.mark_as_unsaved()

    def clear_selection(self):
        """Clear the current selection"""
        if 0 <= self.current_index < len(self.entry_widgets):
            try:
                self.entry_widgets[self.current_index].setSelected(False)
            except RuntimeError:
                # Widget has been deleted, ignore
                pass
        self.current_index = -1
        self.is_editing_mode = False
        
    def scroll_area_click(self, event):
        """Handle clicks in empty areas of the scroll area"""
        if event.button() == Qt.LeftButton:
            # Check if click is on empty space (not on any entry widget)
            click_pos = event.pos()
            viewport_pos = self.scroll_area.viewport().mapFromParent(click_pos)
            
            clicked_on_entry = False
            for widget in self.entry_widgets:
                try:
                    # Get widget position relative to viewport
                    widget_pos = widget.mapTo(self.scroll_area.viewport(), widget.rect().topLeft())
                    widget_rect = QRect(widget_pos, widget.size())
                    
                    if widget_rect.contains(viewport_pos):
                        clicked_on_entry = True
                        break
                except RuntimeError:
                    # Widget deleted, skip
                    continue
            
            # If not clicked on any entry, clear selection
            if not clicked_on_entry:
                self.clear_selection()
                # Clear the form in table editor
                if hasattr(self.table_editor, 'clear_editor_form'):
                    self.table_editor.clear_editor_form()

    def handle_entry_click(self, widget, event):
        if event.button() == Qt.LeftButton:
            try:
                index = self.entry_widgets.index(widget)
                self.select_entry(index)
                self.setFocus()
            except (ValueError, RuntimeError):
                # Widget not found or deleted, ignore
                pass
        elif event.button() == Qt.RightButton:
            try:
                widget.contextMenuEvent(event)
            except RuntimeError:
                # Widget deleted, ignore
                pass

    def handle_entry_click_by_index(self, index, event):
        """Handle entry click using index instead of widget reference"""
        if event.button() == Qt.LeftButton:
            if 0 <= index < len(self.entry_widgets):
                self.select_entry(index)
                self.setFocus()
        elif event.button() == Qt.RightButton:
            if 0 <= index < len(self.entry_widgets):
                try:
                    self.entry_widgets[index].contextMenuEvent(event)
                except RuntimeError:
                    # Widget deleted, ignore
                    pass

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
        if 0 <= index < len(self.entry_widgets) and 0 <= index < len(self.entries):
            # Safely clear previous selection
            if 0 <= self.current_index < len(self.entry_widgets):
                try:
                    self.entry_widgets[self.current_index].setSelected(False)
                except RuntimeError:
                    # Widget has been deleted, ignore
                    pass
            
            self.current_index = index  
            widget = self.entry_widgets[index]
            widget.setSelected(True)
            self.ensure_widget_visible(widget)
            if hasattr(self.table_editor, 'load_entry_into_editor'):
                self.table_editor.load_entry_into_editor(self.entries[index])
                self.is_editing_mode = True  # Enable editing mode

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

        # Handle copy/paste/delete shortcuts
        if modifiers == Qt.ControlModifier:
            if key == Qt.Key_C:  # Copy
                self.copy_entry()
                event.accept()
                return
            elif key == Qt.Key_V:  # Paste
                self.paste_entry()
                event.accept()
                return
            elif key == Qt.Key_BracketRight or key == Qt.Key_Equal: 
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

        # Handle Delete key
        if key == Qt.Key_Delete:
            self.delete_entry()
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
            
