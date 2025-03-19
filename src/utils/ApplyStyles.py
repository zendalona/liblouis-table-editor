# style_utils.py

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtCore import QIODevice

def apply_styles(widget):
    
    stylesheet_path = "./src/styles.qss"
    style_file = QFile(stylesheet_path)
    # if not style_file.open(QFile.ReadOnly | QFile.Text):
    if not style_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):

        print(f"Failed to open stylesheet: {stylesheet_path}")
        return False
    
    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()
    widget.setStyleSheet(style_sheet)
    
    style_file.close()
    return True
