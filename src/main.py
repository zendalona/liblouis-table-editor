import sys
<<<<<<< HEAD
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap
=======
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QStackedLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
>>>>>>> liblouis/main
from PyQt5.QtCore import Qt
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.Menubar import create_menubar
from components.TableEditor import TableEditor
<<<<<<< HEAD
=======
from components.Homepage import HomeScreen
>>>>>>> liblouis/main
from utils.ApplyStyles import apply_styles

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

<<<<<<< HEAD
        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
=======
        self.setWindowTitle('Liblouis-Tables-Editor')
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'icon.ico')
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            QApplication.setWindowIcon(app_icon)  # Set it globally
        
        screen = QApplication.primaryScreen().geometry()
        
        available_height = screen.height() - 100  
        available_width = screen.width() - 100
        
        width = min(WINDOW_WIDTH, available_width)
        height = min(WINDOW_HEIGHT, available_height)
        
        self.resize(width, height)
        
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.move(x, y)
>>>>>>> liblouis/main

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

<<<<<<< HEAD
=======
        self.stacked_layout = QStackedLayout()
        
>>>>>>> liblouis/main
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

<<<<<<< HEAD
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setPixmap(QPixmap('src/assets/images/background.png'))
        self.background_label.setScaledContents(True)

        layout.addWidget(self.tab_widget)
        layout.addWidget(self.background_label)
=======
        self.home_screen = HomeScreen(self)
        self.home_screen.file_opened.connect(self.handle_file_opened)
        
        self.stacked_layout.addWidget(self.home_screen)
        self.stacked_layout.addWidget(self.tab_widget)

        layout.addLayout(self.stacked_layout)
>>>>>>> liblouis/main

        self.setLayout(layout)

        apply_styles(self)

        self.update_background_visibility()

<<<<<<< HEAD
    def add_tab(self, file_name, file_content):
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        table_editor = TableEditor()
        table_editor.set_content(file_content)

        layout.addWidget(table_editor)
        new_tab.setLayout(layout)

        self.tab_widget.addTab(new_tab, file_name)
        self.tab_widget.setCurrentWidget(new_tab)

        self.update_background_visibility()
=======
    def handle_file_opened(self, file_name, file_content, file_path):
        self.add_tab(file_name, file_content, file_path)
        self.stacked_layout.setCurrentIndex(1)

    def add_tab(self, file_name, file_content, file_path=None):
        try:
            new_tab = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            table_editor = TableEditor()
            table_editor.set_content(file_content)
            if file_path:
                table_editor.testing_widget.set_current_table(file_path)
                table_editor.mark_as_saved()
            else:
                table_editor.mark_as_unsaved()

            layout.addWidget(table_editor)
            new_tab.setLayout(layout)

            index = self.tab_widget.addTab(new_tab, file_name)
            self.tab_widget.setCurrentIndex(index)

            self.update_background_visibility()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add tab: {str(e)}")
>>>>>>> liblouis/main

    def get_current_table_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.layout().itemAt(0).widget()
        return None

    def close_tab(self, index):
<<<<<<< HEAD
        self.tab_widget.removeTab(index)
        self.update_background_visibility()

    def update_background_visibility(self):
        if self.tab_widget.count() == 0:
            self.background_label.show()
        else:
            self.background_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
=======
        try:
            widget = self.tab_widget.widget(index)
            
            table_editor = widget.layout().itemAt(0).widget()
            if hasattr(table_editor, 'has_unsaved_changes') and table_editor.has_unsaved_changes():
                reply = QMessageBox.question(
                    self, 'Unsaved Changes',
                    'There are unsaved changes. Do you want to save before closing?',
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                )
                
                if reply == QMessageBox.Save:
                    current_path = None
                    if hasattr(table_editor, 'testing_widget') and hasattr(table_editor.testing_widget, 'current_table_path'):
                        current_path = table_editor.testing_widget.current_table_path
                    
                    if current_path:
                        try:
                            table_editor.save_entries(current_path)
                            if hasattr(table_editor, 'mark_as_saved'):
                                table_editor.mark_as_saved()
                        except Exception as e:
                            QMessageBox.warning(self, 'Error', f'Failed to save file: {str(e)}')
                            return
                    else:
                        file_dialog = QFileDialog(self)
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
                                except Exception as e:
                                    QMessageBox.warning(self, 'Error', f'Failed to save file: {str(e)}')
                                    return
                            else:
                                return
                        else:
                            return
                elif reply == QMessageBox.Cancel:
                    return
            
            self.tab_widget.removeTab(index)
            
            if widget:
                widget.deleteLater()
            
            self.update_background_visibility()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to close tab: {str(e)}")

    def update_background_visibility(self):
        if self.tab_widget.count() == 0:
            self.stacked_layout.setCurrentIndex(0)  
        else:
            self.stacked_layout.setCurrentIndex(1)  

    def closeEvent(self, event):
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            table_editor = widget.layout().itemAt(0).widget()
            if hasattr(table_editor, 'has_unsaved_changes') and table_editor.has_unsaved_changes():
                reply = QMessageBox.question(
                    self, 'Unsaved Changes',
                    'There are unsaved changes. Do you want to save before closing?',
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                )
                
                if reply == QMessageBox.Save:
                    current_path = None
                    if hasattr(table_editor, 'testing_widget') and hasattr(table_editor.testing_widget, 'current_table_path'):
                        current_path = table_editor.testing_widget.current_table_path
                    
                    if current_path:
                        try:
                            table_editor.save_entries(current_path)
                            if hasattr(table_editor, 'mark_as_saved'):
                                table_editor.mark_as_saved()
                        except Exception as e:
                            QMessageBox.warning(self, 'Error', f'Failed to save file: {str(e)}')
                            event.ignore()
                            return
                    else:
                        file_dialog = QFileDialog(self)
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
                                except Exception as e:
                                    QMessageBox.warning(self, 'Error', f'Failed to save file: {str(e)}')
                                    event.ignore()
                                    return
                            else:
                                event.ignore()
                                return
                        else:
                            event.ignore()
                            return
                elif reply == QMessageBox.Cancel:
                    event.ignore()
                    return
        
        event.accept()

if __name__ == '__main__':
    # Set application icon path before creating QApplication
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'icon.ico')
    
    app = QApplication(sys.argv)
    
    # Set application icon
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
        QApplication.setWindowIcon(app_icon)  
        
        if sys.platform == 'win32':
            try:
                import ctypes
                myappid = 'liblouis.table.editor.1.0'  
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception as e:
                print(f"Warning: Could not set Windows app ID: {e}")
        
        elif sys.platform.startswith('linux'):
            try:
                from PyQt5.QtDBus import QDBusConnection, QDBusMessage
                bus = QDBusConnection.sessionBus()
                if bus.isConnected():
                    message = QDBusMessage.createMethodCall(
                        "org.freedesktop.portal.Desktop",
                        "/org/freedesktop/portal/desktop",
                        "org.freedesktop.portal.Settings",
                        "Read"
                    )
                    message.setArguments(["org.freedesktop.appearance", "color-scheme"])
                    bus.call(message)
            except Exception as e:
                print(f"Warning: Could not set Linux theme integration: {e}")
>>>>>>> liblouis/main

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 248, 255))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 248, 255))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 248, 255))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(70, 130, 180))
    palette.setColor(QPalette.HighlightedText, Qt.white)

    app.setPalette(palette)

<<<<<<< HEAD
    window = TableManager()
    window.show()

    sys.exit(app.exec_())
=======
    try:
        window = TableManager()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {str(e)}")
        sys.exit(1)
>>>>>>> liblouis/main
