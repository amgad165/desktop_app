from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize theme state
        self.is_dark_mode = False
        
        # Setup sidebar connections and styles
        self.setup_sidebar_connections()
        self.setup_sidebar_icons()
        self.apply_sidebar_styles()
        
        # Set initial active item
        self.current_label = None
        
    def setup_sidebar_icons(self):
        # Setup icons for all sidebar items
        icon_size = 24
        
        # Home
        self.ui.homeIcon.setPixmap(QPixmap("resources/icons/home.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.homeIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Document
        self.ui.documentIcon.setPixmap(QPixmap("resources/icons/document.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.documentIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Products
        self.ui.productsIcon.setPixmap(QPixmap("resources/icons/products.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.productsIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Customers
        self.ui.customersIcon.setPixmap(QPixmap("resources/icons/customers.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.customersIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Workers
        self.ui.workersIcon.setPixmap(QPixmap("resources/icons/workers.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.workersIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Casher
        self.ui.casherIcon.setPixmap(QPixmap("resources/icons/casher.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.casherIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        # Orders
        self.ui.ordersIcon.setPixmap(QPixmap("resources/icons/orders.png").scaled(
            icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.ui.ordersIcon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
    def setup_sidebar_connections(self):
        # Connect all containers to the click handler
        containers = [
            self.ui.homeContainer,
            self.ui.documentContainer,
            self.ui.productsContainer,
            self.ui.customersContainer,
            self.ui.workersContainer,
            self.ui.casherContainer,
            self.ui.ordersContainer
        ]
        
        for container in containers:
            container.mousePressEvent = lambda event, c=container: self.handle_sidebar_click(c)
            container.setCursor(Qt.PointingHandCursor)
    
    def handle_sidebar_click(self, container):
        # Reset all containers to default style
        for c in [
            self.ui.homeContainer,
            self.ui.documentContainer,
            self.ui.productsContainer,
            self.ui.customersContainer,
            self.ui.workersContainer,
            self.ui.casherContainer,
            self.ui.ordersContainer
        ]:
            c.setStyleSheet("""
                QFrame {
                    background-color: #6b87b6;
                    border-radius: 12px;
                    padding: 10px;
                }
                QLabel {
                    color: black;
                    font-family: 'Poppins';
                    font-size: 15px;
                    font-weight: bold;
                }
            """)
        
        # Set the clicked container to active style
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QLabel {
                color: black;
                font-family: 'Poppins';
                font-size: 15px;
                font-weight: bold;
            }
        """)
        
        # Store current active container
        self.current_label = container
    
    def toggle_sidebar_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_sidebar_styles()
    
    def apply_sidebar_styles(self):
        sidebar_items = [
            self.ui.homeContainer,
            self.ui.documentContainer,
            self.ui.productsContainer,
            self.ui.customersContainer,
            self.ui.workersContainer,
            self.ui.casherContainer,
            self.ui.ordersContainer
        ]
        
        # Set colors based on theme
        sidebar_bg = "#2c2c2c" if self.is_dark_mode else "#e3e3e3"
        button_bg = "#3c4f6d" if self.is_dark_mode else "#6b87b6"
        text_color = "#ffffff" if self.is_dark_mode else "#000000"
        
        # Apply sidebar background
        self.ui.sidebar.setStyleSheet(f"""
            QFrame#sidebar {{
                background-color: {sidebar_bg};
                border: none;
                padding: 12px;
            }}
        """)
        
        # Apply styles to all containers
        for container in sidebar_items:
            container.setStyleSheet(f"""
                QFrame {{
                    background-color: {button_bg};
                    border-radius: 12px;
                    padding: 10px;
                    min-height: 40px;
                    max-height: 48px;
                }}
                QFrame:hover {{
                    background-color: #ffffff;
                }}
                QLabel {{
                    color: {text_color};
                    font-family: 'Poppins';
                    font-size: 15px;
                    font-weight: bold;
                    padding-left: 12px;
                }}
            """)
        
        # Re-apply active state if there is one
        if self.current_label:
            self.current_label.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 12px;
                    padding: 10px;
                    min-height: 40px;
                    max-height: 48px;
                }
                QLabel {
                    color: black;
                    font-family: 'Poppins';
                    font-size: 15px;
                    font-weight: bold;
                    padding-left: 12px;
                }
            """)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_() 