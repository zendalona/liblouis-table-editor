import os
from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

def create_action(parent, title, icon_path=None, shortcut=None, status_tip=None, triggered=None):
    action = QAction(title, parent)
    if icon_path:
        action.setIcon(QIcon(icon_path))
    if shortcut:
        action.setShortcut(shortcut)
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

    def update_stylesheet(new_size):
        try:
            # Read the current stylesheet
            stylesheet_path = "./src/styles.qss"
            with open(stylesheet_path, 'r') as file:
                stylesheet = file.read()
            
            # Update the font-size in the QWidget section
            import re
            updated_stylesheet = re.sub(
                r'(QWidget\s*{\s*[^}]*?font-size:\s*)\d+px',
                rf'\g<1>{new_size}px',
                stylesheet
            )
            
            # Apply the updated stylesheet
            parent.setStyleSheet(updated_stylesheet)
            
            # Also update all child widgets
            for widget in parent.findChildren(QWidget):
                widget.setStyleSheet(updated_stylesheet)
                
        except Exception as e:
            print(f"Error updating stylesheet: {e}")

    def increase_font_size():
        try:
            # Get the current font size from QWidget in stylesheet
            stylesheet_path = "./src/styles.qss"
            with open(stylesheet_path, 'r') as file:
                stylesheet = file.read()
            
            import re
            match = re.search(r'QWidget\s*{\s*[^}]*?font-size:\s*(\d+)px', stylesheet)
            if match:
                current_size = int(match.group(1))
                new_size = current_size + 2
                update_stylesheet(new_size)
                print(f"Increased font size to {new_size}px")
            
            # Update application font
            app = QApplication.instance()
            font = app.font()
            font.setPointSize(font.pointSize() + 1)
            app.setFont(font)
            
            # Force update
            parent.updateGeometry()
            parent.update()
            
        except Exception as e:
            print(f"Error in increase_font_size: {e}")

    def decrease_font_size():
        try:
            # Get the current font size from QWidget in stylesheet
            stylesheet_path = "./src/styles.qss"
            with open(stylesheet_path, 'r') as file:
                stylesheet = file.read()
            
            import re
            match = re.search(r'QWidget\s*{\s*[^}]*?font-size:\s*(\d+)px', stylesheet)
            if match:
                current_size = int(match.group(1))
                new_size = max(8, current_size - 2)  # Don't go below 8px
                update_stylesheet(new_size)
                print(f"Decreased font size to {new_size}px")
            
            # Update application font
            app = QApplication.instance()
            font = app.font()
            new_size = max(8, font.pointSize() - 1)  # Don't go below 8pt
            font.setPointSize(new_size)
            app.setFont(font)
            
            # Force update
            parent.updateGeometry()
            parent.update()
            
        except Exception as e:
            print(f"Error in decrease_font_size: {e}")

    # Create actions for font size controls
    increase_font_action = QAction('Increase Font Size', parent)
    increase_font_action.setShortcut('Ctrl+]')
    increase_font_action.setIcon(QIcon(os.path.join(icon_base_path, 'increase_font.png')))
    increase_font_action.triggered.connect(increase_font_size)

    decrease_font_action = QAction('Decrease Font Size', parent)
    decrease_font_action.setShortcut('Ctrl+[')
    decrease_font_action.setIcon(QIcon(os.path.join(icon_base_path, 'decrease_font.png')))
    decrease_font_action.triggered.connect(decrease_font_size)

    menu_structure = {
        'File': [
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
            increase_font_action,
            decrease_font_action
        ],
        'Help': [
            ('About', os.path.join(icon_base_path, 'about.png'), None, None, None),
            ('Report a bug', os.path.join(icon_base_path, 'report_bug.png'), None, None, None),
            ('User Guide', os.path.join(icon_base_path, 'user_guide.png'), None, None, None)
        ]
    }

    # Add menus and actions
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
                menu.addAction(menu_action)

    return menubar

def open_new_file_dialog(parent):
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


def open_file_dialog(parent):
    file_dialog = QFileDialog(parent)
    file_dialog.setFileMode(QFileDialog.ExistingFile)
    file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

    
    if file_dialog.exec_():
        file_names = file_dialog.selectedFiles()
        if file_names:
            file_path = file_names[0]
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                parent.add_tab(os.path.basename(file_path), content)
            except Exception as e:
                QMessageBox.warning(parent, 'Error', f'Failed to open file: {str(e)}')
        else:
            QMessageBox.warning(parent, 'Error', 'No file selected.')

    file_dialog.deleteLater()

def save_file_dialog(parent):
    table_editor = parent.get_current_table_editor()
    if table_editor:
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
                except Exception as e:
                    QMessageBox.warning(parent, 'Error', f'Failed to save file: {str(e)}')
            else:
                QMessageBox.warning(parent, 'Error', 'No file selected.')

        file_dialog.deleteLater()
    else:
        QMessageBox.warning(parent, 'Error', 'No tab is currently open.')

def save_as_file_dialog(parent):
    save_file_dialog(parent)
