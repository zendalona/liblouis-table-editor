import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel
from PyQt6.QtGui import QPalette, QColor, QPixmap
from PyQt6.QtCore import Qt
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
        # self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.background_label.setPixmap(QPixmap('src/assets/images/background.png'))
        self.background_label.setScaledContents(True)

        layout.addWidget(self.tab_widget)
        layout.addWidget(self.background_label)

        self.setLayout(layout)

        apply_styles(self)

        self.update_background_visibility()

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

    def get_current_table_editor(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            return current_widget.layout().itemAt(0).widget()
        return None

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        self.update_background_visibility()

    def update_background_visibility(self):
        if self.tab_widget.count() == 0:
            self.background_label.show()
        else:
            self.background_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 248, 255))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 248, 255))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Highlight, QColor(70, 130, 180))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)


    app.setPalette(palette)

    window = TableManager()
    window.show()

    # sys.exit(app.exec_())
    sys.exit(app.exec())

