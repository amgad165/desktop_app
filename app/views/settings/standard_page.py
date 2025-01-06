from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QRadioButton, QHBoxLayout,QPushButton, QFormLayout, QMessageBox, QButtonGroup, QWidget
from app.models.app_models import billSettings, session
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class StandardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setupUi()
        self.load_settings()

    def setupUi(self):
        self.setObjectName("StandardPage")
        self.resize(600, 400)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("mainLayout")

        # Top Layout for Back Button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("border: none; background-color: transparent;")
        back_button.clicked.connect(self.parent.go_back_to_settings_page)

        top_layout.addWidget(back_button)
        self.layout.addLayout(top_layout)


        # Header label
        self.headerLabel = QLabel("Standard Einstellungen", self)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.headerLabel.setFont(font)
        self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.headerLabel)

        # Form layout for settings
        self.formLayout = QFormLayout()
        self.formLayout.setHorizontalSpacing(20)
        self.layout.addLayout(self.formLayout)

        # Styling: Smaller inputs, centered rows
        self.inputStyle = "padding: 5px; width: 100px; border: 1px solid #ccc; border-radius: 3px;"
        self.radioStyle = "QRadioButton { padding: 0px; background: none; border: none; }"

        # Currency
        self.currencyLabel = QLabel("Währung:", self)
        self.currencySelect = QComboBox(self)
        self.currencySelect.addItems(["$", "€", "£"])
        self.currencySelect.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_centered_row(self.currencyLabel, self.currencySelect))

        # Decimal Places
        self.decimalPlacesLabel = QLabel("Dezimalstellen:", self)
        self.decimalPlacesInput = QLineEdit(self)
        self.decimalPlacesInput.setPlaceholderText("z.B. 2")
        self.decimalPlacesInput.setStyleSheet(self.inputStyle)
        self.decimalPlacesInput.setMaximumWidth(100)
        self.formLayout.addRow(self.create_centered_row(self.decimalPlacesLabel, self.decimalPlacesInput))


        # Prices
        self.pricesIsLabel = QLabel("Preise in:", self)
        self.pricesIsSelect = QComboBox(self)
        self.pricesIsSelect.addItems(["Brutto", "Netto"])
        self.pricesIsSelect.setStyleSheet(self.inputStyle)
        self.formLayout.addRow(self.create_centered_row(self.pricesIsLabel, self.pricesIsSelect))

        # VAT
        self.vatLabel = QLabel("Mehrwertsteuer (MwSt):", self)
        self.vatLayout = QtWidgets.QHBoxLayout()
        self.vatRadioGroup = QButtonGroup(self)
        self.vat0 = QRadioButton("0 %")
        self.vat10 = QRadioButton("10 %")
        self.vat20 = QRadioButton("20 %")
        self.vatRadioGroup.addButton(self.vat0, 0)
        self.vatRadioGroup.addButton(self.vat10, 10)
        self.vatRadioGroup.addButton(self.vat20, 20)
        self.vat10.setChecked(True)
        self.vat0.setStyleSheet(self.radioStyle)
        self.vat10.setStyleSheet(self.radioStyle)
        self.vat20.setStyleSheet(self.radioStyle)
        self.vatLayout.addWidget(self.vat0)
        self.vatLayout.addWidget(self.vat10)
        self.vatLayout.addWidget(self.vat20)
        vatContainer = QWidget(self)
        vatContainer.setLayout(self.vatLayout)
        self.formLayout.addRow(self.create_centered_row(self.vatLabel, vatContainer))

        # Save button
        self.saveButton = QPushButton("Speichern", self)
        self.saveButton.setMinimumHeight(40)
        self.saveButton.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.layout.addWidget(self.saveButton, alignment=QtCore.Qt.AlignCenter)

        # Connect signals
        self.saveButton.clicked.connect(self.save_settings)

    def create_centered_row(self, label, input_widget):
        """Helper to create a row with label and input closely aligned."""
        rowLayout = QtWidgets.QGridLayout()
        rowLayout.setAlignment(QtCore.Qt.AlignCenter)
        rowLayout.addWidget(label, 0, 0, alignment=QtCore.Qt.AlignRight)
        rowLayout.addWidget(input_widget, 0, 1, alignment=QtCore.Qt.AlignLeft)
        container = QWidget(self)
        container.setLayout(rowLayout)
        return container

    def load_settings(self):
        """Load settings from the database and populate the UI."""
        settings = session.query(billSettings).first()
        if settings:
            self.currencySelect.setCurrentText(settings.currency)
            self.decimalPlacesInput.setText(str(settings.decimal_places))
            self.pricesIsSelect.setCurrentText(settings.prices_is)
            for button in self.vatRadioGroup.buttons():
                if self.vatRadioGroup.id(button) == settings.VAT:
                    button.setChecked(True)
                    break

    def save_settings(self):
        """Save or update the settings in the database."""
        # Validate input
        decimal_places = self.decimalPlacesInput.text()
        if not decimal_places.isdigit():
            QMessageBox.warning(self, "Eingabefehler", "Dezimalstellen müssen eine Zahl sein.")
            return

        # Get values from UI
        currency = self.currencySelect.currentText()
        decimal_places = int(decimal_places)
        prices_is = self.pricesIsSelect.currentText()
        vat = self.vatRadioGroup.checkedId()

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
