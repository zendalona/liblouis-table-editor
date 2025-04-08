import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.Menubar import create_menubar
from components.TableEditor import TableEditor
from utils.ApplyStyles import apply_styles

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        
        # Use proper path handling for background image
        bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'images', 'background.png')
        if os.path.exists(bg_path):
            self.background_label.setPixmap(QPixmap(bg_path))
            self.background_label.setScaledContents(True)
        else:
            print(f"Warning: Background image not found at {bg_path}")

        layout.addWidget(self.tab_widget)
        layout.addWidget(self.background_label)

        self.setLayout(layout)

        apply_styles(self)

        self.update_background_visibility()

    def add_tab(self, file_name, file_content):
        try:
            new_tab = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            table_editor = TableEditor()
            table_editor.set_content(file_content)

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
            # Get the widget before removing the tab
            widget = self.tab_widget.widget(index)
            
            # Check if there are unsaved changes
            table_editor = widget.layout().itemAt(0).widget()
            if hasattr(table_editor, 'has_unsaved_changes') and table_editor.has_unsaved_changes():
                reply = QMessageBox.question(
                    self, 'Unsaved Changes',
                    'There are unsaved changes. Do you want to save before closing?',
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                )
                
                if reply == QMessageBox.Save:
                    # Implement save logic here
                    pass
                elif reply == QMessageBox.Cancel:
                    return
            
            # Remove the tab first
            self.tab_widget.removeTab(index)
            
            # Clean up the widget and its children
            if widget:
                widget.deleteLater()
            
            self.update_background_visibility()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to close tab: {str(e)}")

    def update_background_visibility(self):
        if self.tab_widget.count() == 0:
            self.background_label.show()
        else:
            self.background_label.hide()

    def closeEvent(self, event):
        """Handle application closing."""
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
                    # Implement save logic here
                    pass
                elif reply == QMessageBox.Cancel:
                    event.ignore()
                    return
        
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set up the application palette
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
