from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from app.models.app_models import Customer, session

class CustomersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("CustomersPage")
        self.resize(1000, 600)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("mainLayout")
        # Add customersLabel at the top of the page
        self.customersLabel = QtWidgets.QLabel("Kundenliste", self)
        # Add productsLabel at the top of the page
        self.customersLabel.setObjectName("customersLabel")

        # Set the font size and style
        font = QtGui.QFont()
        font.setPointSize(20)  # Set font size (increase as per requirement)
        self.customersLabel.setFont(font)

        # Center align the label
        self.customersLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Add the label to the layout
        self.layout.addWidget(self.customersLabel)


        
        # --- Styled search container ---
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

        # Load icon
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

        # Styled search input
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Suche...")
        self.searchInput.textChanged.connect(self.filter_customers)
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

        # Add searchContainer to your layout
        self.layout.addWidget(self.searchContainer)


        # Table for customers
        self.customersTable = QtWidgets.QTableWidget(self)
        self.customersTable.setColumnCount(10)
        self.customersTable.setHorizontalHeaderLabels(
            ["Status", "Nummer", "Kunde", "Adresse", "PLZ", "Ort", "Telefon", "Mobil", "eMail", "Kommentar"]
        )
        self.customersTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.customersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.customersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.customersTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.customersTable)

        # Icon-only buttons (inside searchContainer)

        # Spacer between search input and icons
        self.searchContainerLayout.addStretch()

        iconBtnStyle = """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
                border-radius: 8px;
            }
        """

        # Add (plus) button
        self.addButton = QtWidgets.QPushButton()
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus_b.png'))
        self.addButton.setIconSize(QtCore.QSize(22, 22))
        self.addButton.setToolTip("Kunden hinzufügen")
        self.addButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.addButton)

        # Edit (pencil) button
        self.editButton = QtWidgets.QPushButton()
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit_b.png'))
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setToolTip("Kunden bearbeiten")
        self.editButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.editButton)

        # Delete (trash) button
        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete_b.png'))
        self.deleteButton.setIconSize(QtCore.QSize(22, 22))
        self.deleteButton.setToolTip("Kunden löschen")
        self.deleteButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.deleteButton)

        self.retranslateUi()
        self.load_customers()

        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_customer)
        self.editButton.clicked.connect(self.edit_customer)
        self.deleteButton.clicked.connect(self.delete_customer)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("CustomersPage", "Customers Page"))

    def load_customers(self):
        self.customersTable.setRowCount(0)
        customers = session.query(Customer).all()  # Use the session to query
        for customer in customers:
            row_position = self.customersTable.rowCount()
            self.customersTable.insertRow(row_position)
            self.customersTable.setItem(row_position, 0, QTableWidgetItem(customer.status or ""))
            self.customersTable.setItem(row_position, 1, QTableWidgetItem(customer.nummer))
            self.customersTable.setItem(row_position, 2, QTableWidgetItem(customer.kunde))
            self.customersTable.setItem(row_position, 3, QTableWidgetItem(customer.adresse))
            self.customersTable.setItem(row_position, 4, QTableWidgetItem(customer.plz))
            self.customersTable.setItem(row_position, 5, QTableWidgetItem(customer.ort))
            self.customersTable.setItem(row_position, 6, QTableWidgetItem(customer.telefon))
            self.customersTable.setItem(row_position, 7, QTableWidgetItem(customer.mobil or ""))
            self.customersTable.setItem(row_position, 8, QTableWidgetItem(customer.email))
            self.customersTable.setItem(row_position, 9, QTableWidgetItem(customer.kommentar or ""))

    def filter_customers(self):
        filter_text = self.searchInput.text().lower()
        for row in range(self.customersTable.rowCount()):
            item = self.customersTable.item(row, 2)  # Assuming "Kunde" (Name) is in the 3rd column
            self.customersTable.setRowHidden(row, filter_text not in item.text().lower())

    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_customer = dialog.get_customer_data()
            # Save to database
            customer = Customer(**new_customer)
            session.add(customer)
            session.commit()
            self.load_customers()

    def edit_customer(self):
        selected_row = self.customersTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Bitte wählen Sie einen Kunden zur Bearbeitung aus.")
            return
        customer_id = self.customersTable.item(selected_row, 1).text()  # Assuming "Nummer" (Number) is in the 2nd column
        customer = session.query(Customer).filter_by(nummer=customer_id).first()  # Fetch customer from database

        if not customer:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Kunde nicht gefunden.")
            return
        
        dialog = CustomerDialog(self, customer)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_customer_data()
            # Update the customer in the database
            for key, value in updated_data.items():
                setattr(customer, key, value)
            session.commit()
            self.load_customers()

    def delete_customer(self):
        selected_row = self.customersTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Löschfehler", "Bitte wählen Sie einen Kunden zum Löschen aus.")
            return
        customer_id = self.customersTable.item(selected_row, 1).text()  # Assuming "Nummer" (Number) is in the 2nd column
        customer = session.query(Customer).filter_by(nummer=customer_id).first()  # Fetch customer from database

        if not customer:
            QMessageBox.warning(self, "Löschfehler", "Kunde nicht gefunden.")
            return

        reply = QMessageBox.question(self, 'Löschbestätigung',
                                     "Sind Sie sicher, dass Sie diesen Kunden löschen möchten?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            session.delete(customer)
            session.commit()
            self.load_customers()

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.customer = customer
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Kundendetails")
        self.setModal(True)
        layout = QFormLayout(self)

        # Style for labels
        label_style = "color: white; font-size: 14px;"

        # Fields
        self.numberEdit = QLineEdit(self)
        self.nameEdit = QLineEdit(self)
        self.addressEdit = QLineEdit(self)
        self.zipCodeEdit = QLineEdit(self)
        self.cityEdit = QLineEdit(self)
        self.phoneEdit = QLineEdit(self)
        self.mobileEdit = QLineEdit(self)
        self.emailEdit = QLineEdit(self)
        self.commentEdit = QLineEdit(self)

        fields = [
            ("Number", self.numberEdit),
            ("Name", self.nameEdit),
            ("Address", self.addressEdit),
            ("ZIP Code", self.zipCodeEdit),
            ("City", self.cityEdit),
            ("Phone", self.phoneEdit),
            ("Mobile", self.mobileEdit),
            ("Email", self.emailEdit),
            ("Comment", self.commentEdit),
        ]

        for label_text, field in fields:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(label_style)
            layout.addRow(label, field)

        # Buttons
        self.saveButton = QPushButton("Speichern", self)
        self.cancelButton = QPushButton("Stornieren", self)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow(button_layout)

        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        if self.customer:
            self.load_customer_data()

    def load_customer_data(self):
        self.numberEdit.setText(self.customer.nummer)
        self.nameEdit.setText(self.customer.kunde)
        self.addressEdit.setText(self.customer.adresse)
        self.zipCodeEdit.setText(self.customer.plz)
        self.cityEdit.setText(self.customer.ort)
        self.phoneEdit.setText(self.customer.telefon)
        self.mobileEdit.setText(self.customer.mobil or "")
        self.emailEdit.setText(self.customer.email)
        self.commentEdit.setText(self.customer.kommentar or "")

    def get_customer_data(self):
        return {
            'nummer': self.numberEdit.text(),
            'kunde': self.nameEdit.text(),
            'adresse': self.addressEdit.text(),
            'plz': self.zipCodeEdit.text(),
            'ort': self.cityEdit.text(),
            'telefon': self.phoneEdit.text(),
            'mobil': self.mobileEdit.text() or None,
            'email': self.emailEdit.text(),
            'kommentar': self.commentEdit.text() or None,
        }
