import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QSizePolicy, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.Menubar import create_menubar
from components.TableEditor import TableEditor
from utils.ApplyStyles import apply_styles
from components.Homepage import HomeScreen  


class TableManager(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Liblouis Tables Manager")
        
        # Layout Setup
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create and add MenuBar
        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.tab_widget.setMinimumWidth(200)  # Prevent extra width
        self.tab_widget.setVisible(False)  # Hide initially

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()  # Get usable screen space

        # Calculate center position
        window_width = int(0.53 * screen_geometry.width())
        window_height = int(0.53 * screen_geometry.height())  # 53% of screen height

        start_x = int(screen_geometry.width() - (window_width * 0.900)) // 2
        start_y = (screen_geometry.height() - window_height) // 2

        # Set window position
        self.setGeometry(start_x, start_y, window_width, window_height)

        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, window_width, window_height)
        self.background_label.lower()

        # Content Layout (Home Screen + Tab Widget)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.home_screen = HomeScreen()
        self.home_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        content_layout.addWidget(self.home_screen, 2)  # Larger home screen
        content_layout.addWidget(self.tab_widget, 1)   # Smaller tab widget

        layout.addLayout(content_layout)
        self.setLayout(layout)

        self.raise_widgets()

        # Apply styles and set fixed size **AFTER** layouts are applied
        apply_styles(self)
        self.adjustSize()
        print("Styles applied successfully!")

    def raise_widgets(self):
        """Ensure the main widgets stay on top of the background."""
        self.home_screen.raise_()
        self.tab_widget.raise_()

    def add_tab(self, file_name, file_content):
        """Adds a new tab with the given file content."""
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        table_editor = TableEditor()
        table_editor.set_content(file_content)

        layout.addWidget(table_editor)
        new_tab.setLayout(layout)

        self.tab_widget.addTab(new_tab, file_name)
        self.tab_widget.setCurrentWidget(new_tab)

        # Ensure visibility updates
        self.home_screen.setVisible(False)
        self.tab_widget.setVisible(True)
        self.update_background_visibility()

    def get_current_table_editor(self):
        """Returns the currently active TableEditor instance."""
        current_widget = self.tab_widget.currentWidget()
        if current_widget and current_widget.layout().count() > 0:
            return current_widget.layout().itemAt(0).widget()
        return None

    def close_tab(self, index):    
        """Closes the tab at the given index."""
        tab_title = self.tab_widget.tabText(index)
        print(f"Closing tab: {tab_title}")

        self.tab_widget.removeTab(index)
        self.update_background_visibility()

    def update_background_visibility(self):
        """Updates visibility of background and home screen based on open tabs."""
        if self.tab_widget.count() == 0:
            self.background_label.show()
            self.home_screen.setVisible(True)
            self.tab_widget.setVisible(False)
        else:
            self.background_label.hide()
            self.home_screen.setVisible(False)
            self.tab_widget.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set Application Palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))  # Pure white
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))  # Pure white
    palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))  # Pure white
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))  # Pure white
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(255, 255, 255))  # Pure white
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(70, 130, 180))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    # Start Application
    window = TableManager()
    window.show()
    sys.exit(app.exec_())
