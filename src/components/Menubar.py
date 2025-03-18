import os
from PyQt6.QtWidgets import QMenuBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction

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

    return menubar

def open_new_file_dialog(parent):
    file_dialog = QFileDialog(parent)
    file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
    file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

    if file_dialog.exec():
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
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

    if file_dialog.exec():
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
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

        if file_dialog.exec():
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

