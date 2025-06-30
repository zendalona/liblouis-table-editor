from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTextEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, QEvent
import unicodedata
import re
import time

class TestCaseWidget(QWidget):
    def __init__(self, testing_widget, parent=None):
        super().__init__(parent)
        self.testing_widget = testing_widget
        self.test_cases = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        labels_row = QHBoxLayout()
        input_label = QLabel("Test Input:")
        output_label = QLabel("Expected Braille:")
        labels_row.addWidget(input_label)
        labels_row.addStretch(1)
        labels_row.addWidget(output_label)
        labels_row.addStretch(2) 
        layout.addLayout(labels_row)

        input_fields_row = QHBoxLayout()

        input_group = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter test input text")
        self.input_text.setMaximumHeight(100)
        self.input_text.installEventFilter(self)
        input_group.addWidget(self.input_text)

        output_group = QVBoxLayout()
        self.expected_output = QTextEdit()
        self.expected_output.setPlaceholderText("Enter expected Braille output using F, D, S, J, K, L keys for dots 1-6, space for next cell, double space for word space")
        self.expected_output.setMaximumHeight(100)
        self.expected_output.keyPressEvent = self.handle_expected_braille_input
        self.current_expected_braille_cell = [False] * 6  
        self.last_expected_space_time = 0  
        self.expected_output.installEventFilter(self)
        output_group.addWidget(self.expected_output)

        button_column_layout = QVBoxLayout()
        self.add_test_button = QPushButton("Add Test Case")
        self.run_tests_button = QPushButton("Run All Tests")
        button_column_layout.addWidget(self.add_test_button)
        button_column_layout.addStretch(1)
        button_column_layout.addWidget(self.run_tests_button)

        button_column_widget = QWidget()
        button_column_widget.setLayout(button_column_layout)
        max_height = max(self.input_text.maximumHeight(), self.expected_output.maximumHeight())
        button_column_widget.setMaximumHeight(max_height)
        button_column_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        input_fields_row.addLayout(input_group)
        input_fields_row.addLayout(output_group)
        input_fields_row.addWidget(button_column_widget)
        input_fields_row.setAlignment(button_column_widget, Qt.AlignTop)

        layout.addLayout(input_fields_row)

        self.test_table = QTableWidget()
        self.test_table.setColumnCount(4)
        self.test_table.setHorizontalHeaderLabels(["Input", "Expected", "Result", "Status"])
        header = self.test_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.test_table.setObjectName("test_table")
        self.test_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.test_table)

        self.setLayout(layout)

        self.add_test_button.clicked.connect(self.add_test_case)
        self.run_tests_button.clicked.connect(self.run_all_tests)

    def add_test_case(self):
        input_text = self.input_text.toPlainText().strip()
        expected = self.expected_output.toPlainText().strip()
        
        if not input_text or not expected:
            QMessageBox.warning(self, "Error", "Please enter both input text and expected output")
            return
        
        self.test_cases.append({
            'input': input_text,
            'expected': expected,
            'result': '',
            'status': 'Not Run'
        })
        
        self.update_test_table()
        
        self.input_text.clear()
        self.expected_output.clear()

    def update_test_table(self):
        self.test_table.setRowCount(len(self.test_cases))
        
        for row, test_case in enumerate(self.test_cases):
            self.test_table.setItem(row, 0, QTableWidgetItem(test_case['input']))
            self.test_table.setItem(row, 1, QTableWidgetItem(test_case['expected']))
            self.test_table.setItem(row, 2, QTableWidgetItem(test_case['result']))
            status_item = QTableWidgetItem(test_case['status'])
            if test_case['status'] == 'Pass':
                status_item.setBackground(Qt.green)
            elif test_case['status'] == 'Fail':
                status_item.setBackground(Qt.red)
            self.test_table.setItem(row, 3, status_item)

    def normalize_braille(self, text):
        if not text:
            return ''
        # Replace all Unicode space characters (including Braille blank) with a regular space
        # Unicode spaces: https://en.wikipedia.org/wiki/Whitespace_character#Unicode
        # Braille pattern blank: U+2800
        text = re.sub(r'[\s\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000\u2800]', ' ', text)
        text = ' '.join(text.split())
        text = unicodedata.normalize('NFC', text)
        return text.strip()

    def run_all_tests(self):
        if not self.test_cases:
            QMessageBox.information(self, "Info", "No test cases to run")
            return
        
        for i, test_case in enumerate(self.test_cases):
            self.testing_widget.forward_input.setPlainText(test_case['input'])
            self.testing_widget.translate_forward()
            result = self.testing_widget.forward_output.toPlainText()
            
            expected_norm = self.normalize_braille(test_case['expected'])
            result_norm = self.normalize_braille(result)
            
            self.test_cases[i]['result'] = result
            self.test_cases[i]['status'] = 'Pass' if result_norm == expected_norm else 'Fail'
        
        self.update_test_table()
        
        passes = sum(1 for test in self.test_cases if test['status'] == 'Pass')
        total = len(self.test_cases)
        QMessageBox.information(self, "Test Results", 
            f"Tests completed: {total}\nPassed: {passes}\nFailed: {total - passes}")

    def handle_expected_braille_input(self, event):
        key_to_dot = {
            Qt.Key_F: 0,  # Dot 1
            Qt.Key_D: 1,  # Dot 2
            Qt.Key_S: 2,  # Dot 3
            Qt.Key_J: 3,  # Dot 4
            Qt.Key_K: 4,  # Dot 5
            Qt.Key_L: 5,  # Dot 6
        }
        
        if event.key() in key_to_dot:
            dot_pos = key_to_dot[event.key()]
            self.current_expected_braille_cell[dot_pos] = True
            self.update_expected_braille_cell()
        elif event.key() == Qt.Key_Space:
            current_time = int(time.time() * 1000)
            if current_time - self.last_expected_space_time < 300:
                self.add_expected_word_space()
                self.last_expected_space_time = 0
            else:
                self.add_expected_braille_cell()
                self.last_expected_space_time = current_time
        elif event.key() == Qt.Key_Backspace:
            self.handle_expected_backspace()
            event.accept()
        else:
            QTextEdit.keyPressEvent(self.expected_output, event)

    def update_expected_braille_cell(self):
        dots = self.current_expected_braille_cell
        unicode_value = 0x2800
        if dots[0]: unicode_value |= 0x01
        if dots[1]: unicode_value |= 0x02
        if dots[2]: unicode_value |= 0x04
        if dots[3]: unicode_value |= 0x08
        if dots[4]: unicode_value |= 0x10
        if dots[5]: unicode_value |= 0x20
        current_text = self.expected_output.toPlainText()
        if not current_text:
            current_text = chr(unicode_value)
        else:
            current_text = current_text[:-1] + chr(unicode_value)
        self.expected_output.setPlainText(current_text)
        cursor = self.expected_output.textCursor()
        cursor.movePosition(cursor.End)
        self.expected_output.setTextCursor(cursor)

    def add_expected_braille_cell(self):
        self.update_expected_braille_cell()
        self.current_expected_braille_cell = [False] * 6
        cursor = self.expected_output.textCursor()
        cursor.insertText(chr(0x2800))
        self.expected_output.setTextCursor(cursor)

    def add_expected_word_space(self):
        current_text = self.expected_output.toPlainText()
        if current_text and current_text[-1] == chr(0x2800):
            current_text = current_text[:-1]
        self.expected_output.setPlainText(current_text + " ")
        cursor = self.expected_output.textCursor()
        cursor.movePosition(cursor.End)
        self.expected_output.setTextCursor(cursor)
        self.current_expected_braille_cell = [False] * 6

    def handle_expected_backspace(self):
        current_text = self.expected_output.toPlainText()
        if current_text:
            if any(self.current_expected_braille_cell):
                self.current_expected_braille_cell = [False] * 6
                self.update_expected_braille_cell()
            else:
                self.expected_output.setPlainText(current_text[:-1])
                self.current_expected_braille_cell = [False] * 6 

    def eventFilter(self, obj, event):

        if isinstance(obj, QTextEdit) and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Tab and not event.modifiers():
                self.focusNextChild()
                return True
            elif event.key() == Qt.Key_Backtab:
                self.focusPreviousChild()
                return True
        return super().eventFilter(obj, event) 
