from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, 
    QPushButton, QLabel, QMessageBox
)
import os
import subprocess
import sys

class TestingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_table = None
        self.find_liblouis()
        self.initUI()

    def find_liblouis(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        possible_paths = [
            os.path.join(project_root, "liblouis"),
        ]
        
        
        for base_path in possible_paths:
            if os.path.exists(base_path):
                if sys.platform == 'win32':
                    translator = os.path.join(base_path, "bin", "lou_translate.exe")
                else:
                    translator = os.path.join(base_path, "bin", "lou_translate")
                
                if os.path.exists(translator):
                    self.liblouis_base = base_path
                    self.tables_dir = os.path.join(base_path, "share", "liblouis", "tables")
                    self.translator_exe = translator
                    return
        
        self.liblouis_base = None
        self.tables_dir = None
        self.translator_exe = None

    def initUI(self):
        main_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        
        forward_layout = QVBoxLayout()
        forward_label = QLabel("Forward Translation:")
        self.forward_translation_input = QLineEdit(self)
        self.forward_translation_input.setPlaceholderText("Enter text to translate")
        forward_layout.addWidget(forward_label)
        forward_layout.addWidget(self.forward_translation_input)
        input_layout.addLayout(forward_layout)
        
        backward_layout = QVBoxLayout()
        backward_label = QLabel("Backward Translation:")
        self.backward_translation_input = QLineEdit(self)
        self.backward_translation_input.setPlaceholderText("Enter Braille to translate back to text")
        backward_layout.addWidget(backward_label)
        backward_layout.addWidget(self.backward_translation_input)
        input_layout.addLayout(backward_layout)
        
        main_layout.addLayout(input_layout)
        
        self.translate_button = QPushButton("⇄ Translate", self)
        self.translate_button.setObjectName("translate_button")
        self.translate_button.setToolTip("Click to translate (or press Enter)")
        input_layout.addWidget(self.translate_button)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
        
        self.translate_button.clicked.connect(self.translate)
        self.forward_translation_input.returnPressed.connect(self.translate)
        self.backward_translation_input.returnPressed.connect(self.translate)
        
        self.update_status()
    
    def set_current_table(self, table_path):
        self.current_table = table_path
        self.current_table_path = table_path
        self.update_status()
    
    def update_status(self):
        if not self.translator_exe:
            self.status_label.setText("Error: liblouis not found")
            self.translate_button.setEnabled(False)
            return
            
        if self.current_table:
            table_name = os.path.basename(self.current_table)
            self.status_label.setText(f"Using table: {table_name}")
            self.translate_button.setEnabled(True)
        else:
            self.status_label.setText("No table selected")
            self.translate_button.setEnabled(False)
    
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
                encoding='utf-8'
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
    
    def translate(self):
        forward_text = self.forward_translation_input.text().strip()
        backward_text = self.backward_translation_input.text().strip()
        
        if forward_text:
            result = self.translate_text(forward_text, "forward")
            if result is not None:
                self.backward_translation_input.setText(result)
        elif backward_text:
            result = self.translate_text(backward_text, "backward")
            if result is not None:
                self.forward_translation_input.setText(result)
        else:
            QMessageBox.warning(self, "Error", "Please enter text in either field to translate")