import json
import louis
import os
import tempfile
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QTextEdit, QLineEdit, QComboBox
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

        self.testing_widget = TestingWidget(self, get_table_content_callback=self.get_content)
        main_layout.addWidget(self.testing_widget)

        self.setLayout(main_layout)

        apply_styles(self)

        self.toast = None

    def add_entry(self):
        entry_data = self.add_entry_widget.collect_entry_data()
        if self.validate_entry(entry_data):
            self.table_preview.add_entry(entry_data)
            self.show_toast("Entry added successfully!", "./src/assets/icons/tick.png", 75, 175, 78)
        else:
            self.show_toast("Invalid entry!", "./src/assets/icons/error.png", 255, 0, 0)

    def validate_entry(self, entry):
        if not entry.strip():
            return False
        parts = entry.split()
        if not parts:
            return False
        opcode = parts[0]
        valid_opcodes = [code["code"] for code in json.load(open('./src/assets/data/opcodes.json'))["codes"]]
        if opcode not in valid_opcodes:
            return False
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tbl', delete=False, encoding='utf-8') as temp_file:
            temp_file.write('\n'.join(self.table_preview.entries + [entry]))
            temp_table_path = temp_file.name
        try:
            louis.translate((temp_table_path,), "test".encode('utf-8'), mode=louis.compbrlAtCursor)
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
        finally:
            os.unlink(temp_table_path)

    def save_entries(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.table_preview.entries, file)

    def load_entries(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            entries = json.load(file)
            self.table_preview.entries = entries
            self.table_preview.update_content()

    def set_content(self, content):
        if content.strip():
            self.table_preview.entries = [line for line in content.splitlines() if line.strip()]
        else:
            self.table_preview.entries = []
        self.table_preview.update_content()

    
    def get_content(self):
        entries = self.table_preview.entries
        if not any("include" in entry for entry in entries):
            entries = [
                "include unicode.dis",
                "include en-us-g1.ctb"
            ] + entries
        if not any("\\n" in entry for entry in entries):
            entries.append("always \\n 0")
        return '\n'.join(entries)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.add_entry()

    def show_toast(self, text, icon_path, colorR, colorG, colorB):
        if self.toast:
            self.toast.close()
        self.toast = Toast(text, icon_path, colorR, colorG, colorB, self)
        self.toast.move((self.width() - self.toast.width()) // 2, self.height() - self.toast.height() - 10)
        self.toast.show_toast()

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