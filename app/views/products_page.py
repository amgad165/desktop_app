from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from app.models.app_models import Product, session


class ProductsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ProductsPage")
        self.resize(1000, 600)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("mainLayout")

        # Add productsLabel at the top of the page
        self.productsLabel = QtWidgets.QLabel("Products", self)
        self.productsLabel.setObjectName("productsLabel")

        # Set the font size and style
        font = QtGui.QFont()
        font.setPointSize(20)  # Set font size (increase as per requirement)
        self.productsLabel.setFont(font)

        # Center align the label
        self.productsLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Add the label to the layout
        self.layout.addWidget(self.productsLabel)

        # Search bar
        self.searchInput = QtWidgets.QLineEdit(self)
        self.searchInput.setPlaceholderText("Search Products")
        self.searchInput.textChanged.connect(self.filter_products)
        self.layout.addWidget(self.searchInput)

        # Table for products
        self.productsTable = QtWidgets.QTableWidget(self)
        self.productsTable.setColumnCount(6)
        self.productsTable.setHorizontalHeaderLabels(
            ["Gruppe", "Nummer", "Produkt", "Beschreibung", "Verkaufspreis", "Bild"]
        )
        self.productsTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.productsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.productsTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productsTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.productsTable)

        # Buttons for add, edit, and delete
        self.buttonsLayout = QtWidgets.QHBoxLayout()

        # Add button with right-aligned icon and larger text
        self.addButton = QPushButton("Add", self)
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addButton.setIconSize(QtCore.QSize(17, 17))  # Set the size of the icon
        self.addButton.setLayoutDirection(QtCore.Qt.RightToLeft)  # Icon on the right
        self.addButton.setStyleSheet("font-size: 16px;")  # Set larger font size

        # Edit button with right-aligned icon and larger text
        self.editButton = QPushButton("Edit ", self)
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit.png'))
        self.editButton.setIconSize(QtCore.QSize(16, 16))  # Set the size of the icon
        self.editButton.setLayoutDirection(QtCore.Qt.RightToLeft)  # Icon on the right
        self.editButton.setStyleSheet("font-size: 16px;")  # Set larger font size

        # Delete button with right-aligned icon and larger text
        self.deleteButton = QPushButton("Delete ", self)
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete.png'))
        self.deleteButton.setIconSize(QtCore.QSize(17, 17))  # Set the size of the icon
        self.deleteButton.setLayoutDirection(QtCore.Qt.RightToLeft)  # Icon on the right
        self.deleteButton.setStyleSheet("font-size: 16px;")  # Set larger font size

        # Add buttons to layout
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.layout.addLayout(self.buttonsLayout)

        self.retranslateUi()
        self.load_products()

        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_product)
        self.editButton.clicked.connect(self.edit_product)
        self.deleteButton.clicked.connect(self.delete_product)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ProductsPage", "Products Page"))

    def load_products(self):
        self.productsTable.setRowCount(0)
        products = session.query(Product).all()
        for product in products:
            row_position = self.productsTable.rowCount()
            self.productsTable.insertRow(row_position)
            self.productsTable.setItem(row_position, 0, QTableWidgetItem(product.gruppe or ""))
            self.productsTable.setItem(row_position, 1, QTableWidgetItem(product.nummer))
            self.productsTable.setItem(row_position, 2, QTableWidgetItem(product.produkt))
            self.productsTable.setItem(row_position, 3, QTableWidgetItem(product.beschreibung or ""))
            self.productsTable.setItem(row_position, 4, QTableWidgetItem(f"{product.verkaufspreis:.2f}"))

            if product.bild:
                self.productsTable.setItem(row_position, 5, QTableWidgetItem("Image Available"))
            else:
                self.productsTable.setItem(row_position, 5, QTableWidgetItem("No Image"))

    def filter_products(self):
        filter_text = self.searchInput.text().lower()
        for row in range(self.productsTable.rowCount()):
            item = self.productsTable.item(row, 2)  # Assuming "Produkt" is in the 3rd column
            self.productsTable.setRowHidden(row, filter_text not in item.text().lower())

    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_product = dialog.get_product_data()
            product = Product(**new_product)
            session.add(product)
            session.commit()
            self.load_products()

    def edit_product(self):
        selected_row = self.productsTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Edit Error", "Please select a product to edit.")
            return
        product_id = self.productsTable.item(selected_row, 1).text()
        product = session.query(Product).filter_by(nummer=product_id).first()

        if not product:
            QMessageBox.warning(self, "Edit Error", "Product not found.")
            return

        dialog = ProductDialog(self, product)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_product_data()
            for key, value in updated_data.items():
                setattr(product, key, value)
            session.commit()
            self.load_products()

    def delete_product(self):
        selected_row = self.productsTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Delete Error", "Please select a product to delete.")
            return
        product_id = self.productsTable.item(selected_row, 1).text()
        product = session.query(Product).filter_by(nummer=product_id).first()

        if not product:
            QMessageBox.warning(self, "Delete Error", "Product not found.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this product?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            session.delete(product)
            session.commit()
            self.load_products()


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Product Details")
        self.setModal(True)
        layout = QFormLayout(self)

        # Fields
        self.gruppeEdit = QLineEdit(self)
        self.nummerEdit = QLineEdit(self)
        self.produktEdit = QLineEdit(self)
        self.beschreibungEdit = QLineEdit(self)
        self.verkaufspreisEdit = QLineEdit(self)

        fields = [
            ("Gruppe", self.gruppeEdit),
            ("Nummer", self.nummerEdit),
            ("Produkt", self.produktEdit),
            ("Beschreibung", self.beschreibungEdit),
            ("Verkaufspreis", self.verkaufspreisEdit),
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

        if self.product:
            self.load_product_data()

    def load_product_data(self):
        self.gruppeEdit.setText(self.product.gruppe or "")
        self.nummerEdit.setText(self.product.nummer)
        self.produktEdit.setText(self.product.produkt)
        self.beschreibungEdit.setText(self.product.beschreibung or "")
        self.verkaufspreisEdit.setText(f"{self.product.verkaufspreis:.2f}")

    def get_product_data(self):
        return {
            'gruppe': self.gruppeEdit.text(),
            'nummer': self.nummerEdit.text(),
            'produkt': self.produktEdit.text(),
            'beschreibung': self.beschreibungEdit.text(),
            'verkaufspreis': float(self.verkaufspreisEdit.text()),
        }
