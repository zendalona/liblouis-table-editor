import sys
import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog,
    QMessageBox, QApplication, QSizePolicy, QListWidget, QListWidgetItem,
    QFrame, QShortcut
)
from PyQt5.QtGui import QFont, QPixmap, QKeySequence, QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class HomeScreen(QWidget):
    file_opened = pyqtSignal(str, str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("homepage")
        
        self.recent_files = self.load_recent_files()

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)  

        left_panel = QWidget()
        left_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setSpacing(15)

        heading = QLabel("Table making doesn't need to be complex")
        heading.setObjectName("heading")
        heading.setWordWrap(True)

        title = QLabel("The Ultimate Tool\nfor Easy\nLiblouis Table Editing")
        title.setObjectName("title")
        title.setWordWrap(True)

        description = QLabel(
            "Streamline the creation and editing of Liblouis translation tables "
            "with our intuitive, cross-platform editor."
        )
        description.setObjectName("description")
        description.setWordWrap(True)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 10, 0, 10)

        create_button = QPushButton("Create new table")
        create_button.setObjectName("createBtn")
        create_button.setCursor(Qt.PointingHandCursor)
        create_button.clicked.connect(self.create_new_table)

        open_button = QPushButton("Open existing table")
        open_button.setObjectName("openBtn")
        open_button.setCursor(Qt.PointingHandCursor)
        open_button.clicked.connect(self.open_existing_table)

        button_layout.addWidget(create_button)
        button_layout.addWidget(open_button)
        button_layout.addStretch()

        recent_label = QLabel("Recent Files")
        recent_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            margin-top: 15px;
        """)
        
        self.recent_files_list = QListWidget()
        self.recent_files_list.setObjectName("recentFiles")
        self.recent_files_list.setMaximumHeight(120)
        self.recent_files_list.itemDoubleClicked.connect(self.open_recent_file)

        left_layout.addWidget(heading)
        left_layout.addWidget(title)
        left_layout.addWidget(description)
        left_layout.addWidget(button_container)
        left_layout.addWidget(recent_label)
        left_layout.addWidget(self.recent_files_list)
        left_layout.addStretch()

        self.right_panel = QLabel()
        self.right_panel.setObjectName("rightPanel")
        self.right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_panel.setMinimumWidth(400)

        self.original_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', 'background.png')
        self.updateBackgroundImage()

        self.main_layout.addWidget(left_panel, 45)
        self.main_layout.addWidget(self.right_panel, 55)

        self.update_recent_files_list()

        self.setMinimumSize(1000, 600)

    def updateBackgroundImage(self):
        if os.path.exists(self.original_image_path):
            original = QPixmap(self.original_image_path)
            if not original.isNull():
                available_width = self.right_panel.width()
                available_height = self.right_panel.height()
                
                if available_width > 0 and available_height > 0:
                    scaled = original.scaled(
                        available_width,
                        available_height,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    
                    final_pixmap = QPixmap(available_width, available_height)
                    final_pixmap.fill(QColor("#FFFFFF"))
                    
                    painter = QPainter(final_pixmap)
                    x = (available_width - scaled.width()) // 2
                    y = (available_height - scaled.height()) // 2
                    painter.drawPixmap(x, y, scaled)
                    painter.end()
                    
                    self.right_panel.setPixmap(final_pixmap)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateBackgroundImage()

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
                    open(file_path, 'w').close()

                    self.add_to_recent_files(file_path)
                    
                    self.file_opened.emit(os.path.basename(file_path), "", file_path)

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

                    self.add_to_recent_files(file_path)
                    
                    self.file_opened.emit(os.path.basename(file_path), file_content, file_path)

                except Exception as e:
                    QMessageBox.warning(self, 'Error', f'Failed to open file: {str(e)}')
                    
    def open_recent_file(self, item):
        file_path = item.data(Qt.UserRole)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                
                self.add_to_recent_files(file_path)
                
                self.file_opened.emit(os.path.basename(file_path), file_content, file_path)
                
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to open file: {str(e)}')
        else:
            QMessageBox.warning(self, 'Error', f'File not found: {file_path}')
            self.remove_from_recent_files(file_path)
            
    def load_recent_files(self):
        try:
            settings_path = os.path.join(os.path.expanduser("~"), ".liblouis_table_editor", "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                    return settings.get('recent_files', [])
        except Exception:
            pass
        return []
        
    def save_recent_files(self):
        try:
            settings_dir = os.path.join(os.path.expanduser("~"), ".liblouis_table_editor")
            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir)
                
            settings_path = os.path.join(settings_dir, "settings.json")
            settings = {'recent_files': self.recent_files}
            
            with open(settings_path, 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass
            
    def add_to_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        
        if len(self.recent_files) > 10:
            self.recent_files = self.recent_files[:10]
            
        self.save_recent_files()
        self.update_recent_files_list()
        
    def remove_from_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
            self.save_recent_files()
            self.update_recent_files_list()
            
    def update_recent_files_list(self):
        self.recent_files_list.clear()
        
        for file_path in self.recent_files:
            if os.path.exists(file_path):
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, file_path)
                item.setToolTip(file_path)
                self.recent_files_list.addItem(item)