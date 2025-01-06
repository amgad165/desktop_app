from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget,
    QTableWidgetItem, QPushButton, QCheckBox, QSpinBox, QWidget
)
from difflib import get_close_matches

class BatchProductDialog(QDialog):
    def __init__(self, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Products by Batch")
        self.setGeometry(100, 100, 1100, 800)

        # Layouts
        main_layout = QHBoxLayout(self)

        # Left - Text Area with "Generate Suggestions" button
        left_layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Paste products here...")
        left_layout.addWidget(self.text_area)

        self.generate_button = QPushButton("Generate Suggestions")
        self.generate_button.clicked.connect(self.on_generate_suggestions)
        left_layout.addWidget(self.generate_button)

        main_layout.addLayout(left_layout)

        # Right - Table
        right_layout = QVBoxLayout()
        self.product_table = QTableWidget(0, 5)
        self.product_table.setHorizontalHeaderLabels(["Select", "Product Name", "Menge","CodeNr","SalesPrice"])
        right_layout.addWidget(self.product_table)

        self.add_all_button = QPushButton("Add All")
        self.cancel_button = QPushButton("Cancel")
        right_layout.addWidget(self.add_all_button)
        right_layout.addWidget(self.cancel_button)

        main_layout.addLayout(right_layout)

        # Connections
        self.add_all_button.clicked.connect(self.add_all_products)
        self.cancel_button.clicked.connect(self.reject)

        # Store the products for suggestions
        self.products = products

    def on_generate_suggestions(self):
        """Handle the 'Generate Suggestions' button click."""
        pasted_text = self.text_area.toPlainText()
        suggestions = self.generate_suggestions(pasted_text)
        self.populate_table(suggestions)

    def populate_table(self, product_suggestions):
        self.product_table.setRowCount(0)  # Clear previous data
        for product, quantity, codeNr, salePrice in product_suggestions:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)

            # Add checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(True)  # Set checkbox to be checked by default
            self.product_table.setCellWidget(row_position, 0, checkbox)

            # Add product name
            self.product_table.setItem(row_position, 1, QTableWidgetItem(product))


            # Quantity input
            spin_box = QSpinBox()
            spin_box.setValue(quantity)


            self.product_table.setCellWidget(row_position, 2, spin_box)


            self.product_table.setItem(row_position, 3, QTableWidgetItem(str(codeNr)))
            self.product_table.setItem(row_position, 4, QTableWidgetItem(str(salePrice)))


    def add_all_products(self):
        selected_products = []
        for row in range(self.product_table.rowCount()):
            checkbox = self.product_table.cellWidget(row, 0)
            if checkbox.isChecked():
                product_name = self.product_table.item(row, 1).text()
                quantity_widget = self.product_table.cellWidget(row, 2)
                quantity = quantity_widget.value()

                codeNr = self.product_table.item(row, 3).text()
                salePrice = self.product_table.item(row, 4).text()
                selected_products.append((codeNr,str(quantity), product_name, salePrice))
        self.accept()  # Close dialog and return
        return selected_products
    
    def generate_suggestions(self, pasted_text):
        suggestions = []
        lines = [line.strip() for line in pasted_text.strip().split("\n") if line.strip()]  # Exclude empty lines

        for line in lines:
            # Split product name and optional quantity
            parts = line.rsplit(" ", 1)

            if len(parts) == 2 and parts[1].isdigit():  # Check if the last part is a number
                product_name = parts[0].strip()
                quantity = int(parts[1])
            else:
                product_name = line  # Assume entire line is the product name
                quantity = 1  # Default quantity

            # Stage 1: Match similar products
            exact_match = None
            for product in self.products:
                if product_name.lower() in product[1].lower():
                    exact_match = (product[1], quantity, product[0] , str(product[2]))
                    break

            if exact_match:
                suggestions.append(exact_match)
            else:
                # Stage 2: Find the most similar product
                # codeNr = [product[0] for product in self.products]
                product_names = [product[1] for product in self.products]
                closest_match = get_close_matches(product_name, product_names, n=1, cutoff=0.6)  # Adjust cutoff for sensitivity
                if closest_match:

                    product = next((p for p in self.products if p[1] == closest_match[0]), None)
                    if product:
                        product_with_menge = (product[1], quantity, product[0], str(product[2]))
                    else:
                        # Handle case where product isn't found in the model
                        product_with_menge = (product_name, quantity, 'Unknown', 'Unknown')

                    suggestions.append(product_with_menge)
                else:
                    suggestions.append((product_name, quantity, 'Unknown', 'Unknown'))  # Use the raw input as a fallback

        return suggestions
