import os
<<<<<<< HEAD
from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

def create_action(parent, title, icon_path=None, shortcut=None, status_tip=None, triggered=None):
    action = QAction(title, parent)
    if icon_path:
        action.setIcon(QIcon(icon_path))
    if shortcut:
        action.setShortcut(shortcut)
=======
from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from components.HelpDialogs import AboutDialog, UserGuideDialog, ReportBugDialog

def create_action(parent, title, icon_path=None, shortcut=None, status_tip=None, triggered=None):
    action = QAction(title, parent)
    if icon_path and os.path.exists(icon_path):
        action.setIcon(QIcon(icon_path))
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
>>>>>>> liblouis/main
    if status_tip:
        action.setStatusTip(status_tip)
    if triggered:
        action.triggered.connect(triggered)
    return action

def add_menu_with_actions(menubar, title, actions):
    menu = menubar.addMenu(title)
    for action in actions:
        if action == 'separator':
            menu.addSeparator()
        else:
            menu.addAction(action)
    return menu

def create_menubar(parent):
    menubar = QMenuBar(parent)

    icon_base_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons')

    menu_structure = {
        'File': [
<<<<<<< HEAD
            ('New', os.path.join(icon_base_path, 'new.png'), 'Ctrl+N', None, lambda: open_new_file_dialog(parent)),
            ('Open', os.path.join(icon_base_path, 'open.png'), 'Ctrl+O', None, lambda: open_file_dialog(parent)),
            ('Save', os.path.join(icon_base_path, 'save.png'), 'Ctrl+S', None, lambda: save_file_dialog(parent)),
            ('Save As', os.path.join(icon_base_path, 'save_as.png'), 'Ctrl+Shift+S', None, lambda: save_as_file_dialog(parent))
        ],
        'Edit': [
            ('Undo', os.path.join(icon_base_path, 'undo.png'), 'Ctrl+Z', None, None),
            ('Redo', os.path.join(icon_base_path, 'redo.png'), 'Ctrl+Y', None, None),
            'separator',
            ('Go to Entry', os.path.join(icon_base_path, 'go_to_entry.png'), 'Ctrl+I', None, None),
            ('Find', os.path.join(icon_base_path, 'find.png'), 'Ctrl+F', None, None),
            ('Find and Replace', os.path.join(icon_base_path, 'find_replace.png'), 'Ctrl+H', None, None)
        ],
        'Tools': [
            ('Increase Font Size', os.path.join(icon_base_path, 'increase_font.png'), 'Ctrl+]', None, None),
            ('Decrease Font Size', os.path.join(icon_base_path, 'decrease_font.png'), 'Ctrl+[', None, None)
        ],
        'Help': [
            ('About', os.path.join(icon_base_path, 'about.png'), None, None, None),
            ('Report a bug', os.path.join(icon_base_path, 'report_bug.png'), None, None, None),
            ('User Guide', os.path.join(icon_base_path, 'user_guide.png'), None, None, None)
        ]
    }

    # Add menus and actions
    for menu_title, actions in menu_structure.items():
        action_list = []
        for action in actions:
            if action == 'separator':
                action_list.append('separator')
            else:
                title, icon_path, shortcut, status_tip, triggered = action
                action_list.append(create_action(parent, title, icon_path, shortcut, status_tip, triggered))
        add_menu_with_actions(menubar, menu_title, action_list)
=======
            ('New', os.path.join(icon_base_path, 'new.png'), 'Ctrl+N', 'Create a new table file', lambda: open_new_file_dialog(parent)),
            ('Open', os.path.join(icon_base_path, 'open.png'), 'Ctrl+O', 'Open an existing table file', lambda: open_file_dialog(parent)),
            ('Save', os.path.join(icon_base_path, 'save.png'), 'Ctrl+S', 'Save the current table', lambda: save_file_dialog(parent)),
            ('Save As', os.path.join(icon_base_path, 'save_as.png'), 'Ctrl+Shift+S', 'Save the current table with a new name', lambda: save_as_file_dialog(parent)),
            'separator',
            ('Exit', os.path.join(icon_base_path, 'exit.png'), 'Alt+F4', 'Exit the application', lambda: parent.close())
        ],
        'Edit': [
            ('Undo', os.path.join(icon_base_path, 'undo.png'), 'Ctrl+Z', 'Undo the last action', lambda: undo_action(parent)),
            ('Redo', os.path.join(icon_base_path, 'redo.png'), 'Ctrl+Y', 'Redo the last undone action', lambda: redo_action(parent)),
            'separator',
            ('Go to Entry', os.path.join(icon_base_path, 'go_to_entry.png'), 'Ctrl+I', 'Go to a specific entry', lambda: go_to_entry(parent)),
            ('Find', os.path.join(icon_base_path, 'find.png'), 'Ctrl+F', 'Find text in the current table', lambda: find_text(parent)),
            ('Find and Replace', os.path.join(icon_base_path, 'find_replace.png'), 'Ctrl+H', 'Find and replace text', lambda: find_replace(parent))
        ],
         'Tools': [
            ('Increase Font Size', os.path.join(icon_base_path, 'increase_font.png'), 'Ctrl+]', 'Increase the font size', lambda: change_font_size(parent, True)),
            ('Decrease Font Size', os.path.join(icon_base_path, 'decrease_font.png'), 'Ctrl+[', 'Decrease the font size', lambda: change_font_size(parent, False))
        ],
        'Help': [
            ('About', os.path.join(icon_base_path, 'about.png'), 'F1', 'About this application', lambda: AboutDialog(parent).exec_()),
            ('User Guide', os.path.join(icon_base_path, 'user_guide.png'), 'F2', 'View the user guide', lambda: UserGuideDialog(parent).exec_()),
            ('Report a bug', os.path.join(icon_base_path, 'report_bug.png'), 'F3', 'Report a bug', lambda: ReportBugDialog(parent).exec_())
        ]
    }

    for menu_title, actions in menu_structure.items():
        menu = menubar.addMenu(menu_title)
        
        for action in actions:
            if action == 'separator':
                menu.addSeparator()
            elif isinstance(action, QAction):
                menu.addAction(action)
            else:
                title, icon_path, shortcut, status_tip, triggered = action
                menu_action = create_action(parent, title, icon_path, shortcut, status_tip, triggered)
                menu_action.setToolTip(f"{menu_title} - {title}")
                menu_action.setStatusTip(status_tip or f"{menu_title} - {title}")
                menu.addAction(menu_action)
>>>>>>> liblouis/main

    return menubar

def open_new_file_dialog(parent):
<<<<<<< HEAD
    file_dialog = QFileDialog(parent)
    file_dialog.setFileMode(QFileDialog.AnyFile)
    file_dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

    if file_dialog.exec_():
        file_names = file_dialog.selectedFiles()
        if file_names:
            file_path = file_names[0]
            try:
                open(file_path, 'w').close()  
                file_name = os.path.basename(file_path)
                parent.add_tab(file_name, "") 
            except Exception as e:
                QMessageBox.warning(parent, 'Error', f'Failed to create file: {str(e)}')
        else:
            QMessageBox.warning(parent, 'Error', 'No file selected.')

    file_dialog.deleteLater()

=======
    tab_count = parent.tab_widget.count()
    file_name = f"Untitled-{tab_count + 1}"
    
    parent.add_tab(file_name, "", None)
    
    table_editor = parent.get_current_table_editor()
    if table_editor and hasattr(table_editor, 'mark_as_unsaved'):
        table_editor.mark_as_unsaved()
>>>>>>> liblouis/main

def open_file_dialog(parent):
    file_dialog = QFileDialog(parent)
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

<<<<<<< HEAD
    
=======
>>>>>>> liblouis/main
    if file_dialog.exec_():
        file_names = file_dialog.selectedFiles()
        if file_names:
            file_path = file_names[0]
            try:
<<<<<<< HEAD
                with open(file_path, 'r') as file:
                    content = file.read()
                parent.add_tab(os.path.basename(file_path), content)
=======
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                parent.add_tab(os.path.basename(file_path), content, file_path)
                
                table_editor = parent.get_current_table_editor()
                if table_editor and hasattr(table_editor, 'mark_as_saved'):
                    table_editor.mark_as_saved()
                
>>>>>>> liblouis/main
            except Exception as e:
                QMessageBox.warning(parent, 'Error', f'Failed to open file: {str(e)}')
        else:
            QMessageBox.warning(parent, 'Error', 'No file selected.')

    file_dialog.deleteLater()

def save_file_dialog(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
<<<<<<< HEAD
=======
        if hasattr(table_editor, 'testing_widget') and hasattr(table_editor.testing_widget, 'current_table_path'):
            current_path = table_editor.testing_widget.current_table_path
            if current_path:
                try:
                    table_editor.save_entries(current_path)

                    if hasattr(table_editor, 'mark_as_saved'):
                        table_editor.mark_as_saved()
                    return
                except Exception as e:
                    QMessageBox.warning(parent, 'Error', f'Failed to save file: {str(e)}')
        
        file_dialog = QFileDialog(parent)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_path = file_names[0]
                try:
                    table_editor.save_entries(file_path)
                    if hasattr(table_editor, 'mark_as_saved'):
                        table_editor.mark_as_saved()
                    if hasattr(table_editor, 'testing_widget'):
                        table_editor.testing_widget.set_current_table(file_path)
                    current_index = parent.tab_widget.currentIndex()
                    if current_index >= 0:
                        parent.tab_widget.setTabText(current_index, os.path.basename(file_path))
                except Exception as e:
                    QMessageBox.warning(parent, 'Error', f'Failed to save file: {str(e)}')
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

def save_as_file_dialog(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
>>>>>>> liblouis/main
        file_dialog = QFileDialog(parent)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_path = file_names[0]
                try:
                    table_editor.save_entries(file_path)
<<<<<<< HEAD
=======
                    if hasattr(table_editor, 'mark_as_saved'):
                        table_editor.mark_as_saved()
                    if hasattr(table_editor, 'testing_widget'):
                        table_editor.testing_widget.set_current_table(file_path)
                    current_index = parent.tab_widget.currentIndex()
                    if current_index >= 0:
                        parent.tab_widget.setTabText(current_index, os.path.basename(file_path))
>>>>>>> liblouis/main
                except Exception as e:
                    QMessageBox.warning(parent, 'Error', f'Failed to save file: {str(e)}')
            else:
                QMessageBox.warning(parent, 'Error', 'No file selected.')

        file_dialog.deleteLater()
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

<<<<<<< HEAD
def save_as_file_dialog(parent):
    save_file_dialog(parent)
=======
def undo_action(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        if hasattr(table_editor, 'text_widget') and hasattr(table_editor.text_widget, 'undo'):
            table_editor.text_widget.undo()
        elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'undo'):
            table_editor.table_widget.undo()
        elif hasattr(table_editor, 'undo'):
            table_editor.undo()
        else:
            QMessageBox.information(parent, 'Information', 'Undo is not available in this context.')

def redo_action(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        if hasattr(table_editor, 'text_widget') and hasattr(table_editor.text_widget, 'redo'):
            table_editor.text_widget.redo()
        elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'redo'):
            table_editor.table_widget.redo()
        elif hasattr(table_editor, 'redo'):
            table_editor.redo()
        else:
            QMessageBox.information(parent, 'Information', 'Redo is not available in this context.')

def go_to_entry(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        entry, ok = QInputDialog.getText(parent, 'Go to Entry', 'Enter the entry to go to:', QLineEdit.Normal)
        if ok and entry:
            if hasattr(table_editor, 'go_to_entry'):
                table_editor.go_to_entry(entry)
            elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'go_to_entry'):
                table_editor.table_widget.go_to_entry(entry)
            else:
                QMessageBox.information(parent, 'Information', 'Go to entry is not available in this context.')
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

def find_text(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        search_text, ok = QInputDialog.getText(parent, 'Find', 'Enter text to find:', QLineEdit.Normal)
        if ok and search_text:
            if hasattr(table_editor, 'find_text'):
                table_editor.find_text(search_text)
            elif hasattr(table_editor, 'text_widget') and hasattr(table_editor.text_widget, 'find'):
                table_editor.text_widget.find(search_text)
            elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'find'):
                table_editor.table_widget.find(search_text)
            else:
                QMessageBox.information(parent, 'Information', 'Find is not available in this context.')
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

def find_replace(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        find_text, ok = QInputDialog.getText(parent, 'Find and Replace', 'Enter text to find:', QLineEdit.Normal)
        if ok and find_text:
            replace_text, ok = QInputDialog.getText(parent, 'Find and Replace', 'Enter text to replace with:', QLineEdit.Normal)
            if ok:
                if hasattr(table_editor, 'find_replace'):
                    table_editor.find_replace(find_text, replace_text)
                elif hasattr(table_editor, 'text_widget') and hasattr(table_editor.text_widget, 'find') and hasattr(table_editor.text_widget, 'replace'):
                    if table_editor.text_widget.find(find_text):
                        table_editor.text_widget.replace(replace_text)
                    else:
                        QMessageBox.information(parent, 'Information', 'Text not found.')
                elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'find_replace'):
                    table_editor.table_widget.find_replace(find_text, replace_text)
                else:
                    QMessageBox.information(parent, 'Information', 'Find and replace is not available in this context.')
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

def change_font_size(parent, increase=True):
    table_editor = parent.get_current_table_editor()
    if table_editor:
        if hasattr(table_editor, 'change_font_size'):
            table_editor.change_font_size(increase)
        elif hasattr(table_editor, 'text_widget') and hasattr(table_editor.text_widget, 'font'):
            font = table_editor.text_widget.font()
            current_size = font.pointSize()
            if increase:
                font.setPointSize(current_size + 1)
            else:
                font.setPointSize(max(8, current_size - 1)) 
            table_editor.text_widget.setFont(font)
        elif hasattr(table_editor, 'table_widget') and hasattr(table_editor.table_widget, 'font'):
            font = table_editor.table_widget.font()
            current_size = font.pointSize()
            if increase:
                font.setPointSize(current_size + 1)
            else:
                font.setPointSize(max(8, current_size - 1))  
            table_editor.table_widget.setFont(font)
        else:
            QMessageBox.information(parent, 'Information', 'Font size change is not available in this context.')
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')
>>>>>>> liblouis/main
