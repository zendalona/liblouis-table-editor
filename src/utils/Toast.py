from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QApplication
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

class Toast(QFrame):
    def __init__(self, text, icon_path, colorR, colorG, colorB, parent=None):
        super().__init__(parent)
        self.initUI(text, icon_path, colorR, colorG, colorB)

    def initUI(self, text, icon_path, colorR, colorG, colorB):
        self.setFixedSize(350, 60)  
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        def lighter_color(r, g, b, factor=0.95): 
            return QColor(
                int(r + (255 - r) * factor),
                int(g + (255 - g) * factor),
                int(b + (255 - b) * factor)
            )
        
        background_color = lighter_color(colorR, colorG, colorB)

        self.setStyleSheet(f"""
            Toast {{
                background-color: {background_color.name()};
                border: 2px solid rgb({colorR}, {colorG}, {colorB});
                border-radius: 10px;
            }}
            QLabel {{
                background-color: transparent;
                color: #222222;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }}
        """)
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon(icon_path).pixmap(24, 24))  
        icon_label.setFixedSize(28, 28)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        text_label = QLabel(text, self)
        font = QFont('Segoe UI', 12)  
        font.setWeight(QFont.DemiBold)  
        text_label.setFont(font)
        text_label.setAlignment(Qt.AlignVCenter)
        layout.addWidget(text_label)

        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)

    def show_toast(self, duration=2000):
        screen = QApplication.primaryScreen().geometry()
        
        x = (screen.width() - self.width()) // 2
        y = screen.height() // 6  
        
        self.move(x, y)
        self.show()
        QTimer.singleShot(duration, self.hide)
