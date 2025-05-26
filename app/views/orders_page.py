from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTableWidgetItem
from app.models.app_models import Document, session


class OrdersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("OrdersPage")
        self.resize(1200, 700)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("mainLayout")

        # Header label
        self.documentsLabel = QtWidgets.QLabel("Bestellungen", self)
        self.documentsLabel.setObjectName("documentsLabel")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.documentsLabel.setFont(font)
        self.documentsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.documentsLabel)

        # Filters
        self.filtersLayout = QtWidgets.QHBoxLayout()
        self.filtersLayout.setSpacing(15)

        self.typFilterLayout = QtWidgets.QHBoxLayout()
        self.typLabel = QtWidgets.QLabel("Filter by Typ:")
        self.typFilter = QtWidgets.QComboBox(self)
        self.typFilter.setMinimumWidth(150)
        self.typFilter.addItem("All")
        self.typFilter.addItems(["Angebot", "Rechnung", "Lieferschein"])
        self.typFilter.currentTextChanged.connect(self.apply_filters)
        self.typLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.typFilterLayout.addWidget(self.typLabel)
        self.typFilterLayout.addWidget(self.typFilter)
        self.typFilterLayout.addStretch()

        self.statusFilterLayout = QtWidgets.QHBoxLayout()
        self.statusLabel = QtWidgets.QLabel("Filter by Status:")
        self.statusFilter = QtWidgets.QComboBox(self)
        self.statusFilter.setMinimumWidth(150)
        self.statusFilter.addItem("All")
        self.statusFilter.addItems(["True", "False"])
        self.statusFilter.currentTextChanged.connect(self.apply_filters)
        self.statusLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.statusFilterLayout.addWidget(self.statusLabel)
        self.statusFilterLayout.addWidget(self.statusFilter)
        self.statusFilterLayout.addStretch()

        self.filterContainerLayout = QtWidgets.QHBoxLayout()
        self.filterContainerLayout.addLayout(self.typFilterLayout)
        self.filterContainerLayout.addSpacing(10)
        self.filterContainerLayout.addLayout(self.statusFilterLayout)
        self.layout.addLayout(self.filterContainerLayout)

        # --- Search Container ---
        self.searchContainer = QtWidgets.QWidget(self)
        self.searchContainer.setFixedHeight(60)
        self.searchContainer.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)
        self.searchContainerLayout = QtWidgets.QHBoxLayout(self.searchContainer)
        self.searchContainerLayout.setContentsMargins(12, 6, 12, 6)
        self.searchContainerLayout.setSpacing(8)

        # Search icon
        searchIconLabel = QtWidgets.QLabel()
        searchIconLabel.setFixedSize(28, 28)
        searchIconLabel.setAlignment(QtCore.Qt.AlignCenter)
        iconPath = "resources/icons/search_blue.png"
        pixmap = QtGui.QPixmap(iconPath)

        if pixmap.isNull():
            import os
            absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), iconPath)
            pixmap = QtGui.QPixmap(absolute_path)

        if pixmap.isNull():
            searchIconLabel.setText("🔍")
            searchIconLabel.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 16px;
                    background: transparent;
                }
            """)
        else:
            scaledPixmap = QtGui.QPixmap(22, 22)
            scaledPixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(scaledPixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.drawPixmap(
                0, 0, 22, 22,
                pixmap.scaled(22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            painter.end()
            searchIconLabel.setPixmap(scaledPixmap)

        searchIconLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.searchContainerLayout.addWidget(searchIconLabel)
        self.searchContainerLayout.addSpacing(8)

        # Search Input
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Suche...")
        self.searchInput.textChanged.connect(self.apply_filters)
        self.searchInput.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                outline: none;
            }
        """)
        self.searchInput.setMinimumWidth(400)
        self.searchContainerLayout.addWidget(self.searchInput, 1)

        # Spacer between search and icons
        self.searchContainerLayout.addStretch()

        # --- Icon Buttons (Add, Edit, Delete) ---
        button_style = """
            QPushButton {
                border: none;
                background-color: transparent;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #cccccc;
                border-radius: 6px;
            }
        """

        self.addButton = QtWidgets.QPushButton()
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus_b.png'))
        self.addButton.setIconSize(QtCore.QSize(22, 22))
        self.addButton.setStyleSheet(button_style)

        self.editButton = QtWidgets.QPushButton()
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit_b.png'))
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setStyleSheet(button_style)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete_b.png'))
        self.deleteButton.setIconSize(QtCore.QSize(22, 22))
        self.deleteButton.setStyleSheet(button_style)

        self.searchContainerLayout.addWidget(self.addButton)
        self.searchContainerLayout.addWidget(self.editButton)
        self.searchContainerLayout.addWidget(self.deleteButton)

        self.layout.addWidget(self.searchContainer)

        # --- Table ---
        self.documentsTable = QtWidgets.QTableWidget(self)
        self.documentsTable.setColumnCount(14)
        self.documentsTable.setHorizontalHeaderLabels([
            "Status", "Datum", "Betreff", "Kundennummer", "Kunde", "Adresse", "PLZ",
            "Ort", "Leistungszeitraum", "Lieferadresse", "Projekt", "Netto Summe",
            "Brutto Summe", "Typ"
        ])
        self.documentsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.documentsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.documentsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.documentsTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.documentsTable)

        self.retranslateUi()
        self.load_documents()

        # Connect buttons
        self.addButton.clicked.connect(self.add_document)
        self.editButton.clicked.connect(self.edit_document)
        self.deleteButton.clicked.connect(self.delete_document)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("OrdersPage", "Orders Page"))

    def load_documents(self):
        self.documentsTable.setRowCount(0)
        documents = session.query(Document).all()
        for document in documents:
            row_position = self.documentsTable.rowCount()
            self.documentsTable.insertRow(row_position)
            self.documentsTable.setItem(row_position, 0, QTableWidgetItem(str(document.status)))
            self.documentsTable.setItem(row_position, 1, QTableWidgetItem(document.datum or ""))
            self.documentsTable.setItem(row_position, 2, QTableWidgetItem(document.betreff))
            self.documentsTable.setItem(row_position, 3, QTableWidgetItem(document.kundennummer))
            self.documentsTable.setItem(row_position, 4, QTableWidgetItem(document.kunde))
            self.documentsTable.setItem(row_position, 5, QTableWidgetItem(document.adresse))
            self.documentsTable.setItem(row_position, 6, QTableWidgetItem(document.plz))
            self.documentsTable.setItem(row_position, 7, QTableWidgetItem(document.ort))
            self.documentsTable.setItem(row_position, 8, QTableWidgetItem(document.leistungszeitraum))
            self.documentsTable.setItem(row_position, 9, QTableWidgetItem(document.lieferadresse or ""))
            self.documentsTable.setItem(row_position, 10, QTableWidgetItem(document.projekt or ""))
            self.documentsTable.setItem(row_position, 11, QTableWidgetItem(f"{document.summe_netto:.2f}"))
            self.documentsTable.setItem(row_position, 12, QTableWidgetItem(f"{document.summe_brutto:.2f}"))
            self.documentsTable.setItem(row_position, 13, QTableWidgetItem(document.doc_type))

    def filter_documents(self):
        filter_text = self.searchInput.text().lower()
        for row in range(self.documentsTable.rowCount()):
            match = any(
                filter_text in (self.documentsTable.item(row, col).text().lower() if self.documentsTable.item(row, col) else "")
                for col in range(self.documentsTable.columnCount())
            )
            self.documentsTable.setRowHidden(row, not match)

    def add_document(self):
        dialog = DocumentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_document = dialog.get_document_data()
            document = Document(**new_document)
            session.add(document)
            session.commit()
            self.load_documents()

    def edit_document(self):
        selected_row = self.documentsTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Bitte wählen Sie ein Dokument zum Bearbeiten aus.")
            return
        document_id = self.documentsTable.item(selected_row, 3).text()  # Kundennummer
        document = session.query(Document).filter_by(kundennummer=document_id).first()

        if not document:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Dokument nicht gefunden.")
            return

        dialog = DocumentDialog(self, document)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_document_data()
            for key, value in updated_data.items():
                setattr(document, key, value)
            session.commit()
            self.load_documents()

    def delete_document(self):
        selected_row = self.documentsTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Löschfehler", "Bitte wählen Sie ein Dokument zum Löschen aus.")
            return
        document_id = self.documentsTable.item(selected_row, 3).text()  # Kundennummer
        document = session.query(Document).filter_by(kundennummer=document_id).first()

        if not document:
            QMessageBox.warning(self, "Löschfehler", "Dokument nicht gefunden.")
            return

        reply = QMessageBox.question(self, 'Löschbestätigung',
                                     "Sind Sie sicher, dass Sie dieses Dokument löschen möchten?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            session.delete(document)
            session.commit()
            self.load_documents()
    def apply_filters(self):
        typ_filter = self.typFilter.currentText()
        status_filter = self.statusFilter.currentText()
        search_text = self.searchInput.text().lower()

        for row in range(self.documentsTable.rowCount()):
            # Fetch the row's Typ and Status values
            typ = self.documentsTable.item(row, 13).text() if self.documentsTable.item(row, 13) else ""
            status = self.documentsTable.item(row, 0).text() if self.documentsTable.item(row, 0) else ""

            # Check filters
            typ_matches = typ_filter == "All" or typ_filter == typ
            status_matches = status_filter == "All" or status_filter == status
            search_matches = any(
                search_text in (self.documentsTable.item(row, col).text().lower() if self.documentsTable.item(row, col) else "")
                for col in range(self.documentsTable.columnCount())
            )

            # Show or hide the row
            self.documentsTable.setRowHidden(row, not (typ_matches and status_matches and search_matches))

class DocumentDialog(QDialog):
    def __init__(self, parent=None, document=None):
        super().__init__(parent)
        self.document = document
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Bestellungen")
        self.setModal(True)
        layout = QFormLayout(self)
        # Style for labels
        label_style = "color: white; font-size: 14px;"

        # Fields
        self.idEdit = QLineEdit(self)
        self.statusEdit = QLineEdit(self)
        self.datumEdit = QLineEdit(self)
        self.betreffEdit = QLineEdit(self)
        self.kundennummerEdit = QLineEdit(self)
        self.kundeEdit = QLineEdit(self)
        self.adresseEdit = QLineEdit(self)
        self.plzEdit = QLineEdit(self)
        self.ortEdit = QLineEdit(self)
        self.leistungszeitraumEdit = QLineEdit(self)
        self.lieferadresseEdit = QLineEdit(self)
        self.projektEdit = QLineEdit(self)
        self.summeNettoEdit = QLineEdit(self)
        self.summeBruttoEdit = QLineEdit(self)
        self.summeKommentareEdit = QLineEdit(self)
        self.docTypeEdit = QLineEdit(self)

        fields = [
            ("ID", self.idEdit),
            ("Status", self.statusEdit),
            ("Datum", self.datumEdit),
            ("Betreff", self.betreffEdit),
            ("Kundennummer", self.kundennummerEdit),
            ("Kunde", self.kundeEdit),
            ("Adresse", self.adresseEdit),
            ("PLZ", self.plzEdit),
            ("Ort", self.ortEdit),
            ("Leistungszeitraum", self.leistungszeitraumEdit),
            ("Lieferadresse", self.lieferadresseEdit),
            ("Projekt", self.projektEdit),
            ("Netto Summe", self.summeNettoEdit),
            ("Brutto Summe", self.summeBruttoEdit),
            ("Kommentare", self.summeKommentareEdit),
            ("Typ", self.docTypeEdit),
        ]

        for label_text, field in fields:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(label_style)
            layout.addRow(label, field)

        self.saveButton = QPushButton("Speichern", self)
        self.cancelButton = QPushButton("Stornieren", self)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow(button_layout)

        # Populate fields if editing
        if self.document:
            self.idEdit.setText(str(self.document.id) if self.document.id else "")
            self.statusEdit.setText(str(self.document.status))
            self.datumEdit.setText(self.document.datum or "")
            self.betreffEdit.setText(self.document.betreff)
            self.kundennummerEdit.setText(self.document.kundennummer)
            self.kundeEdit.setText(self.document.kunde)
            self.adresseEdit.setText(self.document.adresse)
            self.plzEdit.setText(self.document.plz)
            self.ortEdit.setText(self.document.ort)
            self.leistungszeitraumEdit.setText(self.document.leistungszeitraum)
            self.lieferadresseEdit.setText(self.document.lieferadresse or "")
            self.projektEdit.setText(self.document.projekt or "")
            self.summeNettoEdit.setText(str(self.document.summe_netto))
            self.summeBruttoEdit.setText(str(self.document.summe_brutto))
            self.summeKommentareEdit.setText(self.document.summe_kommentare or "")
            self.docTypeEdit.setText(self.document.doc_type)

        # Connect buttons
        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def get_document_data(self):
        # Convert the status value correctly - if it's "True" or "False", convert to boolean
        status_text = self.statusEdit.text()
        if status_text.lower() == "true":
            status_value = True
        elif status_text.lower() == "false":
            status_value = False
        else:
            # Try to convert to float if it's not a boolean string
            try:
                status_value = float(status_text)
            except ValueError:
                # Default to False if conversion fails
                status_value = False

        return {
            "id": int(self.idEdit.text()) if self.idEdit.text() else None,
            "status": status_value,
            "datum": self.datumEdit.text(),
            "betreff": self.betreffEdit.text(),
            "kundennummer": self.kundennummerEdit.text(),
            "kunde": self.kundeEdit.text(),
            "adresse": self.adresseEdit.text(),
            "plz": self.plzEdit.text(),
            "ort": self.ortEdit.text(),
            "leistungszeitraum": self.leistungszeitraumEdit.text(),
            "lieferadresse": self.lieferadresseEdit.text(),
            "projekt": self.projektEdit.text(),
            "summe_netto": float(self.summeNettoEdit.text()) if self.summeNettoEdit.text() else 0.0,
            "summe_brutto": float(self.summeBruttoEdit.text()) if self.summeBruttoEdit.text() else 0.0,
            "summe_kommentare": self.summeKommentareEdit.text() if hasattr(self, 'summeKommentareEdit') else "",
            "doc_type": self.docTypeEdit.text()
        }



