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

        # Search bar
        self.searchInput = QtWidgets.QLineEdit(self)
        self.searchInput.setPlaceholderText("Search Customers")
        self.searchInput.textChanged.connect(self.filter_customers)
        self.layout.addWidget(self.searchInput)

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

        # Buttons for add, edit, and delete
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add", self)
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.editButton = QtWidgets.QPushButton("Edit", self)
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit.png'))
        self.deleteButton = QtWidgets.QPushButton("Delete", self)
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete.png'))
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.layout.addLayout(self.buttonsLayout)

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
            QMessageBox.warning(self, "Edit Error", "Please select a customer to edit.")
            return
        customer_id = self.customersTable.item(selected_row, 1).text()  # Assuming "Nummer" (Number) is in the 2nd column
        customer = session.query(Customer).filter_by(nummer=customer_id).first()  # Fetch customer from database

        if not customer:
            QMessageBox.warning(self, "Edit Error", "Customer not found.")
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
            QMessageBox.warning(self, "Delete Error", "Please select a customer to delete.")
            return
        customer_id = self.customersTable.item(selected_row, 1).text()  # Assuming "Nummer" (Number) is in the 2nd column
        customer = session.query(Customer).filter_by(nummer=customer_id).first()  # Fetch customer from database

        if not customer:
            QMessageBox.warning(self, "Delete Error", "Customer not found.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this customer?",
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
        self.setWindowTitle("Customer Details")
        self.setModal(True)
        layout = QFormLayout(self)

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

        for label, field in fields:
            layout.addRow(label, field)

        self.saveButton = QPushButton("Save", self)
        self.cancelButton = QPushButton("Cancel", self)
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
