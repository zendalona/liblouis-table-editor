from collections import OrderedDict
import json
import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QComboBox, QLabel, QPushButton, QSizePolicy, QLayout
)
from PyQt5.QtCore import Qt, QEvent
from liblouis_table_editor.components.AddEntry.BrailleInputWidget import BrailleInputWidget
from liblouis_table_editor.components.AddEntry.UnicodeSelector import UnicodeSelector
from liblouis_table_editor.utils.view import clearLayout

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_path, "assets", "data", relative_path)

data = json.load(open(resource_path('opcodes.json'), 'r'), object_pairs_hook=OrderedDict)
opcodes = data["codes"]

class OpcodeForm(QWidget):
    def __init__(self, fields, parent=None):
        super().__init__(parent)
        self.field_inputs = {}
        self.initUI(fields)

    def initUI(self, fields):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)

        self.nested_forms = []  # Track nested forms

        for field, placeholder in fields.items():
            if field == "opcode":
                nested_opcode_combo = QComboBox()
                nested_opcode_combo.setPlaceholderText("Select Opcode")
                nested_opcode_combo.setAccessibleName("Opcode Combo Box")
                nested_opcode_combo.installEventFilter(self)
                self.populate_opcode_combo(nested_opcode_combo, placeholder)
                nested_opcode_combo.currentIndexChanged.connect(
                    lambda idx, combo=nested_opcode_combo: self.on_opcode_selected(idx, combo)
                )
                self.form_layout.addWidget(nested_opcode_combo)
                self.field_inputs[field] = nested_opcode_combo

            elif field == "unicode" or field.startswith("unicode"):
                unicode_container = QHBoxLayout()
                unicode_display = QLineEdit()
                unicode_display.setPlaceholderText("Selected Character")
                unicode_display.setAccessibleName("Unicode Display Field")
                unicode_display.installEventFilter(self)
                unicode_input = QLineEdit()
                unicode_input.setPlaceholderText(placeholder)
                unicode_input.setProperty("includeInEntry", True)
                unicode_input.setAccessibleName("Unicode Input Field")
                unicode_input.installEventFilter(self)
                
                # Set size policy for full width
                unicode_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                unicode_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                unicode_input.textChanged.connect(lambda text, u_display=unicode_display: self.updateDisplayCharacter(u_display, text))
                unicode_display.textChanged.connect(lambda text, u_input=unicode_input: self.updateUnicodeInput(text, u_input))

                select_button = QPushButton("Select Unicode")
                select_button.setAccessibleName("Select Unicode Button")
                select_button.installEventFilter(self)
                select_button.clicked.connect(lambda _, u_display=unicode_display, u_input=unicode_input: self.showUnicodePopup(u_display, u_input))

                unicode_container.addWidget(unicode_display)
                unicode_container.addWidget(unicode_input)
                unicode_container.addWidget(select_button)
                
                # Ensure container uses full width
                unicode_container.setSizeConstraint(QLayout.SetMinimumSize)

                self.form_layout.addLayout(unicode_container)
                self.field_inputs[field] = unicode_input

            elif field == "name":
                name_input = QLineEdit()
                name_input.setPlaceholderText(placeholder)
                name_input.setAccessibleName("Name Input Field")
                name_input.installEventFilter(self)
                # Set size policy for full width
                name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(name_input)
                self.field_inputs[field] = name_input

            elif field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText(placeholder)
                inp.setAccessibleName("Characters Input Text Area")
                inp.installEventFilter(self)
                # Set size policy for full width
                inp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(inp)
                self.field_inputs[field] = inp

            elif field == "dots":
                self.braille_input_widget = BrailleInputWidget()
                self.braille_input_widget.braille_input.installEventFilter(self)
                self.form_layout.addWidget(self.braille_input_widget)
                self.field_inputs[field] = self.braille_input_widget.braille_input
            
            elif field == "exactdots":
                exactdots_container = QHBoxLayout()

                # Read-only field with '@'
                at_symbol = QLineEdit("@")
                at_symbol.setReadOnly(True)
                at_symbol.setFixedWidth(40)
                at_symbol.setFixedHeight(50)
                at_symbol.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                at_symbol.setAccessibleName("At Symbol Field")
                at_symbol.installEventFilter(self)

                self.braille_input_widget = BrailleInputWidget()
                self.braille_input_widget.braille_input.installEventFilter(self)

                exactdots_container.addWidget(at_symbol)
                exactdots_container.addWidget(self.braille_input_widget)

                self.form_layout.addLayout(exactdots_container)
                self.field_inputs[field] = (at_symbol, self.braille_input_widget.braille_input)
                
            elif field == "groupDots":
                groupdots_container = QHBoxLayout()
                
                for i in range(placeholder):
                    braille_input_widget = BrailleInputWidget()
                    braille_input_widget.braille_input.installEventFilter(self)
                    groupdots_container.addWidget(braille_input_widget)
                    self.field_inputs[f"{field}_{i+1}"] = braille_input_widget.braille_input
                    
                    if i < placeholder - 1:
                        comma_label = QLineEdit(",")
                        comma_label.setReadOnly(True)
                        comma_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                        comma_label.setFixedWidth(30)
                        comma_label.setFixedHeight(50)
                        comma_label.setAccessibleName("Comma Label Field")
                        comma_label.installEventFilter(self)
                        groupdots_container.addWidget(comma_label)

                self.form_layout.addLayout(groupdots_container)

            elif field == "base_attribute":
                base_attr_dropdown = QComboBox()
                base_attr_dropdown.addItems(["space", "digit", "letter", "lowercase", "uppercase", "punctuation", "sign", "math", "litdigit", "attribute", "before", "after"])         
                base_attr_dropdown.setAccessibleName("Base Attribute Combo Box")
                base_attr_dropdown.installEventFilter(self)
                base_attr_dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(base_attr_dropdown)
                self.field_inputs[field] = base_attr_dropdown

    def populate_opcode_combo(self, combo, placeholder=None):
        combo.clear()
        combo.addItem("Select Opcode", None)  
        for opcode in opcodes:
            combo.addItem(opcode["code"], opcode)
        
        if placeholder:
            index = combo.findText(placeholder)
            if index != -1:
                combo.setCurrentIndex(index)

    def on_opcode_selected(self, index, combo):
        if index > 0:
            self.clear_nested_forms()
            opcode = combo.itemData(index)
            nested_form = OpcodeForm(opcode["fields"], self)
            self.form_layout.addWidget(nested_form)
            self.nested_forms.append(nested_form)
            self.field_inputs["nested_form"] = nested_form
        else:
            clearLayout(self.form_layout)

    def clear_nested_forms(self):
        for form in self.nested_forms:
            form.deleteLater()
        self.nested_forms.clear()

    def updateUnicodeInput(self, text, unicode_input):
        if text:
            hex_values = [f'\\x{ord(char):04X}' for char in text]
            unicode_input.setText(''.join(hex_values))
        else:
            unicode_input.clear()

    def updateDisplayCharacter(self, unicode_display, text):
        try:
            characters = []
            hex_values = text.split('\\x')[1:]

            for hex_value in hex_values:
                if hex_value:
                    hex_value = hex_value.zfill(4)
                    code_point = int(hex_value, 16)
                    if code_point > 0x10FFFF:
                        raise ValueError(f"Code point {hex_value} is too large to be a valid Unicode character.")
                    characters.append(chr(code_point))

            unicode_display.setText("".join(characters))
        
        except (ValueError, OverflowError) as e:
            unicode_display.setText("[Invalid Unicode]")
            print(f"Error converting Unicode: {e}")

    def showUnicodePopup(self, unicode_display, unicode_input):
        if not hasattr(self, 'unicode_popup') or self.unicode_popup is None or not self.unicode_popup.isVisible():
            self.unicode_popup = UnicodeSelector()
            self.unicode_popup.on_select(lambda char, code: self.setUnicode(unicode_display, unicode_input, char, code))
        self.unicode_popup.show()
        self.unicode_popup.raise_()
        self.unicode_popup.activateWindow()
        
    def setUnicode(self, unicode_display, unicode_input, char, code):
        unicode_display.setText(char)
        unicode_input.setText(code)
        if hasattr(self, 'unicode_popup'):
            self.unicode_popup.close()
            self.unicode_popup = None

    def get_focusable_widgets(self):
        widgets = []
        for field, widget in self.field_inputs.items():
            if isinstance(widget, (QLineEdit, QTextEdit, QComboBox)):
                widgets.append(widget)
            elif isinstance(widget, tuple) and field == "exactdots":
                widgets.extend(widget)
            elif isinstance(widget, BrailleInputWidget):
                widgets.append(widget.braille_input)
            elif isinstance(widget, OpcodeForm):
                widgets.extend(widget.get_focusable_widgets())
        return widgets

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            obj.setFocus()
        return super().eventFilter(obj, event)

class AddEntryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.field_inputs = {}
        self.initUI()
        self.last_nav_was_tab = False
        self.install_input_event_filters()

    def install_input_event_filters(self):
        def install_on_widget(w):
            if isinstance(w, QLineEdit) or isinstance(w, QTextEdit):
                w.installEventFilter(self)
            elif hasattr(w, 'field_inputs'):
                for subw in w.field_inputs.values():
                    install_on_widget(subw)
        if hasattr(self, 'opcode_combo'):
            self.opcode_combo.installEventFilter(self)
        for w in self.field_inputs.values():
            install_on_widget(w)
        if hasattr(self, 'comment_input'):
            self.comment_input.installEventFilter(self)

        for textedit in self.findChildren(QTextEdit):
            textedit.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if self.last_nav_was_tab:
                obj.setProperty('tabFocus', True)
                obj.style().unpolish(obj)
                obj.style().polish(obj)
            else:
                obj.setProperty('tabFocus', False)
                obj.style().unpolish(obj)
                obj.style().polish(obj)
        elif event.type() == QEvent.FocusOut:
            obj.setProperty('tabFocus', False)
            obj.style().unpolish(obj)
            obj.style().polish(obj)
        elif event.type() == QEvent.KeyPress:

            if isinstance(obj, QTextEdit):
                if event.key() == Qt.Key_Tab and not event.modifiers():
                    self.focusNextChild()
                    return True
                elif event.key() == Qt.Key_Backtab:
                    self.focusPreviousChild()
                    return True
            if isinstance(obj, QLineEdit):
                if event.key() in (Qt.Key_Tab, Qt.Key_Backtab):
                    self.last_nav_was_tab = True
                elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
                    self.last_nav_was_tab = True
                    self.focusNextChild()
                    return True
                else:
                    self.last_nav_was_tab = False

            elif not isinstance(obj, (QLineEdit, QTextEdit)):
                self.last_nav_was_tab = False
        elif event.type() == QEvent.MouseButtonPress:
            self.last_nav_was_tab = False
        return super().eventFilter(obj, event)

    def clear_form(self):
        self.opcode_combo.setCurrentIndex(0)

        for field, widget in self.field_inputs.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, BrailleInputWidget):
                widget.braille_input.clear()

        self.comment_input.clear()

        clearLayout(self.form_layout)
        self.field_inputs.clear()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        self.opcode_combo_layout = QHBoxLayout()

        self.opcode_combo = QComboBox()
        self.opcode_combo.setPlaceholderText("Select Opcode")
        self.populate_opcode_combo()
        self.opcode_combo.setCurrentIndex(0) 
        self.opcode_combo.currentIndexChanged.connect(self.on_opcode_selected)
        self.opcode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.opcode_combo_layout.addWidget(self.opcode_combo)
        main_layout.addLayout(self.opcode_combo_layout)

        self.form_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)

        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Add a comment (optional)")
        # Set size policy for full width
        self.comment_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        main_layout.addWidget(self.comment_input)

        self.add_button = QPushButton("Add")
        main_layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

    def populate_opcode_combo(self, combo=None):
        if combo is None:
            combo = self.opcode_combo
        combo.clear()
        combo.addItem("Select Opcode", None)
        for opcode in opcodes:
            combo.addItem(opcode["code"], opcode)

    def on_opcode_selected(self, index):
        clearLayout(self.form_layout)  
        if index > 0:
            opcode = self.opcode_combo.itemData(index)
            nested_form = OpcodeForm(opcode["fields"], self)
            self.form_layout.addWidget(nested_form)
            self.field_inputs["nested_form"] = nested_form
        self.install_input_event_filters()  

    def collect_entry_data(self):
        collected_data = [self.opcode_combo.currentText()]

        def collect_nested_form_data(nested_form):
            nested_data = []
            for field, widget in nested_form.field_inputs.items():
                if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                    nested_data.append(widget.text())
                elif isinstance(widget, QComboBox):
                    nested_data.append(widget.currentText())
                elif isinstance(widget, BrailleInputWidget):
                    nested_data.append(widget.braille_input.text())
                elif field == "exactdots":
                    at_symbol, braille_input = widget
                    nested_data.append(at_symbol.text() + braille_input.text())
                elif isinstance(widget, OpcodeForm):
                    nested_data.extend(collect_nested_form_data(widget))
            return nested_data

        for field, widget in self.field_inputs.items():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                collected_data.append(widget.text())
            elif isinstance(widget, QComboBox):
                collected_data.append(widget.currentText())
            elif isinstance(widget, BrailleInputWidget):
                collected_data.append(widget.braille_input.text())
            elif field == "exactdots":
                at_symbol, braille_input = widget
                collected_data.append(at_symbol.text() + braille_input.text())
            elif isinstance(widget, OpcodeForm):
                collected_data.extend(collect_nested_form_data(widget))

        collected_data.append(self.comment_input.text())

        return ' '.join(collected_data).strip()

    def get_focusable_widgets(self):
        widgets = []
        if hasattr(self, 'opcode_combo'):
            widgets.append(self.opcode_combo)
        if 'nested_form' in self.field_inputs and hasattr(self.field_inputs['nested_form'], 'get_focusable_widgets'):
            widgets.extend(self.field_inputs['nested_form'].get_focusable_widgets())
        if hasattr(self, 'comment_input'):
            widgets.append(self.comment_input)
        if hasattr(self, 'add_button'):
            widgets.append(self.add_button)
        return widgets

    def keyPressEvent(self, event):
        focusable = self.get_focusable_widgets()
        if not focusable:
            super().keyPressEvent(event)
            return
        current = self.focusWidget()
        try:
            idx = focusable.index(current)
        except ValueError:
            idx = -1
        if event.key() == Qt.Key_Tab and not event.isAutoRepeat():
            if event.modifiers() == Qt.ShiftModifier:
                if idx == 0:
                    p = self.parent()
                    if hasattr(p, 'table_preview'):
                        p.table_preview.setFocus()
                        event.accept()
                        return
                elif idx > 0:
                    focusable[idx-1].setFocus()
                    event.accept()
                    return
            else:
                if idx == len(focusable) - 1:
                    p = self.parent()
                    if hasattr(p, 'table_preview'):
                        p.table_preview.setFocus()
                        event.accept()
                        return
                elif idx < len(focusable) - 1:
                    focusable[idx+1].setFocus()
                    event.accept()
                    return
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if idx < len(focusable) - 1:
                focusable[idx+1].setFocus()
                event.accept()
                return
        super().keyPressEvent(event)
