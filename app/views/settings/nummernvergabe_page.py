from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from app.models.app_models import Nummernvergabe, session


class NummernvergabePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.load_nummernvergabe()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignTop)

        # Top Layout with Back Button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)


        top_layout.addStretch(1)  # Push content to the right
        main_layout.addLayout(top_layout)

        # Header
        header_label = QLabel("Nummernvergabe Einstellungen", self)
        header_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Input fields
        self.betreff_angebot_input = QLineEdit(self)
        self.nummer_angebot_input = QLineEdit(self)
        self.betreff_lieferschein_input = QLineEdit(self)
        self.nummer_lieferschein_input = QLineEdit(self)
        self.betreff_rechnung_input = QLineEdit(self)
        self.nummer_rechnung_input = QLineEdit(self)

        # Remove placeholders & ensure text is black
        for input_field in [
            self.betreff_angebot_input, self.nummer_angebot_input,
            self.betreff_lieferschein_input, self.nummer_lieferschein_input,
            self.betreff_rechnung_input, self.nummer_rechnung_input
        ]:
            input_field.setPlaceholderText("")
            input_field.setStyleSheet("color: black;")  # Ensures text stays black

        def create_input_row(label, input_field):
            """Creates a row with bold label and input field."""
            row = QHBoxLayout()
            label_widget = QLabel(label, self)
            label_widget.setStyleSheet("font-weight: bold;")
            label_widget.setFixedWidth(250)  # Adjust label width
            row.addWidget(label_widget)
            row.addWidget(input_field)
            return row

        # Add rows to the layout
        main_layout.addLayout(create_input_row("Betreff für Angebot:", self.betreff_angebot_input))
        main_layout.addLayout(create_input_row("Nächste fortlaufende Nummer:", self.nummer_angebot_input))
        main_layout.addLayout(create_input_row("Betreff für Lieferschein:", self.betreff_lieferschein_input))
        main_layout.addLayout(create_input_row("Nächste fortlaufende Nummer:", self.nummer_lieferschein_input))
        main_layout.addLayout(create_input_row("Betreff für Rechnung:", self.betreff_rechnung_input))
        main_layout.addLayout(create_input_row("Nächste fortlaufende Nummer:", self.nummer_rechnung_input))

        # Save Button
        save_button = QPushButton("Einstellungen speichern", self)
        save_button.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 14px;                   

        """)
        save_button.clicked.connect(self.save_nummernvergabe)

        # Spacer for alignment
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(save_button, alignment=Qt.AlignCenter)



    def load_nummernvergabe(self):
        nummernvergabe = session.query(Nummernvergabe).first()
        if nummernvergabe:
            self.betreff_angebot_input.setText(nummernvergabe.betreff_angebot)
            self.nummer_angebot_input.setText(str(nummernvergabe.nummer_angebot))
            self.betreff_lieferschein_input.setText(nummernvergabe.betreff_lieferschein)
            self.nummer_lieferschein_input.setText(str(nummernvergabe.nummer_lieferschein))
            self.betreff_rechnung_input.setText(nummernvergabe.betreff_rechnung)
            self.nummer_rechnung_input.setText(str(nummernvergabe.nummer_rechnung))

    def save_nummernvergabe(self):
        try:
            # Get values from inputs
            betreff_angebot = self.betreff_angebot_input.text()
            nummer_angebot = int(self.nummer_angebot_input.text())
            betreff_lieferschein = self.betreff_lieferschein_input.text()
            nummer_lieferschein = int(self.nummer_lieferschein_input.text())
            betreff_rechnung = self.betreff_rechnung_input.text()
            nummer_rechnung = int(self.nummer_rechnung_input.text())

            # Check for an existing record
            nummernvergabe = session.query(Nummernvergabe).first()

            if nummernvergabe:
                nummernvergabe.betreff_angebot = betreff_angebot
                nummernvergabe.nummer_angebot = nummer_angebot
                nummernvergabe.betreff_lieferschein = betreff_lieferschein
                nummernvergabe.nummer_lieferschein = nummer_lieferschein
                nummernvergabe.betreff_rechnung = betreff_rechnung
                nummernvergabe.nummer_rechnung = nummer_rechnung
            else:
                nummernvergabe = Nummernvergabe(
                    betreff_angebot=betreff_angebot,
                    nummer_angebot=nummer_angebot,
                    betreff_lieferschein=betreff_lieferschein,
                    nummer_lieferschein=nummer_lieferschein,
                    betreff_rechnung=betreff_rechnung,
                    nummer_rechnung=nummer_rechnung
                )
                session.add(nummernvergabe)

            session.commit()
            QMessageBox.information(self, "Erfolg", "Einstellungen erfolgreich gespeichert!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Speichern: {e}")
