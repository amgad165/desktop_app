from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)  # Set the height of the title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Layout for the title bar
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)
        
        # Icon label
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QIcon("path/to/icon.png").pixmap(QSize(20, 20)))  # Replace with your icon path
        self.layout.addWidget(self.icon_label)

        # Title label
        self.title_label = QLabel("App Title", self)
        self.title_label.setStyleSheet("color: white;")  # Customize the style
        self.layout.addWidget(self.title_label)

        # Add a stretch to push buttons to the right
        self.layout.addStretch()

        # Minimize button
        self.minimize_button = QPushButton("-", self)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("background-color: #2e2e2e; border: none; color: white;")
        self.minimize_button.clicked.connect(self.minimize_window)
        self.layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("x", self)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: #2e2e2e; border: none; color: white;")
        self.close_button.clicked.connect(self.close_window)
        self.layout.addWidget(self.close_button)

    def minimize_window(self):
        self.parent().showMinimized()

    def close_window(self):
        self.parent().close()
