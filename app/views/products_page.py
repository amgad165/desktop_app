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
        self.productsLabel = QtWidgets.QLabel("Produkte", self)
        self.productsLabel.setObjectName("productsLabel")

        # Set the font size and style
        font = QtGui.QFont()
        font.setPointSize(20)
        self.productsLabel.setFont(font)
        self.productsLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Add the label to the layout
        self.layout.addWidget(self.productsLabel)

        # --- Styled search container for products ---
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

        # Styled search input
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Suche...")
        self.searchInput.textChanged.connect(self.filter_products)
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

        # Spacer
        self.searchContainerLayout.addStretch()

        # Icon button style
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

        # Add Button
        self.addButton = QtWidgets.QPushButton()
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus_b.png'))
        self.addButton.setIconSize(QtCore.QSize(22, 22))
        self.addButton.setToolTip("Produkt hinzufügen")
        self.addButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.addButton)

        # Edit Button
        self.editButton = QtWidgets.QPushButton()
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit_b.png'))
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setToolTip("Produkt bearbeiten")
        self.editButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.editButton)

        # Delete Button
        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete_b.png'))
        self.deleteButton.setIconSize(QtCore.QSize(22, 22))
        self.deleteButton.setToolTip("Produkt löschen")
        self.deleteButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.deleteButton)

        # Add search container to layout
        self.layout.addWidget(self.searchContainer)

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
            QMessageBox.warning(self, "Bearbeitungsfehler", "Bitte wählen Sie ein Produkt zum Bearbeiten aus.")
            return
        product_id = self.productsTable.item(selected_row, 1).text()
        product = session.query(Product).filter_by(nummer=product_id).first()

        if not product:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Produkt nicht gefunden.")
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
            QMessageBox.warning(self, "Löschfehler", "Bitte wählen Sie ein Produkt zum Löschen aus.")
            return
        product_id = self.productsTable.item(selected_row, 1).text()
        product = session.query(Product).filter_by(nummer=product_id).first()

        if not product:
            QMessageBox.warning(self, "Löschfehler", "Produkt nicht gefunden.")
            return

        reply = QMessageBox.question(self, 'Löschbestätigung',
                                     "Sind Sie sicher, dass Sie dieses Produkt löschen möchten?",
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
        self.setWindowTitle("Produkte")
        self.setModal(True)
        layout = QFormLayout(self)
        # Style for labels
        label_style = "color: white; font-size: 14px;"

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
