# style_utils.py

from PyQt5.QtCore import QFile, QTextStream
import os

def apply_styles(widget):
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stylesheet_path = os.path.join(src_dir, "styles.qss")
    
    style_file = QFile(stylesheet_path)
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        return False
    
    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()
    widget.setStyleSheet(style_sheet)
    
    style_file.close()
    return True
