import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout , QSizePolicy, QTextEdit, QLineEdit, QComboBox
)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from components.AddEntry.AddEntryWidget import AddEntryWidget
from components.AddEntry.BrailleInputWidget import BrailleInputWidget
from components.TablePreview import TablePreview
from components.TestingWidget import TestingWidget
from utils.ApplyStyles import apply_styles
from utils.Toast import Toast


class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._unsaved_changes = False
        self._original_content = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.table_preview = TablePreview(self)
        top_layout.addWidget(self.table_preview)

        self.add_entry_widget = AddEntryWidget()
        
        self.add_entry_widget.add_button.clicked.connect(self.add_entry)
        top_layout.addWidget(self.add_entry_widget)

        self.add_entry_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addLayout(top_layout)

        self.testing_widget = TestingWidget(self)
        main_layout.addWidget(self.testing_widget)

        self.setLayout(main_layout)

        apply_styles(self)

        self.toast = None

    def validate_entry_data(self, entry_data):
        """Validate the entry data before adding it to the table."""
        if not entry_data:
            return False
        
        # Check if entry has required fields based on opcode
        if isinstance(entry_data, dict):
            if 'opcode' not in entry_data:
                return False
            # Add more specific validation rules based on opcode
            return True
        elif isinstance(entry_data, str):
            return bool(entry_data.strip())
        return False

    def add_entry(self):
        entry_data = self.add_entry_widget.collect_entry_data()
        if not self.validate_entry_data(entry_data):
            self.show_toast("Invalid entry data!", "./src/assets/icons/error.png", 255, 0, 0)
            return
        self.table_preview.add_entry(entry_data)
        self._unsaved_changes = True
        self.show_toast("Entry added successfully!", "./src/assets/icons/tick.png", 75, 175, 78)

    def save_entries(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                if isinstance(self.table_preview.entries, list):
                    content = '\n'.join(self.table_preview.entries)
                    file.write(content)
                else:
                    json.dump(self.table_preview.entries, file, ensure_ascii=False, indent=2)
            self._original_content = self.get_content()
            self._unsaved_changes = False
            self.show_toast("File saved successfully!", "./src/assets/icons/tick.png", 75, 175, 78)
        except Exception as e:
            self.show_toast(f"Error saving file: {str(e)}", "./src/assets/icons/error.png", 255, 0, 0)

    def load_entries(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    self.table_preview.entries = []
                else:
                    try:
                        # Try parsing as JSON first
                        self.table_preview.entries = json.loads(content)
                    except json.JSONDecodeError:
                        # If not JSON, treat as line-separated entries
                        self.table_preview.entries = [line for line in content.splitlines() if line.strip()]
                self.table_preview.update_content()
            self.show_toast("File loaded successfully!", "./src/assets/icons/tick.png", 75, 175, 78)
        except FileNotFoundError:
            self.show_toast("Error: File not found", "./src/assets/icons/error.png", 255, 0, 0)
        except Exception as e:
            self.show_toast(f"Error loading file: {str(e)}", "./src/assets/icons/error.png", 255, 0, 0)

    def set_content(self, content):
        try:
            if not content or not content.strip():
                self.table_preview.entries = []
            else:
                try:
                    # Try parsing as JSON first
                    self.table_preview.entries = json.loads(content)
                except json.JSONDecodeError:
                    # If not JSON, treat as line-separated entries
                    self.table_preview.entries = [line for line in content.splitlines() if line.strip()]
            self.table_preview.update_content()
            self._original_content = self.get_content()
            self._unsaved_changes = False
        except Exception as e:
            self.show_toast(f"Error setting content: {str(e)}", "./src/assets/icons/error.png", 255, 0, 0)

    def get_content(self):
        try:
            return self.table_preview.entries
        except Exception:
            return []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.add_entry()
        super().keyPressEvent(event)  # Call parent implementation

    def show_toast(self, text, icon_path, colorR, colorG, colorB):
        try:
            if self.toast:
                self.toast.close()
                self.toast.deleteLater()  # Properly clean up old toast
            icon_path = os.path.normpath(icon_path)  # Normalize path for cross-platform compatibility
            self.toast = Toast(text, icon_path, colorR, colorG, colorB, self)
            self.toast.move((self.width() - self.toast.width()), self.height() + 290)
            self.toast.show_toast()
        except Exception as e:
            print(f"Error showing toast: {str(e)}")  # Fallback error handling

    def load_entry_into_editor(self, entry):
        self.add_entry_widget.clear_form()

        parts = entry.split()
        if not parts:
            return

        opcode = parts[0]
        index = self.add_entry_widget.opcode_combo.findText(opcode)
        if index != -1 and index != 0:
            self.add_entry_widget.opcode_combo.setCurrentIndex(index)

            nested_form = self.add_entry_widget.field_inputs.get("nested_form")
            if nested_form:
                form_data = parts[1:]
                self.fill_form_data(nested_form, form_data)
        
                filled_fields_count = len(nested_form.field_inputs)
                remaining_parts = form_data[filled_fields_count:]
                if remaining_parts:
                    remaining_comment = " ".join(remaining_parts)
                    self.add_entry_widget.comment_input.setText(remaining_comment)
        else:
            self.add_entry_widget.comment_input.setText(entry)

    def fill_form_data(self, form, data):
        field_index = 0
        fields_widgets = list(form.field_inputs.items())

        for field, widget in fields_widgets:
            if field_index < len(data):
                if isinstance(widget, tuple) and field == "exactdots":
                    at_symbol, braille_input = widget
                    exactdots_value = data[field_index]
                    if exactdots_value.startswith("@"):
                        braille_input.setText(exactdots_value[1:])
                elif isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                    widget.setText(data[field_index])
                elif isinstance(widget, QComboBox):
                    index = widget.findText(data[field_index])
                    if index != -1:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, BrailleInputWidget):
                    widget.braille_input.setText(data[field_index])
                field_index += 1

    def has_unsaved_changes(self):
        """Check if there are unsaved changes in the editor."""
        if self._unsaved_changes:
            return True
        current_content = self.get_content()
        return current_content != self._original_content
