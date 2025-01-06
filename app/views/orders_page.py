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
        self.documentsLabel = QtWidgets.QLabel("Documents", self)
        self.documentsLabel.setObjectName("documentsLabel")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.documentsLabel.setFont(font)
        self.documentsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.documentsLabel)

        # Filters layout
        self.filtersLayout = QtWidgets.QHBoxLayout()

        # Typ filter
        self.typFilter = QtWidgets.QComboBox(self)
        self.typFilter.addItem("All")  # Default option to show all types
        self.typFilter.addItems(["Angebot", "Rechnung", "Lieferschein"])
        self.typFilter.currentTextChanged.connect(self.apply_filters)
        self.filtersLayout.addWidget(QtWidgets.QLabel("Filter by Typ:"))
        self.filtersLayout.addWidget(self.typFilter)

        # Status filter
        self.statusFilter = QtWidgets.QComboBox(self)
        self.statusFilter.addItem("All")  # Default option to show all statuses
        self.statusFilter.addItems(["Active", "Inactive"])  # Adjust based on your status options
        self.statusFilter.currentTextChanged.connect(self.apply_filters)
        self.filtersLayout.addWidget(QtWidgets.QLabel("Filter by Status:"))
        self.filtersLayout.addWidget(self.statusFilter)

        self.layout.addLayout(self.filtersLayout)

        # Search bar
        self.searchInput = QtWidgets.QLineEdit(self)
        self.searchInput.setPlaceholderText("Search Documents")
        self.searchInput.textChanged.connect(self.apply_filters)
        self.layout.addWidget(self.searchInput)

        # Table for documents
        self.documentsTable = QtWidgets.QTableWidget(self)
        self.documentsTable.setColumnCount(14)  # Adjusted for all columns
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

        # Buttons for add, edit, delete
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.addButton = QPushButton("Add", self)
        self.editButton = QPushButton("Edit", self)
        self.deleteButton = QPushButton("Delete", self)
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.layout.addLayout(self.buttonsLayout)

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
            QMessageBox.warning(self, "Edit Error", "Please select a document to edit.")
            return
        document_id = self.documentsTable.item(selected_row, 3).text()  # Kundennummer
        document = session.query(Document).filter_by(kundennummer=document_id).first()

        if not document:
            QMessageBox.warning(self, "Edit Error", "Document not found.")
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
            QMessageBox.warning(self, "Delete Error", "Please select a document to delete.")
            return
        document_id = self.documentsTable.item(selected_row, 3).text()  # Kundennummer
        document = session.query(Document).filter_by(kundennummer=document_id).first()

        if not document:
            QMessageBox.warning(self, "Delete Error", "Document not found.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this document?",
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
        self.setWindowTitle("Document Details")
        self.setModal(True)
        layout = QFormLayout(self)

        # Fields
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
        self.docTypeEdit = QLineEdit(self)

        fields = [
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
            ("Typ", self.docTypeEdit),
        ]

        for label, field in fields:
            layout.addRow(label, field)

        self.saveButton = QPushButton("Save", self)
        self.cancelButton = QPushButton("Cancel", self)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow(button_layout)

        # Populate fields if editing
        if self.document:
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
            self.docTypeEdit.setText(self.document.doc_type)

        # Connect buttons
        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def get_document_data(self):
        return {
            "status": float(self.statusEdit.text()),
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
            "summe_netto": float(self.summeNettoEdit.text()),
            "summe_brutto": float(self.summeBruttoEdit.text()),
            "doc_type": self.docTypeEdit.text(),
        }



