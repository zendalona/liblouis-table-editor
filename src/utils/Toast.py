from PyQt6.QtWidgets import QLabel, QHBoxLayout, QFrame
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, QTimer

class Toast(QFrame):
    def __init__(self, text, icon_path, colorR, colorG, colorB, parent=None):
        super().__init__(parent)
        self.initUI(text, icon_path, colorR, colorG, colorB)

    def initUI(self, text, icon_path, colorR, colorG, colorB):
        self.setFixedSize(350, 60)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        
        def lighter_color(r, g, b, factor=0.7):
            return QColor(
                int(r + (255 - r) * factor),
                int(g + (255 - g) * factor),
                int(b + (255 - b) * factor)
            )
        
        background_color = lighter_color(colorR, colorG, colorB)

        # Apply styles
        self.setStyleSheet(f"""
            Toast {{
                background-color: {background_color.name()};
                border: 2px solid rgb({colorR}, {colorG}, {colorB});
            }}
            QLabel {{
                background-color: {background_color.name()};
            }}
        """)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))
        layout.addWidget(icon_label)

        text_label = QLabel(text, self)
        layout.addWidget(text_label)

        layout.setContentsMargins(5, 2, 10, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_toast(self, duration=2000):
        self.show()
        QTimer.singleShot(duration, self.hide)
