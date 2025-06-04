# style_utils.py

from PyQt5.QtCore import QFile, QTextStream
<<<<<<< HEAD

def apply_styles(widget):
    
    stylesheet_path = "./src/styles.qss"
    style_file = QFile(stylesheet_path)
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Failed to open stylesheet: {stylesheet_path}")
=======
import os
import sys

def apply_styles(widget):

    if getattr(sys, 'frozen', False):

        base_dir = os.path.dirname(sys.executable)
        print(f"Running in PyInstaller bundle, base_dir: {base_dir}")

        possible_paths = [
            os.path.join(base_dir, "_internal", "styles.qss"),  
            os.path.join(base_dir, "styles.qss"), 
        ]
    else:

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"Running in development environment, base_dir: {base_dir}")
        possible_paths = [
            os.path.join(base_dir, "styles.qss"), 
            os.path.join(base_dir, "src", "styles.qss"), 
        ]
    
    print("Looking for styles.qss in:")
    for path in possible_paths:
        print(f"  - {path}")
    
    stylesheet_path = None
    for path in possible_paths:
        if os.path.exists(path):
            stylesheet_path = path
            print(f"Found styles.qss at: {path}")
            break
    
    if not stylesheet_path:
        print("Error: styles.qss not found in any of the expected locations")
        return False
    
    style_file = QFile(stylesheet_path)
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Error: Could not open stylesheet at {stylesheet_path}")
>>>>>>> liblouis/main
        return False
    
    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()
    widget.setStyleSheet(style_sheet)
    
    style_file.close()
<<<<<<< HEAD
=======
    print(f"Successfully loaded styles from: {stylesheet_path}")
>>>>>>> liblouis/main
    return True
