from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QStackedWidget, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
from app.models.app_models import CompanyDetails, session
from app.views.settings.nummernvergabe_page import NummernvergabePage  # Import NummernvergabePage
from app.views.settings.standard_page import StandardPage
from app.views.settings.bankverbindung_page import BankverbindungPage  # Import BankverbindungPage

class CompanyDetailsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_company_details()

    def init_ui(self):
        main_layout = QVBoxLayout(self)  # Main vertical layout

        # --- Back Button Layout ---
        top_layout = QHBoxLayout()
        self.back_button = QPushButton(self)
        self.back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        self.back_button.setIconSize(QSize(24, 24))
        self.back_button.setStyleSheet("border: none; background-color: transparent;")
        self.back_button.clicked.connect(self.parent.go_back_to_settings_page)
        top_layout.addWidget(self.back_button)
        top_layout.addStretch(1)  # Push everything else to the right

        # --- Main Content Layout ---
        content_layout = QHBoxLayout()  # Main horizontal layout (Sidebar + Content)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(400)
        self.sidebar.setSpacing(10)

        # Sidebar items
        items = ["Firmendaten", "Bankverbindung", "Währung", "Nummernvergabe"]
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setSizeHint(QSize(220, 60))
            list_item.setTextAlignment(Qt.AlignCenter)

            # Set font bold and larger size
            font = QFont()
            font.setBold(True)
            font.setPointSize(14)
            list_item.setFont(font)

            self.sidebar.addItem(list_item)

        # Sidebar styling
        self.sidebar.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                background-color: #e8e4e4;
                padding: 10px;
                font-size: 20px;
                font-weight: bold;
                color: black;
                height: 60px;
                border-radius: 15px;
                margin: 5px 0px;
            }
            QListWidget::item:selected {
                background-color: #b8b4b4;
                font-weight: bold;
            }
            QListWidget::item:focus {
                outline: none;
            }
        """)

        # Default selection
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.switch_section)
        sidebar_layout.addWidget(self.sidebar)

        # Content Area - Rounded Container
        content_container = QWidget()
        content_container.setStyleSheet("""
            background-color: #e6e6e6;
            border-radius: 15px;
            padding: 8px;
        """)

        content_stack_layout = QVBoxLayout(content_container)
        self.content_stack = QStackedWidget()
        self.content_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Sections
        self.firmendaten_widget = self.create_firmendaten_section()
        self.bankverbindung_widget = BankverbindungPage(self)
        self.währung_widget = StandardPage(self)  # Placeholder
        self.nummernvergabe_widget = NummernvergabePage(self)  # Use NummernvergabePage

        self.content_stack.addWidget(self.firmendaten_widget)
        self.content_stack.addWidget(self.bankverbindung_widget)
        self.content_stack.addWidget(self.währung_widget)
        self.content_stack.addWidget(self.nummernvergabe_widget)

        content_stack_layout.addWidget(self.content_stack)
        content_layout.addLayout(sidebar_layout)
        content_layout.addWidget(content_container)

        # Add layouts to the main layout
        main_layout.addLayout(top_layout)  # Back button at the top
        main_layout.addLayout(content_layout)  # Sidebar + Content

        self.setLayout(main_layout)


    def create_firmendaten_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        def create_field(label_text):
            container = QHBoxLayout()
            label = QLabel(label_text, self)
            label.setFixedWidth(150)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setStyleSheet("font-weight: bold;")

            input_field = QLineEdit(self)
            input_field.setStyleSheet("background-color: #f2f2f2; border-radius: 5px; padding: 2px; color: black;")

            container.addWidget(label)
            container.addWidget(input_field)
            return container, input_field

        # Input Fields
        self.anrede_input_layout, self.anrede_input = create_field("Anrede:")
        self.firmenname_input_layout, self.firmenname_input = create_field("Firmenname:")
        self.vorname_input_layout, self.vorname_input = create_field("Vorname:")
        self.nachname_input_layout, self.nachname_input = create_field("Nachname:")
        self.adresse_input_layout, self.adresse_input = create_field("Adresse:")
        self.plz_input_layout, self.plz_input = create_field("PLZ:")
        self.ort_input_layout, self.ort_input = create_field("Ort:")
        self.land_input_layout, self.land_input = create_field("Land:")
        self.telefon_input_layout, self.telefon_input = create_field("Telefon:")
        self.fax_input_layout, self.fax_input = create_field("Fax:")
        self.email_input_layout, self.email_input = create_field("E-Mail:")
        self.firmenbuchnummer_input_layout, self.firmenbuchnummer_input = create_field("Firmenbuchnummer:")
        self.steuernummer_input_layout, self.steuernummer_input = create_field("Steuernummer:")

        # Add Fields to Layout
        for input_layout in [
            self.anrede_input_layout, self.firmenname_input_layout, self.vorname_input_layout, self.nachname_input_layout,
            self.adresse_input_layout, self.plz_input_layout, self.ort_input_layout, self.land_input_layout,
            self.telefon_input_layout, self.fax_input_layout, self.email_input_layout, self.firmenbuchnummer_input_layout,
            self.steuernummer_input_layout
        ]:
            layout.addLayout(input_layout)
            layout.addSpacing(0)

        # Logo Upload
        self.logo_image_label = QLabel(self)
        self.logo_image_label.setFixedSize(120, 100)
        self.logo_image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; background: white;")

        self.upload_button = QPushButton("Upload Logo", self)
        self.upload_button.setFixedWidth(250)
        self.upload_button.setFixedHeight(30)
        self.upload_button.setStyleSheet("""
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
        """)
        self.upload_button.clicked.connect(self.upload_logo)

        logo_layout = QHBoxLayout()
        logo_layout.addWidget(self.logo_image_label)
        logo_layout.addWidget(self.upload_button)
        layout.addLayout(logo_layout)

        # Save Button
#        Save Button
        self.save_button = QPushButton("Speichern", self)
        self.save_button.setFixedSize(120, 35)  # Set button size
        self.save_button.setStyleSheet("""
            background-color: #000000; 
            color: white; 
            padding: 5px; 
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
        """)
        self.save_button.clicked.connect(self.save_company_details)

        # Center the button
        save_button_layout = QHBoxLayout()
        save_button_layout.addStretch()
        save_button_layout.addWidget(self.save_button)
        save_button_layout.addStretch()

        layout.addLayout(save_button_layout)  # Add centered button to main layout

        return widget

    def switch_section(self, index):
        self.content_stack.setCurrentIndex(index)

    def load_company_details(self):
        company_details = session.query(CompanyDetails).first()
        if company_details:
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
            if company_details.logo_image:
                pixmap = QPixmap()
                pixmap.loadFromData(company_details.logo_image)
                self.logo_image_label.setPixmap(pixmap.scaled(120, 100, Qt.KeepAspectRatio))

    def upload_logo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.logo_image_path = selected_files[0]
                pixmap = QPixmap(self.logo_image_path)
                self.logo_image_label.setPixmap(pixmap.scaled(120, 100, Qt.KeepAspectRatio))

    def save_company_details(self):
        QMessageBox.information(self, "Success", "Company details updated successfully!")
