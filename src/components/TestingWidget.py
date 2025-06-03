from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox, QTextEdit, QTabWidget
)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys
from .TestCaseWidget import TestCaseWidget

class TestingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_table = None
        self.find_liblouis()
        self.initUI()

    def find_liblouis(self):

        self.liblouis_base = "C:\\Program Files\\liblouis"
        self.tables_dir = os.path.join(self.liblouis_base, "share", "liblouis", "tables")
        
        if sys.platform == 'win32':
            self.translator_exe = os.path.join(self.liblouis_base, "bin", "lou_translate.exe")
        else:
            self.translator_exe = os.path.join(self.liblouis_base, "bin", "lou_translate")
            
        if not os.path.exists(self.translator_exe):
            self.liblouis_base = None
            self.tables_dir = None
            self.translator_exe = None

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(6, 6, 6, 6)
        
        tab_widget = QTabWidget()
        
        translation_widget = QWidget()
        translation_layout = QVBoxLayout()
        translation_layout.setSpacing(6)
        translation_layout.setContentsMargins(6, 6, 6, 6)
        
        forward_group = QVBoxLayout()
        forward_group.setSpacing(6)
        forward_group.setContentsMargins(6, 6, 6, 6)
        forward_label = QLabel("Forward Translation (Text to Braille):")
        
        forward_io_layout = QHBoxLayout()
        forward_io_layout.setSpacing(6)
        forward_io_layout.setContentsMargins(0, 0, 0, 0)
        
        forward_input_group = QVBoxLayout()
        forward_input_group.setSpacing(3)
        forward_input_group.setContentsMargins(0, 0, 0, 0)
        forward_input_label = QLabel("Input Text:")
        self.forward_input = QTextEdit(self)
        self.forward_input.setPlaceholderText("Enter text to translate")
        self.forward_input.setMaximumHeight(100)
        self.forward_input.keyPressEvent = self.handle_forward_key_press
        forward_input_group.addWidget(forward_input_label)
        forward_input_group.addWidget(self.forward_input)
        
        forward_output_group = QVBoxLayout()
        forward_output_group.setSpacing(3)
        forward_output_group.setContentsMargins(0, 0, 0, 0)
        forward_output_label = QLabel("Output Braille:")
        self.forward_output = QTextEdit(self)
        self.forward_output.setPlaceholderText("Braille output will appear here")
        self.forward_output.setMaximumHeight(100)
        self.forward_output.setReadOnly(True)
        forward_output_group.addWidget(forward_output_label)
        forward_output_group.addWidget(self.forward_output)
        
        forward_button_layout = QVBoxLayout()
        forward_button_layout.setSpacing(0)
        forward_button_layout.setContentsMargins(0, 45, 0, 0) 
        self.forward_button = QPushButton("→ Translate to Braille", self)
        self.forward_button.setObjectName("forward_button")
        self.forward_button.setToolTip("Click to translate text to Braille (or press Ctrl+Enter)")
        self.forward_button.setFixedSize(200, 40)
        forward_button_layout.addStretch(1)
        forward_button_layout.addWidget(self.forward_button)
        forward_button_layout.addStretch(1)
        
        forward_io_layout.addLayout(forward_input_group)
        forward_io_layout.addLayout(forward_output_group)
        forward_io_layout.addLayout(forward_button_layout)
        forward_io_layout.setAlignment(forward_button_layout, Qt.AlignVCenter)
        
        forward_group.addWidget(forward_label)
        forward_group.addLayout(forward_io_layout)
        
        backward_group = QVBoxLayout()
        backward_group.setSpacing(6)
        backward_group.setContentsMargins(6, 6, 6, 6)
        backward_label = QLabel("Backward Translation (Braille to Text):")
        
        backward_io_layout = QHBoxLayout()
        backward_io_layout.setSpacing(6)
        backward_io_layout.setContentsMargins(0, 0, 0, 0)
        
        backward_input_group = QVBoxLayout()
        backward_input_group.setSpacing(3)
        backward_input_group.setContentsMargins(0, 0, 0, 0)
        backward_input_label = QLabel("Input Braille:")
        self.backward_input = QTextEdit(self)
        self.backward_input.setPlaceholderText("Enter Braille using F, D, S, J, K, L keys for dots 1-6, space for next cell, double space for word space")
        self.backward_input.setMaximumHeight(100)
        self.backward_input.keyPressEvent = self.handle_braille_input
        self.current_braille_cell = [False] * 6 
        self.last_space_time = 0 
        backward_input_group.addWidget(backward_input_label)
        backward_input_group.addWidget(self.backward_input)
        
        backward_output_group = QVBoxLayout()
        backward_output_group.setSpacing(3)
        backward_output_group.setContentsMargins(0, 0, 0, 0)
        backward_output_label = QLabel("Output Text:")
        self.backward_output = QTextEdit(self)
        self.backward_output.setPlaceholderText("Text output will appear here")
        self.backward_output.setMaximumHeight(100)
        self.backward_output.setReadOnly(True)
        backward_output_group.addWidget(backward_output_label)
        backward_output_group.addWidget(self.backward_output)
        
        backward_button_layout = QVBoxLayout()
        backward_button_layout.setSpacing(0)
        backward_button_layout.setContentsMargins(0, 45, 0, 0)  
        self.backward_button = QPushButton("← Translate to Text", self)
        self.backward_button.setObjectName("backward_button")
        self.backward_button.setToolTip("Click to translate Braille to text (or press Ctrl+Enter)")
        self.backward_button.setFixedSize(200, 40)
        backward_button_layout.addStretch(1)
        backward_button_layout.addWidget(self.backward_button)
        backward_button_layout.addStretch(1)
        
        backward_io_layout.addLayout(backward_input_group)
        backward_io_layout.addLayout(backward_output_group)
        backward_io_layout.addLayout(backward_button_layout)
        backward_io_layout.setAlignment(backward_button_layout, Qt.AlignVCenter)
        
        backward_group.addWidget(backward_label)
        backward_group.addLayout(backward_io_layout)
        
        translation_layout.addLayout(forward_group)
        translation_layout.addLayout(backward_group)
        translation_widget.setLayout(translation_layout)
        
        self.test_case_widget = TestCaseWidget(self)
        
        tab_widget.addTab(translation_widget, "Translation")
        tab_widget.addTab(self.test_case_widget, "Test Cases")
        
        main_layout.addWidget(tab_widget)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
        self.forward_button.clicked.connect(self.translate_forward)
        self.backward_button.clicked.connect(self.translate_backward)
        
        self.update_status()
    
    def set_current_table(self, table_path):
        self.current_table = table_path
        self.current_table_path = table_path
        self.update_status()
    
    def update_status(self):
        if not self.translator_exe:
            self.status_label.setText("Error: liblouis not found")
            self.forward_button.setEnabled(False)
            self.backward_button.setEnabled(False)
            return
            
        if self.current_table:
            table_name = os.path.basename(self.current_table)
            self.status_label.setText(f"Using table: {table_name}")
            self.forward_button.setEnabled(True)
            self.backward_button.setEnabled(True)
        else:
            self.status_label.setText("No table selected")
            self.forward_button.setEnabled(False)
            self.backward_button.setEnabled(False)
    
    def translate_text(self, text, direction="forward"):
        if not self.translator_exe:
            QMessageBox.critical(self, "Error", "liblouis not found. Please install liblouis and try again.")
            return None
            
        if not self.current_table:
            QMessageBox.warning(self, "Error", "No translation table selected")
            return None
            
        if not text.strip():
            return ""
            
        try:
            # Use CREATE_NO_WINDOW flag to prevent command prompt from appearing
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            process = subprocess.Popen(
                [
                    self.translator_exe,
                    "--backward" if direction == "backward" else "--forward",
                    f"unicode.dis,{self.current_table}"
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                error_msg = stderr.strip() if stderr else "Unknown error occurred"
                QMessageBox.warning(self, "Error", f"Translation failed: {error_msg}")
                return None
            
            output = stdout.strip()
            if direction == "forward" and ("⠭" in output or "⡳" in output):
                QMessageBox.warning(self, "Translation Error", 
                    "Some characters in your input are not defined in the current table.\n"
                    f"Current table: {os.path.basename(self.current_table)}\n"
                    "Please check if you're using the correct table for these characters.")
                return None
            
            return output
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return None
    
    def handle_forward_key_press(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ControlModifier:
            self.translate_forward()
        else:
            QTextEdit.keyPressEvent(self.forward_input, event)
    
    def handle_braille_input(self, event):
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
            self.current_braille_cell[dot_pos] = True
            self.update_braille_cell()
        elif event.key() == Qt.Key_Space:
            current_time = event.timestamp()
            if current_time - self.last_space_time < 300:  
                self.add_word_space()
                self.last_space_time = 0 
            else:
                self.add_braille_cell()
                self.last_space_time = current_time
        elif event.key() == Qt.Key_Backspace:
            self.handle_backspace()
            event.accept()  
        else:
            QTextEdit.keyPressEvent(self.backward_input, event)
    
    def update_braille_cell(self):
        dots = self.current_braille_cell
        unicode_value = 0x2800
        if dots[0]: unicode_value |= 0x01
        if dots[1]: unicode_value |= 0x02
        if dots[2]: unicode_value |= 0x04
        if dots[3]: unicode_value |= 0x08
        if dots[4]: unicode_value |= 0x10
        if dots[5]: unicode_value |= 0x20
        
        current_text = self.backward_input.toPlainText()
        
        if not current_text:
            current_text = chr(unicode_value)
        else:
            current_text = current_text[:-1] + chr(unicode_value)
        
        self.backward_input.setPlainText(current_text)
        cursor = self.backward_input.textCursor()
        cursor.movePosition(cursor.End)
        self.backward_input.setTextCursor(cursor)
    
    def add_braille_cell(self):
        self.update_braille_cell()
        self.current_braille_cell = [False] * 6
        cursor = self.backward_input.textCursor()
        cursor.insertText(chr(0x2800))
        self.backward_input.setTextCursor(cursor)
    
    def add_word_space(self):
        current_text = self.backward_input.toPlainText()
        if current_text and current_text[-1] == chr(0x2800):
            current_text = current_text[:-1]
        self.backward_input.setPlainText(current_text + " ")
        cursor = self.backward_input.textCursor()
        cursor.movePosition(cursor.End)
        self.backward_input.setTextCursor(cursor)
        self.current_braille_cell = [False] * 6
    
    def handle_backspace(self):
        current_text = self.backward_input.toPlainText()
        if current_text:
            if any(self.current_braille_cell):
                self.current_braille_cell = [False] * 6
                self.update_braille_cell()
            else:
                self.backward_input.setPlainText(current_text[:-1])
                self.current_braille_cell = [False] * 6
    
    def translate_forward(self):
        forward_text = self.forward_input.toPlainText().strip()
        if forward_text:
            result = self.translate_text(forward_text, "forward")
            if result is not None:
                self.forward_output.setText(result)
        else:
            QMessageBox.warning(self, "Error", "Please enter text to translate")
    
    def translate_backward(self):
        backward_text = self.backward_input.toPlainText().strip()
        if backward_text:
            result = self.translate_text(backward_text, "backward")
            if result is not None:
                self.backward_output.setText(result)
        else:
            QMessageBox.warning(self, "Error", "Please enter Braille to translate")