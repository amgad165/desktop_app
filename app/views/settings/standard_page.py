from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QHBoxLayout, QPushButton, QFormLayout, QMessageBox, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from app.models.app_models import billSettings, session

class StandardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi()
        self.load_settings()

    def setupUi(self):
        self.setObjectName("StandardPage")
        self.resize(600, 400)

        # Main vertical layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignTop)

        # Header label
        self.headerLabel = QLabel("Einstellungen", self)
        self.headerLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.headerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.headerLabel)

        # Form layout for settings
        self.formLayout = QFormLayout()
        self.formLayout.setHorizontalSpacing(20)

        # Input style (matching NummernvergabePage)
        self.inputStyle = """
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
            color: black;
            height: 30px;
            font-size: 14px;
        """

        # Currency
        self.currencyLabel = QLabel("Währung:", self)
        self.currencyLabel.setStyleSheet("font-weight: bold;")
        self.currencySelect = QComboBox(self)
        self.currencySelect.addItems(["$", "€", "£"])
        self.currencySelect.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_input_row(self.currencyLabel, self.currencySelect))

        # Decimal Places
        self.decimalPlacesLabel = QLabel("Nachkommastellen:", self)
        self.decimalPlacesLabel.setStyleSheet("font-weight: bold;")
        self.decimalPlacesInput = QLineEdit(self)
        self.decimalPlacesInput.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_input_row(self.decimalPlacesLabel, self.decimalPlacesInput))

        # Prices
        self.pricesIsLabel = QLabel("Preise in:", self)
        self.pricesIsLabel.setStyleSheet("font-weight: bold;")
        self.pricesIsSelect = QComboBox(self)
        self.pricesIsSelect.addItems(["Brutto", "Netto"])
        self.pricesIsSelect.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_input_row(self.pricesIsLabel, self.pricesIsSelect))

        # VAT (MwSt)
        self.vatLabel = QLabel("Mehrwertsteuer (MwSt):", self)
        self.vatLabel.setStyleSheet("font-weight: bold;")
        self.vatInput = QLineEdit(self)
        self.vatInput.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_input_row(self.vatLabel, self.vatInput))

        # Add form layout to main layout
        self.layout.addLayout(self.formLayout)

        # **Spacer to push button to the bottom**
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Save button (centered, normal size)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setAlignment(Qt.AlignCenter)

        self.saveButton = QPushButton("Speichern", self)
        self.saveButton.setFixedSize(120, 45)  # Standard button size
        self.saveButton.setStyleSheet("""
            background-color: black;
            color: white;
            border-radius: 5px;
            font-size: 14px;                   
        """)
        self.saveButton.clicked.connect(self.save_settings)

        self.buttonLayout.addWidget(self.saveButton)
        self.layout.addLayout(self.buttonLayout)

    def create_input_row(self, label, input_widget):
        """Creates a row with bold label and input field of equal width."""
        row = QHBoxLayout()
        label.setFixedWidth(250)  # Aligns with NummernvergabePage label width
        row.addWidget(label)
        row.addWidget(input_widget)
        return row

    def load_settings(self):
        """Load settings from the database and populate the UI."""
        settings = session.query(billSettings).first()
        if settings:
            self.currencySelect.setCurrentText(settings.currency)
            self.decimalPlacesInput.setText(str(settings.decimal_places))
            self.pricesIsSelect.setCurrentText(settings.prices_is)
            self.vatInput.setText(str(settings.VAT))

    def save_settings(self):
        """Save or update the settings in the database."""
        decimal_places = self.decimalPlacesInput.text()
        vat = self.vatInput.text()

        if not decimal_places.isdigit():
            QMessageBox.warning(self, "Eingabefehler", "Dezimalstellen müssen eine Zahl sein.")
            return

        if not vat.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Eingabefehler", "MwSt muss eine Zahl sein.")
            return

        # Get values from UI
        currency = self.currencySelect.currentText()
        decimal_places = int(decimal_places)
        prices_is = self.pricesIsSelect.currentText()
        vat = float(vat)

        # Save to database
        settings = session.query(billSettings).first()
        if settings:
            settings.currency = currency
            settings.decimal_places = decimal_places
            settings.prices_is = prices_is
            settings.VAT = vat
        else:
            settings = billSettings(
                currency=currency,
                decimal_places=decimal_places,
                prices_is=prices_is,
                VAT=vat
            )
            session.add(settings)

        session.commit()
        QMessageBox.information(self, "Gespeichert", "Einstellungen wurden erfolgreich gespeichert.")
