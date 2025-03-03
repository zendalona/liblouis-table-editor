import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog,
    QMessageBox, QApplication, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class HomeScreen(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: white; padding: 0px; margin: 0px;")  

        # Wrapper Layout (Holds Everything)
        self.wrapper_layout = QVBoxLayout(self)
        self.wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.wrapper_layout.setSpacing(0)
        self.wrapper_layout.setAlignment(Qt.AlignCenter)

        # Main Layout (Holds Content + Image)
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(15)

        # Left Content Layout
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)  
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Heading Section
        self.heading = QLabel("Table making doesn’t need to be complex")
        self.heading.setWordWrap(True)
        self.heading.setStyleSheet("padding: 0px; margin: 0px; font-size: 22px; font-weight: bold;")

        # Title
        self.title = QLabel(" The Ultimate Tool \n for Easy \n Liblouis Table Editing")
        self.title.setStyleSheet("color: #222; font-size: 30px; font-weight: bold;")
        self.title.setAlignment(Qt.AlignLeft)

        # Buttons
        self.create_button = QPushButton("Create new table to get started")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #DCE7F5;
                color: black;
                border-radius: 30px;
                padding: 15px;
                margin: 10px;
                border: 2px solid transparent;
            }
            QPushButton:hover {
                background-color: #C4D8F5;
            }
            QPushButton:pressed {
                background-color: #A0C0E5;
            }
        """)
        self.create_button.clicked.connect(self.create_new_table)

        self.open_button = QPushButton("Or open existing table")
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #0077C2;
                color: white;
                border-radius: 30px;
                padding: 15px;
                margin: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #C4D8F5;
            }
            QPushButton:pressed {
                background-color: #A0C0E5;
            }
        
        """)
        self.open_button.clicked.connect(self.open_existing_table)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.open_button)

        # Description
        self.description = QLabel(
            "Streamline the creation and editing of Liblouis translation tables "
            "with our intuitive, cross-platform editor."
        )
        self.description.setWordWrap(True)
        self.description.setStyleSheet("color: #666; padding-top: 10px;")
        self.description.setAlignment(Qt.AlignLeft)

        # Add widgets to content layout
        self.content_layout.addWidget(self.heading)
        self.content_layout.addWidget(self.title)
        self.content_layout.addLayout(self.button_layout)
        self.content_layout.addWidget(self.description)

        # Right Image Layout
        self.image_layout = QVBoxLayout()
        self.image_layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignRight)
        pixmap = QPixmap("src/assets/images/image.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setMaximumWidth(550)  # Limit image width
        self.image_layout.addWidget(self.image_label)

        # Add layouts to main layout
        self.main_layout.addLayout(self.content_layout, 1)  
        self.main_layout.addLayout(self.image_layout, 1)  # Balanced layout

        # Add main layout to wrapper layout
        self.wrapper_layout.addLayout(self.main_layout)

        # Set window size based on content
        self.adjustSize()
        self.setFixedSize(self.main_layout.sizeHint())  

    def resizeEvent(self, event):
        """Resize event to dynamically update layout size."""
        super().resizeEvent(event)
        self.setFixedSize(self.main_layout.sizeHint())  # Ensure width matches content

    def create_new_table(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_path = file_names[0]
                
                try:
                    # Create an empty file
                    open(file_path, 'w').close()

                    # Send the new file to TableManager
                    parent_window = self.window()  
                    if hasattr(parent_window, "add_tab"):  
                        parent_window.add_tab(os.path.basename(file_path), "")  # Empty content
                    else:
                        QMessageBox.warning(self, "Error", "Failed to open new table inside the app.")

                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Failed to create file: {str(e)}')

    def open_existing_table(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Table Files (*.cti *.ctb *.utb);;All Files (*)")

        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                file_path = file_names[0]
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_content = file.read()

                    # Send the file data to TableManager
                    parent_window = self.window()  # Get the parent TableManager instance
                    if hasattr(parent_window, "add_tab"):  
                        parent_window.add_tab(os.path.basename(file_path), file_content)
                    else:
                        QMessageBox.warning(self, "Error", "Failed to open table inside the app.")

                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Failed to open file: {str(e)}')

