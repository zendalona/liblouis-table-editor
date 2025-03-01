import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QLabel,QDesktopWidget
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
        # Dynamically set the window size based on the screen resolution
        screen_geometry=QDesktopWidget().screenGeometry()
        self.resize(screen_geometry.width()*0.8, screen_geometry.height()*0.8)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setPixmap(QPixmap('src/assets/images/background.png'))
        self.background_label.setScaledContents(True)

        layout.addWidget(self.tab_widget,stretch=1)
        layout.addWidget(self.background_label,stretch=0)

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

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
