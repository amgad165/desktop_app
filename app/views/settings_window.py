from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QStackedWidget, QLineEdit, QFileDialog, QGraphicsOpacityEffect, QMessageBox,QSpacerItem

from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QIcon, QPixmap
from app.views.settings.company_details_page import CompanyDetailsPage
from app.views.settings.nummernvergabe_page import NummernvergabePage
from app.views.settings.einstellungen_page import EinstellungenPage
from app.views.settings.standard_page import StandardPage

class HoverFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        # Placeholder for click event connection
        self.click_action = None

    def mousePressEvent(self, event):
        # Trigger the click action if one is set
        if self.click_action:
            self.click_action()
        super().mousePressEvent(event)

    def set_click_action(self, action):
        # Set the click action for the frame
        self.click_action = action

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(1000, 750)
        self.setObjectName("settingsWindow")

        # Create a stacked widget to manage different pages
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setObjectName("settingsStackedWidget")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)
        
        # Set up the settings page content
        self.settings_page = QWidget()
        self.stacked_widget.addWidget(self.settings_page)
        self.show_settings_page()

        # Set up the first page (CompanyDetailsPage)
        self.company_details_page = CompanyDetailsPage(self)
        self.nummernvergabe_page = NummernvergabePage(self)
        self.einstellungenPage = EinstellungenPage(self)
        self.standard_page = StandardPage(self)
        self.stacked_widget.addWidget(self.company_details_page)
        self.stacked_widget.addWidget(self.nummernvergabe_page)
        self.stacked_widget.addWidget(self.einstellungenPage)
        self.stacked_widget.addWidget(self.standard_page)

    def show_settings_page(self):
        # Main layout for the settings page
        main_layout = QVBoxLayout(self.settings_page)
        main_layout.setAlignment(Qt.AlignCenter)  # Center the layout both vertically and horizontally
        main_layout.setObjectName("settingsLayout")  # Set object name for styling

        # Button properties
        button_size = QSize(150, 150)  # Size of the QFrame
        icon_size = QSize(70, 70)  # Icon size

        # Icons and labels for buttons
        button_data = [
            ("resources/icons/assured_workload.png", "Firma"),
            ("resources/icons/assignment_late.png", "Nummernvergabe"),
            ("resources/icons/settings.png", "Einstellungen"),
            ("resources/icons/rule.png", "Standard"),
            # ("resources/icons/box.png", "Button 5"),
            # ("resources/icons/box.png", "Button 6")
        ]

        # Create buttons and arrange them in rows of 3
        for i in range(0, len(button_data), 3):
            row_layout = QHBoxLayout()  # Horizontal layout for each row
            row_layout.setAlignment(Qt.AlignCenter)
            main_layout.addLayout(row_layout)

            for j in range(3):
                if i + j < len(button_data):
                    icon_path, label_text = button_data[i + j]

                    # Create the custom hover frame to hold the button and label
                    frame = HoverFrame()
                    frame.setFixedSize(button_size)
                    frame.setObjectName(f"settingsButton")  # Unique name for each frame

                    # Create a vertical layout inside the frame to place the button and the label
                    frame_layout = QVBoxLayout(frame)
                    frame_layout.setAlignment(Qt.AlignCenter)
                    frame_layout.setContentsMargins(0, 0, 0, 0)
                    frame_layout.setSpacing(5)  # Add some spacing between the button and label

                    # Create a button with an icon
                    button = QPushButton()
                    button.setFixedSize(icon_size)
                    button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    button.setStyleSheet("border: none;")  # Remove button borders
                    button.setObjectName(f"icon_object")  # Unique name for each button
                    button.setEnabled(False)
                    button.setAttribute(Qt.WA_TransparentForMouseEvents, True)

                    # Create a QIcon for the button
                    button.setIcon(QIcon(icon_path))
                    button.setIconSize(icon_size)
                    button.setFixedWidth(140)
                    # Connect the frame's click action to the page change slot
                    if label_text == "Firma":
                        frame.set_click_action(self.show_company_details_page)

                    elif label_text == "Nummernvergabe":
                        frame.set_click_action(self.show_nummernvergabe_details_page)

                    elif label_text == "Einstellungen":
                        frame.set_click_action(self.show_einstellungen_page)
                        
                    elif label_text == "Standard":
                        frame.set_click_action(self.show_standard_page)
                        

                    # Create the label for the button
                    label = QLabel(label_text)
                    label.setAlignment(Qt.AlignCenter)
                    label.setObjectName("buttonLabel")  # Set object name for styling

                    # Add the button and label to the frame layout
                    frame_layout.addWidget(button)  # Add the button
                    frame_layout.addWidget(label)  # Add the label

                    # Add the frame to the row layout
                    row_layout.addWidget(frame)

    def show_company_details_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(3000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.company_details_page)


    def show_nummernvergabe_details_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(3000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.nummernvergabe_page)


    def show_einstellungen_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(3000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.einstellungenPage)


    def show_standard_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(3000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.standard_page)

    def go_back_to_settings_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(2000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.settings_page)


