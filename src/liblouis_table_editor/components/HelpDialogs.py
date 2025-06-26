from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton, QFrame, QHBoxLayout, QScrollArea, QWidget, QShortcut, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QKeySequence
import os

class StyledDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.close_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.close_shortcut.activated.connect(self.close)

class AboutDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        this_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle("About Liblouis Table Editor")
        self.setWindowIcon(QIcon(os.path.join(this_dir, '..', 'assets', 'icons', 'about.png')))
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        self.setFocusPolicy(Qt.StrongFocus)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_frame = QFrame()
        header_frame.setObjectName("header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 16, 16, 16)
        
        logo_path = os.path.join(this_dir, '..', 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            logo_label.setPixmap(QPixmap(logo_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAccessibleName("Application Logo")
            header_layout.addWidget(logo_label)
        
        title_layout = QVBoxLayout()
        title_label = QLabel("Liblouis Table Editor")
        title_label.setStyleSheet("font-size: 32px; font-weight: 600; color: #2d2d2d;")
        title_label.setAccessibleName("Application Title")
        
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("color: #666666;")
        version_label.setAccessibleName("Application Version")
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        content_text = """
        <div class='section'>
            <p>An intuitive, accessible, and user-friendly tool designed to simplify the creation, editing, and management of translation tables used by the Liblouis Braille translation system.</p>
        </div>
        
        <div class='section'>
            <h3>Development</h3>
            <p>Developed By Zendalona</p>
            <p>© 2025 Zendalona</p>
        </div>
        
        <div class='section'>
            <h3>License</h3>
            <p>This project is licensed under the MIT License.</p>
        </div>
        """
        
        content_label = QLabel(content_text)
        content_label.setWordWrap(True)
        content_label.setAccessibleName("About Content")
        content_layout.addWidget(content_label)
        
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(16, 16, 16, 16)
        
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the About dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)
        main_layout.addWidget(footer_frame)
        
        self.setLayout(main_layout)

class UserGuideDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        this_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle("User Guide")
        self.setWindowIcon(QIcon(os.path.join(this_dir, '..', 'assets', 'icons', 'user_guide.png')))
        self.setMinimumSize(900, 700)
        self.resize(900, 700)
        self.setFocusPolicy(Qt.StrongFocus)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header_frame = QFrame()
        header_frame.setObjectName("header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 16, 16, 16)
        
        title_label = QLabel("User Guide")
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #2d2d2d;")
        title_label.setAccessibleName("User Guide Title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        guide_text = """
        <div class='section info-section'>
            <h2>Getting Started</h2>
            <p>Welcome to the Liblouis Table Editor! This guide will help you get started with creating and managing translation tables.</p>
        </div>
        
        <div class='section'>
            <h2>Basic Operations</h2>
            <div class='info-section'>
                <h3>Creating a New Table</h3>
                <p>1. Click on File > New</p>
                <p>2. Choose a location to save your table</p>
                <p>3. Start adding entries to your table</p>
            </div>
            
            <div class='info-section'>
                <h3>Opening Existing Tables</h3>
                <p>1. Click on File > Open</p>
                <p>2. Navigate to your table file</p>
                <p>3. Select and open the file</p>
            </div>
        </div>
        
        <div class='section'>
            <h2>Working with Entries</h2>
            <div class='info-section'>
                <h3>Adding Entries</h3>
                <p>• Use the Add Entry form to create new entries</p>
                <p>• Fill in the required fields</p>
                <p>• Click Add to save the entry</p>
            </div>
            
            <div class='info-section'>
                <h3>Editing Entries</h3>
                <p>• Double-click an entry to edit it</p>
                <p>• Use the context menu for additional options</p>
                <p>• Save changes when done</p>
            </div>
        </div>
        
        <div class='section'>
            <h2>Testing Your Table</h2>
            <div class='info-section'>
                <h3>Using the Testing Panel</h3>
                <p>• Enter text in the input field</p>
                <p>• View the braille output</p>
                <p>• Verify translations are correct</p>
            </div>
        </div>
        
        <div class='section'>
            <h2>Keyboard Shortcuts</h2>
            <div class='info-section'>
                <p>• <span class='shortcut'>Ctrl+N</span> New file</p>
                <p>• <span class='shortcut'>Ctrl+O</span> Open file</p>
                <p>• <span class='shortcut'>Ctrl+S</span> Save file</p>
                <p>• <span class='shortcut'>Ctrl+Shift+S</span> Save As</p>
                <p>• <span class='shortcut'>Ctrl+F</span> Find</p>
                <p>• <span class='shortcut'>Ctrl+H</span> Find and Replace</p>
                <p>• <span class='shortcut'>Ctrl+Z</span> Undo</p>
                <p>• <span class='shortcut'>Ctrl+Y</span> Redo</p>
                <p>• <span class='shortcut'>F1</span> About</p>
                <p>• <span class='shortcut'>F2</span> User Guide</p>
                <p>• <span class='shortcut'>F3</span> Report Bug</p>
            </div>
        </div>
        """
        
        guide_browser = QTextBrowser()
        guide_browser.setHtml(guide_text)
        guide_browser.setOpenExternalLinks(True)
        guide_browser.setAccessibleName("User Guide Content")
        scroll_layout.addWidget(guide_browser)
        
        scroll.setWidget(content_widget)
        content_layout.addWidget(scroll)
        
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(16, 16, 16, 16)
        
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the User Guide dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)
        main_layout.addWidget(footer_frame)
        
        self.setLayout(main_layout)

class ReportBugDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        this_dir = os.path.dirname(os.path.abspath(__file__))
        self.setWindowTitle("Report a Bug")
        self.setWindowIcon(QIcon(os.path.join(this_dir, '..', 'assets', 'icons', 'report_bug.png')))
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        
        self.setFocusPolicy(Qt.StrongFocus)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        header_frame = QFrame()
        header_frame.setObjectName("header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 16, 16, 16)
        
        title_label = QLabel("Report a Bug")
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #2d2d2d;")
        title_label.setAccessibleName("Report Bug Title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        bug_text = """
        <div class='section warning-section'>
            <h2>Found a Bug?</h2>
            <p>If you've found a bug in the Liblouis Table Editor, please help us improve by reporting it. Your feedback is valuable in making the application better for everyone.</p>
        </div>
        
        <div class='section'>
            <h2>How to Report</h2>
            <div class='info-section'>
                <h3>Step 1: Visit GitHub</h3>
                <p>Go to our GitHub repository: <a href="https://github.com/zendalona/liblouis-table-editor/issues">https://github.com/zendalona/liblouis-table-editor/issues</a></p>
                
                <h3>Step 2: Create New Issue</h3>
                <p>Click on the "New Issue" button</p>
                
                <h3>Step 3: Provide Details</h3>
                <p>Fill in the issue template with the following information:</p>
                <ul>
                    <li>A clear description of the bug</li>
                    <li>Steps to reproduce the issue</li>
                    <li>Expected behavior</li>
                    <li>Actual behavior</li>
                    <li>Screenshots if applicable</li>
                    <li>System information (OS, version)</li>
                </ul>
            </div>
        </div>
        
        <div class='section success-section'>
            <h2>Thank You!</h2>
            <p>Your feedback helps us make the Liblouis Table Editor better for everyone. We appreciate your contribution to improving the application.</p>
        </div>
        """
        
        bug_browser = QTextBrowser()
        bug_browser.setHtml(bug_text)
        bug_browser.setOpenExternalLinks(True)
        bug_browser.setAccessibleName("Report Bug Content")
        content_layout.addWidget(bug_browser)
        
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(16, 16, 16, 16)
        
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the Report Bug dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(content_frame)
        main_layout.addWidget(footer_frame)
        
        self.setLayout(main_layout) 
