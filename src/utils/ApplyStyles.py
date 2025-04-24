import os
from PyQt5.QtCore import QFile, QTextStream

def apply_styles(widget):
    stylesheet_path = os.path.abspath("./src/styles.qss")

    if not os.path.exists(stylesheet_path):
        print(f"ERROR: Stylesheet not found at {stylesheet_path}")
        return False

    style_file = QFile(stylesheet_path)
    
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        print(f"ERROR: Failed to open stylesheet: {stylesheet_path}")
        return False

    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()

    if not style_sheet.strip():
        print("ERROR: Stylesheet is empty!")
        return False

    widget.setStyleSheet(style_sheet)
    style_file.close()
    
    print("✅ Stylesheet applied successfully!")
    return True
