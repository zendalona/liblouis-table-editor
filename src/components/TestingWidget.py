import louis
import os
import tempfile
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from utils.ApplyStyles import apply_styles

class TestingWidget(QWidget):
    def __init__(self, parent=None, get_table_content_callback=None):
        super().__init__(parent)
        self.get_table_content_callback = get_table_content_callback
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        self.forward_translation_input = QLineEdit(self)
        self.forward_translation_input.setPlaceholderText("Enter text (e.g., hello sir)")
        self.forward_translation_input.textChanged.connect(self.handle_forward_text_change)
        layout.addWidget(self.forward_translation_input)

        self.backward_translation_input = QLineEdit(self)
        self.backward_translation_input.setPlaceholderText("Enter Braille (e.g., ⠓⠑⠇⠇⠕⠀)")
        self.backward_translation_input.textChanged.connect(self.handle_backward_text_change)
        layout.addWidget(self.backward_translation_input)

        self.translate_button = QPushButton("Translate", self)
        self.translate_button.clicked.connect(self.perform_translation)
        layout.addWidget(self.translate_button)

        self.setLayout(layout)
        apply_styles(self)

    def handle_forward_text_change(self, text):
        if text.strip():
            self.backward_translation_input.blockSignals(True)
            self.backward_translation_input.clear()
            self.backward_translation_input.blockSignals(False)
            self.perform_translation(live_forward=True)

    def handle_backward_text_change(self, text):
        if text.strip():
            self.forward_translation_input.blockSignals(True)
            self.forward_translation_input.clear()
            self.forward_translation_input.blockSignals(False)
            self.perform_translation(live_backward=True)

    def perform_translation(self, live_forward=False, live_backward=False):
        table_content = self.get_table_content_callback() if self.get_table_content_callback else ""
        if not table_content.strip():
            return

        with tempfile.NamedTemporaryFile(mode='w', suffix='.tbl', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(table_content)
            temp_table_path = temp_file.name

        try:
            if live_forward:
                forward_text = self.forward_translation_input.text().strip()
                if not forward_text:
                    return
                result = louis.translate((temp_table_path,), forward_text, mode=louis.compbrlAtCursor)
                braille_text = result[0].decode('utf-8') if isinstance(result[0], bytes) else result[0]
                self.backward_translation_input.blockSignals(True)
                self.backward_translation_input.setText(braille_text or "")
                self.backward_translation_input.blockSignals(False)

            elif live_backward:
                backward_text = self.backward_translation_input.text().strip()
                if not backward_text:
                    return
                result = louis.backTranslate((temp_table_path,), backward_text, mode=louis.compbrlAtCursor)
                back_translated = result[0].decode('utf-8') if isinstance(result[0], bytes) else result[0]
                self.forward_translation_input.blockSignals(True)
                self.forward_translation_input.setText(back_translated or "")
                self.forward_translation_input.blockSignals(False)

            else:
                self.handle_translation_on_button_click(temp_table_path)

        except Exception as e:
            print(f"Translation error: {e}")
            self.forward_translation_input.setText(f"Error: {e}")
            self.backward_translation_input.setText(f"Error: {e}")

        finally:
            os.unlink(temp_table_path)

    def handle_translation_on_button_click(self, temp_table_path):
        forward_text = self.forward_translation_input.text().strip()
        backward_text = self.backward_translation_input.text().strip()

        if forward_text and not backward_text:
            result = louis.translate((temp_table_path,), forward_text, mode=louis.compbrlAtCursor)
            braille_text = result[0].decode('utf-8') if isinstance(result[0], bytes) else result[0]
            self.backward_translation_input.setText(braille_text or "No translation")

        elif backward_text and not forward_text:
            result = louis.backTranslate((temp_table_path,), backward_text, mode=louis.compbrlAtCursor)
            back_translated = result[0].decode('utf-8') if isinstance(result[0], bytes) else result[0]
            self.forward_translation_input.setText(back_translated or "No back-translation")

        elif forward_text and backward_text:
            print("Please use only one input field at a time.")
            self.forward_translation_input.setText("Error: Use one field only")
            self.backward_translation_input.setText("Error: Use one field only")

        else:
            print("Please enter text in one of the fields.")
            self.forward_translation_input.setText("Error: Enter text")
            self.backward_translation_input.setText("Error: Enter Braille")
