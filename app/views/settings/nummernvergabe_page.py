from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QFrame, QStackedWidget, QLineEdit, QFileDialog, QGraphicsOpacityEffect, QMessageBox,QSpacerItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
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


        # Top Layout for Back Button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("border: none; background-color: transparent;")
        back_button.clicked.connect(self.parent.go_back_to_settings_page)

        top_layout.addWidget(back_button)
        main_layout.addLayout(top_layout)

        # Header
        header_label = QLabel("Nummernvergabe Settings", self)
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

        def create_row(label1, input1, label2, input2):
            row = QHBoxLayout()
            row.addWidget(QLabel(label1, self))
            row.addWidget(input1)
            row.addWidget(QLabel(label2, self))
            row.addWidget(input2)
            return row

        # Add rows to the layout
        main_layout.addLayout(create_row("Betreff Fur Angebot:", self.betreff_angebot_input, "Nachste fortlaufende Nummer:", self.nummer_angebot_input))
        main_layout.addLayout(create_row("Betreff Fur Lieferschein:", self.betreff_lieferschein_input, "Nachste fortlaufende Nummer:", self.nummer_lieferschein_input))
        main_layout.addLayout(create_row("Betreff Fur Rechnung:", self.betreff_rechnung_input, "Nachste fortlaufende Nummer:", self.nummer_rechnung_input))

        # Save button
        save_button = QPushButton("Save Settings", self)
        save_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px;")
        save_button.clicked.connect(self.save_nummernvergabe)
        main_layout.addWidget(save_button)

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
        QMessageBox.information(self, "Success", "Settings saved successfully!")
