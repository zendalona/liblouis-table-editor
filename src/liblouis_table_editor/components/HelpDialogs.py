from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton, QFrame, QHBoxLayout, QScrollArea, QWidget, QShortcut, QSizePolicy, QApplication, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QKeySequence
import os
from ..utils.asset_utils import get_image_path, get_icon_path

class StyledDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QDialog {
                background: #f8f9fa;
            }
            QLabel#sectionHeader {
                font-size: 18px;
                font-weight: bold;
                color: #2d2d2d;
                margin-top: 16px;
                margin-bottom: 8px;
            }
            QFrame[divider="true"] {
                background: #e0e0e0;
                max-height: 1px;
                min-height: 1px;
                border: none;
                margin-top: 12px;
                margin-bottom: 12px;
            }
            QPushButton#openBtn {
                background: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 8px 24px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton#openBtn:hover {
                background: #1565c0;
            }
            QTextBrowser {
                background: #ffffff;
                border-radius: 6px;
                padding: 12px;
                font-size: 15px;
            }
        """)
        self.close_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.close_shortcut.activated.connect(self.close)

class AboutDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Liblouis Table Editor")
        self.setMinimumSize(900, 700)
        self.resize(850, 600)
        self.setFocusPolicy(Qt.StrongFocus)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(32, 32, 32, 32)

        # Documentation-style QTextBrowser
        about_browser = QTextBrowser()
        about_browser.setOpenExternalLinks(True)
        about_browser.setStyleSheet("QTextBrowser { background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; padding: 32px; font-size: 16px; font-family: 'Segoe UI', 'Arial', 'sans-serif'; color: #222; }")

        zendalona_logo_path = get_image_path('zendalona.png')
        logo_html = f"<img src='{zendalona_logo_path}' class='zendalona-logo' style='display:block; max-width:15px; margin-bottom:12px;'>" if zendalona_logo_path else ""

        about_html = f"""
        {logo_html}
        <h1 style='font-size:2.2em; margin-bottom:0.2em;'>Liblouis Table Editor</h1>
        <div style='color:#666; font-size:1.1em; margin-bottom:1.5em;'>Version 1.0.0</div>
        <hr style='margin: 1.5em 0;'>
        <h2>Description</h2>
        <p>An intuitive, accessible, and user-friendly tool designed to simplify the creation, editing, and management of translation tables used by the <b>Liblouis Braille translation system</b>.</p>
        <h2>Features</h2>
        <ul>
            <li>Modern, accessible UI for editing Liblouis tables</li>
            <li>Easy entry management and validation</li>
            <li>Integrated testing and preview</li>
            <li>Keyboard shortcuts for productivity</li>
            <li>Cross-platform support</li>
        </ul>
        <h2>License</h2>
        <pre style='background:#f8f8f8; border:1px solid #e5e5e5; border-radius:4px; padding:12px; font-size:1em; color:#333;'>MIT License</pre>
        <h2>Credits</h2>
        <p>
            Developed by <b>Riya Jain  GSoC'24 Contributor</b> and <b>Sahil Rakhaiya GSoC'25 Contributor</b><br>
            Mentors: <b>Nalin</b>, <b>Samuel Thibault</b>, <b>K Sathaseelan</b>, <b>Prabhu Kondarangi</b><br>
            &copy; 2025 Zendalona. All rights reserved.
        </p>

        <h2>Links</h2>
        <ul>
            <li><a href='https://github.com/zendalona/liblouis-table-editor'>GitHub Repository</a></li>
            <li><a href='https://liblouis.io/'>Liblouis Project</a></li>
        </ul>
        """
        about_browser.setHtml(about_html)
        main_layout.addWidget(about_browser)

        # Close button at the bottom
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 24, 0, 0)
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the About dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        main_layout.addLayout(footer_layout)

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
        header_layout.setContentsMargins(32, 32, 32, 16)
        title_label = QLabel("User Guide")
        title_label.setStyleSheet("font-size: 28px; font-weight: 700; color: #1976d2;")
        title_label.setAccessibleName("User Guide Title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        divider1 = QFrame()
        divider1.setProperty("divider", True)
        divider1.setFrameShape(QFrame.HLine)
        divider1.setFrameShadow(QFrame.Sunken)
        
        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(32, 16, 32, 16)
        content_layout.setSpacing(0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        guide_browser = QTextBrowser()
        guide_browser.setHtml("""
        <div class='section info-section'>
            <h2>Getting Started</h2>
            <p>Welcome to the Liblouis Table Editor! This guide will help you get started with creating and managing translation tables.</p>
        </div>
        <hr>
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
            <div class='info-section'>
                <h3>"Open With" Integration</h3>
                <p>The Liblouis Table Editor now supports multiple ways to open files:</p>
                <p>• <strong>Right-click context menu:</strong> Right-click any .cti, .ctb, or .utb file and select "Open with Liblouis Table Editor"</p>
                <p>• <strong>Command line:</strong> Open files directly from terminal/command prompt</p>
                <p>• <strong>Drag and drop:</strong> Drag table files directly onto the application window</p>
                <p>• <strong>Multiple files:</strong> Open several files simultaneously from command line or file manager</p>
                <p><strong>Supported file types:</strong> .cti, .ctb, .utb</p>
            </div>
        </div>
        <hr>
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
        <hr>
        <div class='section'>
            <h2>Testing Your Table</h2>
            <div class='info-section'>
                <h3>Using the Testing Panel</h3>
                <p>• Enter text in the input field</p>
                <p>• View the braille output</p>
                <p>• Verify translations are correct</p>
            </div>
        </div>
        <hr>
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
        """)
        guide_browser.setOpenExternalLinks(True)
        guide_browser.setAccessibleName("User Guide Content")
        scroll_layout.addWidget(guide_browser)
        
        scroll.setWidget(content_widget)
        content_layout.addWidget(scroll)
        
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(32, 16, 32, 32)
        
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the User Guide dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(divider1)
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
        header_layout.setContentsMargins(32, 32, 32, 16)
        title_label = QLabel("Report a Bug")
        title_label.setStyleSheet("font-size: 28px; font-weight: 700; color: #d32f2f;")
        title_label.setAccessibleName("Report Bug Title")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        divider1 = QFrame()
        divider1.setProperty("divider", True)
        divider1.setFrameShape(QFrame.HLine)
        divider1.setFrameShadow(QFrame.Sunken)
        
        content_frame = QFrame()
        content_frame.setObjectName("content")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(32, 16, 32, 16)
        content_layout.setSpacing(0)
        
        bug_browser = QTextBrowser()
        bug_browser.setHtml("""
        <div class='section warning-section'>
            <h2>Found a Bug?</h2>
            <p>If you've found a bug in the Liblouis Table Editor, please help us improve by reporting it. Your feedback is valuable in making the application better for everyone.</p>
        </div>
        <hr>
        <div class='section'>
            <h2>How to Report</h2>
            <div class='info-section'>
                <h3>Step 1: Visit GitHub</h3>
                <p>Go to our GitHub repository: <a href=\"https://github.com/zendalona/liblouis-table-editor/issues\">https://github.com/zendalona/liblouis-table-editor/issues</a></p>
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
        <hr>
        <div class='section success-section'>
            <h2>Thank You!</h2>
            <p>Your feedback helps us make the Liblouis Table Editor better for everyone. We appreciate your contribution to improving the application.</p>
        </div>
        """)
        bug_browser.setOpenExternalLinks(True)
        bug_browser.setAccessibleName("Report Bug Content")
        content_layout.addWidget(bug_browser)
        
        footer_frame = QFrame()
        footer_frame.setObjectName("footer")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(32, 16, 32, 32)
        
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the Report Bug dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        
        main_layout.addWidget(header_frame)
        main_layout.addWidget(divider1)
        main_layout.addWidget(content_frame)
        main_layout.addWidget(footer_frame)
        
        self.setLayout(main_layout) 

class LiblouisInstallDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liblouis Installation Guide")
        self.setMinimumSize(850, 725)
        self.resize(600, 500)
        self.setFocusPolicy(Qt.StrongFocus)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(32, 32, 32, 32)

        header_layout = QHBoxLayout()
        icon_path = get_icon_path('about.png')
        if icon_path:
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            header_layout.addWidget(icon_label)
        title_label = QLabel("<b style='font-size: 2em;'>How to Install Liblouis</b>")
        title_label.setStyleSheet("font-size: 2em; margin-left: 12px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        instructions = QTextBrowser()
        instructions.setOpenExternalLinks(True)
        instructions.setStyleSheet("QTextBrowser { background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; padding: 24px; font-size: 16px; font-family: 'Segoe UI', 'Arial', 'sans-serif'; color: #222; }")
        instructions.setHtml('''
        <style>
        code { font-family: "Consolas", "Courier New", monospace; font-size: 15px; color: #222; }
        </style>
        <h2 style="color:#1976d2;">Windows</h2>
        <ol>
        <li>Download the latest liblouis release from: <a href="https://github.com/liblouis/liblouis/releases">https://github.com/liblouis/liblouis/releases</a></li>
        <li>Extract the downloaded zip file</li>
        <li>Copy the extracted folder to <b>C:\\Program Files\\liblouis</b> (remove extra word from name only extracted as "liblouis")</li>
        <li>Make sure the following structure exists:<br>
            <code>C:\\Program Files\\liblouis\\bin\\lou_translate.exe</code><br>
            <code>C:\\Program Files\\liblouis\\share\\liblouis\\tables</code>
        </li>
        <li>Add liblouis to Windows PATH:
            <ol type="a">
                <li>Press Windows + R, type <b>sysdm.cpl</b> and press Enter</li>
                <li>Go to <b>Advanced</b> tab</li>
                <li>Click <b>Environment Variables</b></li>
                <li>Under <b>User variables</b>, find and select <b>Path</b></li>
                <li>Click <b>Edit</b></li>
                <li>Click <b>New</b></li>
                <li>Add <code>C:\\Program Files\\liblouis\\bin</code></li>
                <li>Click <b>OK</b> on all windows</li>
                <li>Restart your PC/Laptop</li>
            </ol>
        </li>
        </ol>
        <p style="color:#d32f2f;"><b>After installation, click Test Installation below.</b></p>
        ''')
        main_layout.addWidget(instructions)

        # Test Installation button
        test_btn = QPushButton("Test Installation")
        test_btn.setObjectName("openBtn")
        test_btn.setToolTip("Check if lou_translate is available on your system")
        test_btn.clicked.connect(self.test_installation)
        main_layout.addWidget(test_btn)

        # Footer with close button
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 24, 0, 0)
        close_button = QPushButton("Close")
        close_button.setObjectName("openBtn")
        close_button.setAccessibleName("Close Dialog")
        close_button.setAccessibleDescription("Closes the Liblouis installation dialog")
        close_button.clicked.connect(self.close)
        footer_layout.addStretch()
        footer_layout.addWidget(close_button)
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def test_installation(self):
        import shutil, os, sys
        found = False
        if sys.platform == 'win32':
            exe = os.path.join("C:\\Program Files\\liblouis", "bin", "lou_translate.exe")
            found = os.path.exists(exe)
        else:
            found = shutil.which('lou_translate') is not None or os.path.exists("/usr/bin/lou_translate")
        if found:
            QMessageBox.information(self, "Liblouis Found", "liblouis is installed and available!")
        else:
            QMessageBox.warning(self, "Not Found", "liblouis is still not found. Please follow the steps above.") 
