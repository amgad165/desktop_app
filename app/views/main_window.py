from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QGraphicsOpacityEffect, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QPoint
from PyQt5.QtGui import QIcon
from ui.ui_main_window import Ui_MainWindow
from app.controllers.create_bill_controller import CreateBillController

class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CustomTitleBar")
        self.setFrameShape(QFrame.NoFrame)
        self.setFixedHeight(50)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 10, 5, 10)
        self.layout.setSpacing(10)

        # Title label
        self.title_label = QLabel("App Title", self)
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setObjectName("minimize_button")
        minimize_icon = QIcon("resources/icons/window_minimize.png")
        self.minimize_button.setIcon(minimize_icon)
        self.minimize_button.setIconSize(QSize(20, 20))
        self.minimize_button.clicked.connect(self.minimize_window)
        self.layout.addWidget(self.minimize_button)

        # Fullscreen button
        self.fullscreen_button = QPushButton(self)
        self.fullscreen_button.setFixedSize(30, 30)
        self.fullscreen_button.setObjectName("fullscreen_button")
        fullscreen_icon = QIcon("resources/icons/square.png")
        self.fullscreen_button.setIcon(fullscreen_icon)
        self.fullscreen_button.setIconSize(QSize(20, 20))
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.layout.addWidget(self.fullscreen_button)

        # Close button
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("close_button")
        close_icon = QIcon("resources/icons/window_close.png")
        self.close_button.setIcon(close_icon)
        self.close_button.setIconSize(QSize(20, 20))
        self.close_button.clicked.connect(self.close_window)
        self.layout.addWidget(self.close_button)

        # Variables to track mouse dragging
        self._is_dragging = False
        self._start_pos = QPoint()

    def minimize_window(self):
        if self.window():
            self.window().showMinimized()

    def toggle_fullscreen(self):
        if self.window().isFullScreen():
            self.window().showNormal()
        else:
            self.window().showFullScreen()

    def close_window(self):
        if self.window():
            self.window().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._start_pos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self.window().move(event.globalPos() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            event.accept()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("border-radius: 10px;")  # Rounded edges

        # Custom title bar
        self.title_bar = CustomTitleBar(self)

        # Central widget to hold the title bar and main content
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(3)

        # Add title bar
        central_layout.addWidget(self.title_bar)

        # Add the stacked widget (main content)
        central_layout.addWidget(self.centralwidget)
        self.setCentralWidget(central_widget)

        # Set up CreateBillController
        self.create_bill_controller = CreateBillController(self.stackedWidget)
        self.create_bill_controller.setup_connections()

        # Set up HomePage with a "Welcome to the app" label
        self.homePage = QWidget()
        self.homeLayout = QVBoxLayout(self.homePage)
        self.welcomeLabel = QLabel("Welcome to the app")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.homeLayout.addWidget(self.welcomeLabel)

        # Add widgets to stackedWidget
        self.stackedWidget.addWidget(self.homePage)
        self.stackedWidget.addWidget(self.create_bill_controller.create_bill_page)

        # Initialize highlighted label
        self.current_label = None

        # Initialize the fade animation
        self.fade_effect = QGraphicsOpacityEffect(self.stackedWidget)
        self.stackedWidget.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(1000)  # Duration in milliseconds

        # Connect signals
        self.setup_connections()

        # Set the default page to home
        self.show_home_page()

    def setup_connections(self):
        self.homeLabel.mousePressEvent = lambda event: self.show_home_page()
        self.createBillLabel.mousePressEvent = lambda event: self.show_create_bill_page()

    def highlight_label(self, label):
        if self.current_label:
            self.current_label.setStyleSheet("")
        label.setStyleSheet("border: 2px solid #31112C; background-color: #0a0d12;")
        self.current_label = label

    def show_home_page(self):
        print("Showing home page")
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stackedWidget.setCurrentWidget(self.homePage)
        self.highlight_label(self.homeContainer)

    def show_create_bill_page(self):
        print("Showing create bill page")
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stackedWidget.setCurrentWidget(self.create_bill_controller.create_bill_page)
        self.highlight_label(self.createBillContainer)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
