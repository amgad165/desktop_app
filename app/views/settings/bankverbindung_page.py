from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from app.models.app_models import session, Bankverbindung

class BankverbindungPage(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.initUI()
        self.load_bankverbindung()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("Bankverbindung")
        title_label.setAlignment(Qt.AlignCenter)  # Centering the title
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.institut_input = self.create_input_field(form_layout, "Institut:")
        self.inhaber_input = self.create_input_field(form_layout, "Inhaber:")
        self.iban_input = self.create_input_field(form_layout, "IBAN:")
        self.bic_input = self.create_input_field(form_layout, "BIC:")

        # Add form layout to main layout
        main_layout.addLayout(form_layout)

        # Spacer to push the button down
        main_layout.addStretch()

        # Save button container (Centered)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)  

        self.save_button = QPushButton("Speichern")
        self.save_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 10px 25px;
            border-radius: 5px;
            font-size: 14px;
        """)
        self.save_button.clicked.connect(self.save_bankverbindung)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_input_field(self, layout, label_text):
        container = QHBoxLayout()  # Use horizontal layout for label : input
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold;")
        label.setFixedWidth(100)  # Adjust label width for alignment

        input_field = QLineEdit()
        input_field.setStyleSheet("color: black; padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
        input_field.setFixedHeight(30)

        container.addWidget(label)
        container.addWidget(input_field)
        layout.addLayout(container)

        return input_field

    def load_bankverbindung(self):
        bank_data = session.query(Bankverbindung).first()
        if bank_data:
            self.institut_input.setText(bank_data.institut)
            self.inhaber_input.setText(bank_data.inhaber)
            self.iban_input.setText(bank_data.iban)
            self.bic_input.setText(bank_data.bic)

    def save_bankverbindung(self):
        bank_data = session.query(Bankverbindung).first()

        if bank_data:
            # Update existing data
            bank_data.institut = self.institut_input.text()
            bank_data.inhaber = self.inhaber_input.text()
            bank_data.iban = self.iban_input.text()
            bank_data.bic = self.bic_input.text()
        else:
            # Insert new data
            new_bank = Bankverbindung(
                institut=self.institut_input.text(),
                inhaber=self.inhaber_input.text(),
                iban=self.iban_input.text(),
                bic=self.bic_input.text()
            )
            session.add(new_bank)

        session.commit()
        QMessageBox.information(self, "Erfolg", "Bankverbindung gespeichert!")
