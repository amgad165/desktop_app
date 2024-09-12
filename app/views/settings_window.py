from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QStackedWidget, QLineEdit, QFileDialog, QGraphicsOpacityEffect, QMessageBox,QSpacerItem

from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QIcon, QPixmap
from app.models.app_models import CompanyDetails, session

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
        self.stacked_widget.addWidget(self.company_details_page)

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
            ("resources/icons/database.png", "Button 1"),
            ("resources/icons/box.png", "Button 2"),
            ("resources/icons/box.png", "Button 3"),
            ("resources/icons/box.png", "Button 4"),
            ("resources/icons/box.png", "Button 5"),
            ("resources/icons/box.png", "Button 6")
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

                    # Connect the frame's click action to the page change slot
                    if label_text == "Button 1":
                        frame.set_click_action(self.show_company_details_page)

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

    def go_back_to_settings_page(self):
        self.fade_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.fade_effect)
        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(2000)  # Duration in milliseconds
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()
        self.stacked_widget.setCurrentWidget(self.settings_page)


class CompanyDetailsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_company_details()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 0, 20, 20)
        main_layout.setAlignment(Qt.AlignTop)

        # Back button
        back_button_layout = QHBoxLayout()
        back_button_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("border: none; background-color: transparent;")
        back_button.clicked.connect(self.parent.go_back_to_settings_page)

        back_button_layout.addWidget(back_button)
        main_layout.addLayout(back_button_layout)

        # Header label
        header_label = QLabel("Edit Company Details", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header_label)

        # Center layout
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Create and layout input fields
        self.anrede_input = QLineEdit(self)
        self.firmenname_input = QLineEdit(self)
        self.vorname_input = QLineEdit(self)
        self.nachname_input = QLineEdit(self)
        self.adresse_input = QLineEdit(self)
        self.plz_input = QLineEdit(self)
        self.ort_input = QLineEdit(self)
        self.land_input = QLineEdit(self)
        self.telefon_input = QLineEdit(self)
        self.fax_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.firmenbuchnummer_input = QLineEdit(self)
        self.steuernummer_input = QLineEdit(self)

        # Helper function to create a vertical layout for a label and input
        def create_field_layout(label_text, input_widget):
            layout = QVBoxLayout()
            layout.addWidget(QLabel(label_text, self))
            layout.addWidget(input_widget)
            return layout

        # Row 1: Anrede, Firmenname
        row1_layout = QHBoxLayout()
        row1_layout.addLayout(create_field_layout("Anrede:", self.anrede_input))
        row1_layout.addLayout(create_field_layout("Firmenname:", self.firmenname_input))
        center_layout.addLayout(row1_layout)

        # Row 2: Vorname, Nachname
        row2_layout = QHBoxLayout()
        row2_layout.addLayout(create_field_layout("Vorname:", self.vorname_input))
        row2_layout.addLayout(create_field_layout("Nachname:", self.nachname_input))
        center_layout.addLayout(row2_layout)

        # Row 3: Adresse
        row3_layout = QVBoxLayout()
        row3_layout.addLayout(create_field_layout("Adresse:", self.adresse_input))
        center_layout.addLayout(row3_layout)

        # Row 4: PLZ, Ort
        row4_layout = QHBoxLayout()
        row4_layout.addLayout(create_field_layout("PLZ:", self.plz_input))
        row4_layout.addLayout(create_field_layout("Ort:", self.ort_input))
        center_layout.addLayout(row4_layout)

        # Row 5: Land
        row5_layout = QVBoxLayout()
        row5_layout.addLayout(create_field_layout("Land:", self.land_input))
        center_layout.addLayout(row5_layout)

        # Row 6: Telefon, Fax
        row6_layout = QHBoxLayout()
        row6_layout.addLayout(create_field_layout("Telefon:", self.telefon_input))
        row6_layout.addLayout(create_field_layout("Fax:", self.fax_input))
        center_layout.addLayout(row6_layout)

        # Row 7: E-Mail
        row7_layout = QVBoxLayout()
        row7_layout.addLayout(create_field_layout("E-Mail:", self.email_input))
        center_layout.addLayout(row7_layout)

        # Row 8: Firmenbuchnummer, Steuernummer
        row8_layout = QHBoxLayout()
        row8_layout.addLayout(create_field_layout("Firmenbuchnummer:", self.firmenbuchnummer_input))
        row8_layout.addLayout(create_field_layout("Steuernummer:", self.steuernummer_input))
        center_layout.addLayout(row8_layout)

        # Add center layout to the main layout
        main_layout.addLayout(center_layout)

        # Layout for the logo and upload button
        logo_button_layout = QHBoxLayout()
        logo_button_layout.setAlignment(Qt.AlignCenter)

        # Label to display the logo
        self.logo_image_label = QLabel(self)
        self.logo_image_label.setFixedSize(120, 100)
        self.logo_image_label.setStyleSheet("border: 1px solid #ccc;")

        # Upload logo button
        self.upload_button = QPushButton("Upload Logo", self)
        self.upload_button.setIcon(QIcon("resources/icons/upload.png"))
        self.upload_button.setIconSize(QSize(16, 16))
        self.upload_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.upload_button.setFixedWidth(150)
        self.upload_button.setStyleSheet(
            """
            QPushButton {
                background-color: #007BFF;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                margin-top: 25px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )
        self.upload_button.clicked.connect(self.upload_logo)

        # Add logo and button to the logo_button_layout
        logo_button_layout.addWidget(self.logo_image_label)
        logo_button_layout.addWidget(self.upload_button)

        # Add logo_button_layout to the center_layout
        center_layout.addLayout(logo_button_layout)

        # Label to display the file path
        self.file_name_label = QLabel(self)
        self.file_name_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.file_name_label)

        # Save button
        self.save_button = QPushButton("Save Company Details", self)
        self.save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            """
        )
        self.save_button.clicked.connect(self.save_company_details)
        center_layout.addWidget(self.save_button)

        main_layout.addStretch()

    def load_company_details(self):
        # Query the database for the existing record
        company_details = session.query(CompanyDetails).first()
        
        if company_details:
            # Populate the input fields with existing values
            self.anrede_input.setText(company_details.anrede)
            self.firmenname_input.setText(company_details.firmenname)
            self.vorname_input.setText(company_details.vorname)
            self.nachname_input.setText(company_details.nachname)
            self.adresse_input.setText(company_details.adresse)
            self.plz_input.setText(company_details.plz)
            self.ort_input.setText(company_details.ort)
            self.land_input.setText(company_details.land)
            self.telefon_input.setText(company_details.telefon)
            self.fax_input.setText(company_details.fax or "")
            self.email_input.setText(company_details.email)
            self.firmenbuchnummer_input.setText(company_details.firmenbuchnummer)
            self.steuernummer_input.setText(company_details.steuernummer)

            # Display the logo image if available
            if company_details.logo_image:
                pixmap = QPixmap()
                pixmap.loadFromData(company_details.logo_image)
                self.logo_image_label.setPixmap(pixmap.scaled(120, 100, Qt.KeepAspectRatio))
            else:
                self.logo_image_label.clear()
                self.file_name_label.clear()

    def upload_logo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.List)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.logo_image_path = selected_files[0]
                pixmap = QPixmap(self.logo_image_path)
                self.logo_image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                self.file_name_label.clear()

    def save_company_details(self):
        # Get the data from the inputs
        anrede = self.anrede_input.text()
        firmenname = self.firmenname_input.text()
        vorname = self.vorname_input.text()
        nachname = self.nachname_input.text()
        adresse = self.adresse_input.text()
        plz = self.plz_input.text()
        ort = self.ort_input.text()
        land = self.land_input.text()
        telefon = self.telefon_input.text()
        fax = self.fax_input.text()
        email = self.email_input.text()
        firmenbuchnummer = self.firmenbuchnummer_input.text()
        steuernummer = self.steuernummer_input.text()

        # Convert image to binary data if a file was selected
        logo_image_data = None
        if hasattr(self, 'logo_image_path'):
            with open(self.logo_image_path, 'rb') as file:
                logo_image_data = file.read()

        # Check if a record already exists
        company_details = session.query(CompanyDetails).first()

        if company_details:
            # Update existing record
            company_details.anrede = anrede
            company_details.firmenname = firmenname
            company_details.vorname = vorname
            company_details.nachname = nachname
            company_details.adresse = adresse
            company_details.plz = plz
            company_details.ort = ort
            company_details.land = land
            company_details.telefon = telefon
            company_details.fax = fax
            company_details.email = email
            company_details.firmenbuchnummer = firmenbuchnummer
            company_details.steuernummer = steuernummer
            company_details.logo_image = logo_image_data
            print("Updating existing company details in the database.")
        else:
            # Insert new record
            company_details = CompanyDetails(
                anrede=anrede,
                firmenname=firmenname,
                vorname=vorname,
                nachname=nachname,
                adresse=adresse,
                plz=plz,
                ort=ort,
                land=land,
                telefon=telefon,
                fax=fax,
                email=email,
                firmenbuchnummer=firmenbuchnummer,
                steuernummer=steuernummer,
                logo_image=logo_image_data
            )
            session.add(company_details)
            print("Inserting new company details into the database.")

        session.commit()

        # Clear the form and show success message
        self.clear_form()
        self.show_success_message()

    def show_success_message(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Company details updated successfully!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def clear_form(self):
        self.anrede_input.clear()
        self.firmenname_input.clear()
        self.vorname_input.clear()
        self.nachname_input.clear()
        self.adresse_input.clear()
        self.plz_input.clear()
        self.ort_input.clear()
        self.land_input.clear()
        self.telefon_input.clear()
        self.fax_input.clear()
        self.email_input.clear()
        self.firmenbuchnummer_input.clear()
        self.steuernummer_input.clear()
        self.file_name_label.clear()
        self.logo_image_label.clear()
        if hasattr(self, 'logo_image_path'):
            del self.logo_image_path