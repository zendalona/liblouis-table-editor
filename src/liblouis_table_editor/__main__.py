import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QStackedLayout, QMessageBox, QFileDialog, QDesktopWidget, QShortcut
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon, QKeySequence
from PyQt5.QtCore import Qt
from liblouis_table_editor.config import WINDOW_WIDTH, WINDOW_HEIGHT
from liblouis_table_editor.components.Menubar import create_menubar
from liblouis_table_editor.components.TableEditor import TableEditor
from liblouis_table_editor.components.Homepage import HomeScreen
from liblouis_table_editor.utils.ApplyStyles import apply_styles
from liblouis_table_editor.utils.asset_utils import get_icon_path

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis-Table-Editor')
        self.setObjectName("liblouis-table-editor")
        
        self.setMinimumSize(1200, 800)
        
        icon_path = get_icon_path('liblouis-table-editor.ico')
        if not icon_path:
            icon_path = get_icon_path('icon.ico')
        
        if icon_path:
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
            QApplication.setWindowIcon(app_icon)  
        
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()  
        
        margin = 50  
        available_width = screen_rect.width() - (margin * 2)
        available_height = screen_rect.height() - (margin * 2)
        
        min_size = self.minimumSize()
        width = max(min_size.width(), min(WINDOW_WIDTH, available_width))
        height = max(min_size.height(), min(WINDOW_HEIGHT, available_height))
        
        self.resize(width, height)
        
        x = screen_rect.x() + (screen_rect.width() - width) // 2
        y = screen_rect.y() + (screen_rect.height() - height) // 2
        
        x = max(screen_rect.x(), min(x, screen_rect.x() + screen_rect.width() - width))
        y = max(screen_rect.y(), min(y, screen_rect.y() + screen_rect.height() - height))
        
        self.move(x, y)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

        self.stacked_layout = QStackedLayout()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.home_screen = HomeScreen(self)
        self.home_screen.file_opened.connect(self.handle_file_opened)
        
        self.stacked_layout.addWidget(self.home_screen)
        self.stacked_layout.addWidget(self.tab_widget)

        layout.addLayout(self.stacked_layout)

        self.setLayout(layout)

        apply_styles(self)

        self.update_background_visibility()

        self.showMaximized()

        self.focus_menu_shortcut = QShortcut(QKeySequence("Alt+F"), self)
        self.focus_menu_shortcut.activated.connect(self.focus_file_menu)

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

    def get_current_table_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.layout().itemAt(0).widget()
        return None

    def close_tab(self, index):
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
                            QMessageBox.warning(self, 'Error', f"Failed to save file: {str(e)}")
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
                                    QMessageBox.warning(self, 'Error', f"Failed to save file: {str(e)}")
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

    def focus_file_menu(self):

        if self.menubar:
            file_menu = self.menubar.actions()[0].menu()
            if file_menu:
                self.menubar.setActiveAction(self.menubar.actions()[0])
                file_menu.popup(self.menubar.mapToGlobal(self.menubar.actionGeometry(self.menubar.actions()[0]).bottomLeft()))
                self.menubar.setFocus()

def main():
    app = QApplication(sys.argv)
    
    icon_path = get_icon_path('liblouis-table-editor.ico')
    if not icon_path:
        icon_path = get_icon_path('icon.ico')
    
    if icon_path:
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

    try:
        window = TableManager()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Fatal Error", f"Application failed to start: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
