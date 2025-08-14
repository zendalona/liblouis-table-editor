import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QTextEdit, QLineEdit, QComboBox, QShortcut, QPushButton, QLabel, QMessageBox, QSplitter, QApplication
)
from PyQt5.QtGui import QKeyEvent, QFont, QKeySequence
from PyQt5.QtCore import Qt
from liblouis_table_editor.components.AddEntry.AddEntryWidget import AddEntryWidget
from liblouis_table_editor.components.AddEntry.BrailleInputWidget import BrailleInputWidget
from liblouis_table_editor.components.TablePreview import TablePreview
from liblouis_table_editor.components.TestingWidget import TestingWidget
from liblouis_table_editor.utils.ApplyStyles import apply_styles
from liblouis_table_editor.utils.Toast import Toast
from liblouis_table_editor.utils.asset_utils import get_icon_for_toast
from liblouis_table_editor.components.HelpDialogs import LiblouisInstallDialog


class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._unsaved_changes = False
        self._original_content = None
        self._current_font_size = 10  
        self._undo_stack = []
        self._redo_stack = []
        self.liblouis_found = self.check_liblouis()
        self.initUI()

    def check_liblouis(self):
        import sys, os, shutil
        if sys.platform == 'win32':
            translator_exe = os.path.join("C:\\Program Files\\liblouis", "bin", "lou_translate.exe")
            return os.path.exists(translator_exe)
        else:
            if os.path.exists("/usr/bin/lou_translate"):
                return True
            if shutil.which('lou_translate'):
                return True
            return False

    def initUI(self):
        main_layout = QVBoxLayout()

        if not self.liblouis_found:
            while True:
                dialog = LiblouisInstallDialog(self)
                dialog.exec_()

                self.liblouis_found = self.check_liblouis()
                if self.liblouis_found:
                    break

                res = QMessageBox.question(self, "Liblouis Not Found", "liblouis is still not installed. Retry installation?", QMessageBox.Retry | QMessageBox.Close, QMessageBox.Retry)
                if res == QMessageBox.Close:
                    break  

        if not self.liblouis_found:
            self.liblouis_warning_label = QLabel("<b style='color: #d32f2f;'>Warning: Liblouis is not installed. Some features will not work.</b>")
            self.liblouis_warning_label.setAccessibleName("Liblouis Warning Label")
            self.liblouis_warning_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(self.liblouis_warning_label)

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setAccessibleName("Main Window Splitter")
        main_splitter.setObjectName("main_splitter")
        
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setAccessibleName("Top Section Splitter")
        top_splitter.setObjectName("top_splitter")

        self.table_preview = TablePreview(self)
        self.table_preview.setAccessibleName("Table Preview Widget")
        self.table_preview.setObjectName("table_preview")
        self.table_preview.setMinimumWidth(250)
        self.table_preview.setMinimumHeight(200)
        top_splitter.addWidget(self.table_preview)

        self.add_entry_widget = AddEntryWidget()
        self.add_entry_widget.setAccessibleName("Add Entry Widget")
        self.add_entry_widget.setObjectName("add_entry_widget")
        self.add_entry_widget.add_button.clicked.connect(self.add_entry)
        self.add_entry_widget.clear_button.clicked.connect(self.clear_editor_form)
        self.add_entry_widget.setMinimumWidth(300)
        self.add_entry_widget.setMinimumHeight(200)
        top_splitter.addWidget(self.add_entry_widget)

        # Set top splitter to balanced middle position (50-50 split)
        top_splitter.setSizes([500, 500])  # Equal split for top panels
        
        main_splitter.addWidget(top_splitter)

        self.testing_widget = TestingWidget(self)
        self.testing_widget.setAccessibleName("Translation Widget")
        self.testing_widget.setObjectName("testing_widget")
        self.testing_widget.setMinimumHeight(150)  # Reduced from 200 to 150
        self.testing_widget.setMinimumWidth(400)
        main_splitter.addWidget(self.testing_widget)

        # Remove predefined sizes - let panels use natural sizing  
        # main_splitter.setSizes([650, 350])  # Commented out for natural sizing
        
        main_splitter.setChildrenCollapsible(False)
        top_splitter.setChildrenCollapsible(False)
        
        main_splitter.setHandleWidth(6)
        top_splitter.setHandleWidth(6)
        
        main_splitter.setStretchFactor(0, 2)  
        main_splitter.setStretchFactor(1, 1)  
        
        top_splitter.setStretchFactor(0, 1)  
        top_splitter.setStretchFactor(1, 2) 
        
        main_layout.addWidget(main_splitter)

        self.main_splitter = main_splitter
        self.top_splitter = top_splitter

        self.setLayout(main_layout)

        self.add_entry_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.add_entry_shortcut.activated.connect(self.add_entry)
        self.add_entry_shortcut2 = QShortcut(QKeySequence("Ctrl+Enter"), self)
        self.add_entry_shortcut2.activated.connect(self.add_entry)

        apply_styles(self)

        self.toast = None

    def validate_entry_data(self, entry_data):
        if not entry_data:
            return False
        
    
        if isinstance(entry_data, dict):
            if 'opcode' not in entry_data:
                return False
            
            return True
        elif isinstance(entry_data, str):
            return bool(entry_data.strip())
        return False

    def add_entry(self):
        entry_data = self.add_entry_widget.collect_entry_data()
        if not self.validate_entry_data(entry_data):
            self.show_toast("Invalid entry data! (Ctrl+Enter to add entry)", get_icon_for_toast('error'), 255, 0, 0)
            return
        
        # Check if we're in editing mode
        if hasattr(self.table_preview, 'is_editing_mode') and self.table_preview.is_editing_mode:
            self.update_current_entry(entry_data)
        else:
            self._save_state_for_undo()
            self.table_preview.add_entry(entry_data)
            self.mark_as_unsaved()
            self.show_toast("Entry added successfully! (Ctrl+Enter to add entry)", get_icon_for_toast('success'), 75, 175, 78)

    def update_current_entry(self, entry_data):
        """Update the currently selected entry in the table preview"""
        if hasattr(self.table_preview, 'current_index') and 0 <= self.table_preview.current_index < len(self.table_preview.entries):
            self._save_state_for_undo()
            # Update the entry in place without re-sorting
            self.table_preview.update_current_entry(entry_data)
            self.table_preview.is_editing_mode = False  # Exit editing mode
            # Clear the form after successful update
            self.clear_editor_form()
            self.show_toast("Entry updated successfully!", get_icon_for_toast('success'), 75, 175, 78)
        else:
            # Fallback to adding new entry
            self._save_state_for_undo()
            self.table_preview.add_entry(entry_data)
            self.mark_as_unsaved()
            self.show_toast("Entry added successfully! (Ctrl+Enter to add entry)", get_icon_for_toast('success'), 75, 175, 78)

    def clear_editor_form(self):
        """Clear the add entry form and exit editing mode"""
        # Only clear if not already being cleared to avoid recursion
        if not hasattr(self, '_clearing_form') or not self._clearing_form:
            self._clearing_form = True
            self.add_entry_widget.clear_form()
            if hasattr(self.table_preview, 'clear_selection'):
                self.table_preview.clear_selection()
            self._clearing_form = False

    def _save_state_for_undo(self):
        current_content = self.get_content().copy() if isinstance(self.get_content(), list) else self.get_content()
        self._undo_stack.append(current_content)
        self._redo_stack = []

    def save_entries(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                if isinstance(self.table_preview.entries, list):
                    content = '\n'.join(self.table_preview.entries)
                    file.write(content)
                else:
                    json.dump(self.table_preview.entries, file, ensure_ascii=False, indent=2)
            
            self.mark_as_saved()
            
            self.testing_widget.set_current_table(file_path)
            
            self.show_toast("File saved successfully!", get_icon_for_toast('success'), 75, 175, 78)
            
            return True
        except Exception as e:
            self.show_toast(f"Error saving file: {str(e)}", get_icon_for_toast('error'), 255, 0, 0)
            return False

    def load_entries(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    self.table_preview.entries = []
                else:
                    try:
                        self.table_preview.entries = json.loads(content)
                    except json.JSONDecodeError:
                        self.table_preview.entries = [line for line in content.splitlines() if line.strip()]
                # Mark as fresh load so scroll position resets to top
                self.table_preview._fresh_load = True
                self.table_preview.update_content()
                
            self.testing_widget.set_current_table(file_path)
            self.show_toast("File loaded successfully!", get_icon_for_toast('success'), 75, 175, 78)
            
            self.mark_as_saved()
        except FileNotFoundError:
            self.show_toast("Error: File not found", get_icon_for_toast('error'), 255, 0, 0)
        except Exception as e:
            self.show_toast(f"Error loading file: {str(e)}", get_icon_for_toast('error'), 255, 0, 0)

    def set_content(self, content):
        try:
            if not content or not content.strip():
                self.table_preview.entries = []
            else:
                try:
                    self.table_preview.entries = json.loads(content)
                except json.JSONDecodeError:
                    self.table_preview.entries = [line for line in content.splitlines() if line.strip()]
            # Mark as fresh load so scroll position resets to top
            self.table_preview._fresh_load = True
            self.table_preview.update_content()
            self._original_content = self.get_content()
            self._unsaved_changes = False
        except Exception as e:
            self.show_toast(f"Error setting content: {str(e)}", get_icon_for_toast('error'), 255, 0, 0)

    def get_content(self):
        try:
            return self.table_preview.entries
        except Exception:
            return []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.add_entry()
        super().keyPressEvent(event)  

    def show_toast(self, text, icon_path, colorR, colorG, colorB):
        try:
            if self.toast:
                self.toast.close()
                self.toast.deleteLater()  
            icon_path = os.path.normpath(icon_path)  
            self.toast = Toast(text, icon_path, colorR, colorG, colorB, self)
            
            main_window = self.window()
            if main_window:
                toast_x = main_window.x() + (main_window.width() - self.toast.width()) // 2
                toast_y = main_window.y() + (main_window.height() - self.toast.height()) // 2
                self.toast.move(toast_x, toast_y)
            
            self.toast.show_toast()
        except Exception as e:
            pass

    def load_entry_into_editor(self, entry):
        self.add_entry_widget._programmatic_update = True  # Prevent popups
        self.add_entry_widget.clear_form()

        # Handle empty or whitespace-only entries
        if not entry or not entry.strip():
            self.add_entry_widget.set_editing_mode(True)
            self.add_entry_widget._programmatic_update = False
            return

        entry_text = entry.strip()
        parts = entry_text.split()
        if not parts:
            self.add_entry_widget.set_editing_mode(True)
            self.add_entry_widget._programmatic_update = False
            return

        # Check if the entry starts with a comment (like "# some comment")
        if entry_text.startswith('#'):
            # Entire entry is a comment
            self.add_entry_widget.comment_input.setText(entry_text)
            self.add_entry_widget.set_editing_mode(True)
            self.add_entry_widget._programmatic_update = False
            return

        # Look for comment starting with # anywhere in the entry
        comment_text = ""
        
        for i, part in enumerate(parts):
            if part.startswith('#'):
                comment_text = " ".join(parts[i:])  # Everything from # onwards
                parts = parts[:i]  # Remove comment from main parts
                break

        # Check if we still have parts after removing comments
        if not parts:
            # Entry became empty after removing comments - treat as comment-only
            if comment_text:
                self.add_entry_widget.comment_input.setText(comment_text)
            else:
                self.add_entry_widget.comment_input.setText(entry_text)
            self.add_entry_widget.set_editing_mode(True)
            self.add_entry_widget._programmatic_update = False
            return

        opcode = parts[0]
        index = self.add_entry_widget.opcode_combo.findText(opcode)
        if index != -1 and index != 0:
            self.add_entry_widget.opcode_combo.setCurrentIndex(index)
            
            # Wait for the form to be created
            QApplication.processEvents()

            nested_form = self.add_entry_widget.field_inputs.get("nested_form")
            if nested_form:
                form_data = parts[1:]
                self.fill_form_data(nested_form, form_data)
        else:
            # If no valid opcode found, put everything in comment
            comment_text = entry_text
            
        # Always set the comment text if we found one
        if comment_text:
            self.add_entry_widget.comment_input.setText(comment_text)
            
        # Set editing mode
        self.add_entry_widget.set_editing_mode(True)
        self.add_entry_widget._programmatic_update = False  # Re-enable popups

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
        if self._unsaved_changes:
            return True
        current_content = self.get_content()
        return current_content != self._original_content
        
    def mark_as_saved(self):
        self._original_content = self.get_content()
        self._unsaved_changes = False
        
    def mark_as_unsaved(self):
        self._unsaved_changes = True
        
    def undo(self):
        if self._undo_stack:
            current_content = self.get_content().copy() if isinstance(self.get_content(), list) else self.get_content()
            self._redo_stack.append(current_content)
            
            previous_state = self._undo_stack.pop()
            self.table_preview.entries = previous_state
            self.table_preview.update_content()
            self.mark_as_unsaved()
            self.show_toast("Action undone", get_icon_for_toast('success'), 75, 175, 78)
        else:
            self.show_toast("Nothing to undo", get_icon_for_toast('info'), 0, 0, 255)
            
    def redo(self):
        if self._redo_stack:
            current_content = self.get_content().copy() if isinstance(self.get_content(), list) else self.get_content()
            self._undo_stack.append(current_content)
            
            next_state = self._redo_stack.pop()
            self.table_preview.entries = next_state
            self.table_preview.update_content()
            self.mark_as_unsaved()
            self.show_toast("Action redone", get_icon_for_toast('success'), 75, 175, 78)
        else:
            self.show_toast("Nothing to redo", get_icon_for_toast('info'), 0, 0, 255)
            
    def go_to_entry(self, entry_text):
        if not entry_text:
            return
            
        for i, entry in enumerate(self.table_preview.entries):
            if entry_text in str(entry):
                self.table_preview.select_entry(i)
                self.show_toast(f"Found entry: {entry_text}", get_icon_for_toast('success'), 75, 175, 78)
                return
                
        self.show_toast(f"Entry not found: {entry_text}", get_icon_for_toast('error'), 255, 0, 0)
        
    def find_text(self, search_text):
        if not search_text:
            return
            
        for i, entry in enumerate(self.table_preview.entries):
            if search_text in str(entry):
                self.table_preview.select_entry(i)
                self.show_toast(f"Found text: {search_text}", get_icon_for_toast('success'), 75, 175, 78)
                return
                
        self.show_toast(f"Text not found: {search_text}", get_icon_for_toast('error'), 255, 0, 0)
        
    def find_replace(self, find_text, replace_text):
        if not find_text:
            return
            
        replaced_count = 0
        for i, entry in enumerate(self.table_preview.entries):
            if find_text in str(entry):

                if isinstance(entry, str):
                    new_entry = entry.replace(find_text, replace_text)
                    self.table_preview.entries[i] = new_entry
                    replaced_count += 1
                    
        if replaced_count > 0:
            self.table_preview.update_content()
            self.mark_as_unsaved()
            self.show_toast(f"Replaced {replaced_count} occurrences", get_icon_for_toast('success'), 75, 175, 78)
        else:
            self.show_toast(f"Text not found: {find_text}", get_icon_for_toast('error'), 255, 0, 0)
            
    def change_font_size(self, increase=True):
        if increase:
            self._current_font_size += 1
        else:
            self._current_font_size = max(8, self._current_font_size - 1)  
            
        self.table_preview.update_font_size(self._current_font_size)
        
        self.table_preview.scroll_area.updateGeometry()
        self.table_preview.scroll_widget.adjustSize()
        self.table_preview.update()
            
        self.show_toast(f"Font size: {self._current_font_size}pt", get_icon_for_toast('success'), 75, 175, 78)

    def show_liblouis_install_dialog(self):
        pass

    def save_splitter_state(self):
        """Save the current splitter positions"""
        try:
            main_sizes = self.main_splitter.sizes()
            top_sizes = self.top_splitter.sizes()
            return {
                'main_splitter': main_sizes,
                'top_splitter': top_sizes
            }
        except Exception:
            return None

    def restore_splitter_state(self, state):

        try:
            if state and isinstance(state, dict):
                if 'main_splitter' in state:
                    self.main_splitter.setSizes(state['main_splitter'])
                if 'top_splitter' in state:
                    self.top_splitter.setSizes(state['top_splitter'])
        except Exception:
            pass

    def reset_splitter_layout(self):
        """Reset splitter to natural sizing instead of predefined ratios"""
        # Set top splitter to balanced middle position (50-50 split)
        self.top_splitter.setSizes([500, 500])  # Equal split for top panels
        
        # For main splitter, use natural proportional sizing without forcing extra height
        # Let it use the natural content-based sizing  