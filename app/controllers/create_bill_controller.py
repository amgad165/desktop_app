from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtWidgets
from ui.ui_create_bill_page import Ui_CreateBillPage
from fpdf import FPDF
from shutil import copyfile
import pyodbc

class CreateBillController:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget
        self.create_bill_page = QWidget()
        self.create_bill_page_ui = Ui_CreateBillPage()
        self.create_bill_page_ui.setupUi(self.create_bill_page)
        
        self.selected_products = []
        self.current_selection = []

        self.connections_setup = False  # Flag to ensure connections are only set up once
        self.setup_connections()
        self.load_products()
        self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.infoPage)
    
    def setup_connections(self):
        if self.connections_setup:
            return  # Avoid setting up connections more than once

        self.connections_setup = True  # Set the flag to True after setting up connections

        # Connect buttons
        self.create_bill_page_ui.addEntityButton.clicked.connect(self.update_pdf_viewer)  # Add Entity button
        self.create_bill_page_ui.exportButton.clicked.connect(self.export_pdf)
        
        # Info page connections
        self.create_bill_page_ui.infoButton.clicked.connect(lambda: self.show_inputs("info"))
        self.create_bill_page_ui.addInfoButton.clicked.connect(self.update_pdf_viewer)  # Add Info button
        
        # Address page connections
        self.create_bill_page_ui.addressButton.clicked.connect(lambda: self.show_inputs("address"))
        self.create_bill_page_ui.addAddressDataButton.clicked.connect(self.update_pdf_viewer)  # Add Address Data button
        
        # Order page connections
        self.create_bill_page_ui.orderButton.clicked.connect(lambda: self.show_inputs("order"))
        self.create_bill_page_ui.orderSearchInput.textChanged.connect(self.filter_products)
        self.create_bill_page_ui.productTable.itemSelectionChanged.connect(self.update_selected_products)
        self.create_bill_page_ui.removeLastRowButton.clicked.connect(self.handle_remove_last_row)

        # Print debug statements
        print("Connections have been set up.")

    def show_inputs(self, section):
        if section == "info":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.infoPage)
        elif section == "address":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.addressPage)
        elif section == "order":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.orderPage)
    
    def load_products(self):
        try:
            conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=resources/data/data.accdb;')
            cursor = conn.cursor()
            cursor.execute("SELECT CodeNr, Name, SalesPrice FROM Product")
            products = cursor.fetchall()
            conn.close()
            
            self.products = products
            self.display_products(products)
        except Exception as e:
            QMessageBox.critical(self.create_bill_page, "Database Error", f"Could not load products: {e}")

    def filter_products(self):
        filter_text = self.create_bill_page_ui.orderSearchInput.text().lower()
        for row in range(self.create_bill_page_ui.productTable.rowCount()):
            item = self.create_bill_page_ui.productTable.item(row, 1)
            if filter_text in item.text().lower():
                self.create_bill_page_ui.productTable.setRowHidden(row, False)
            else:
                self.create_bill_page_ui.productTable.setRowHidden(row, True)
                
    def display_products(self, products):
        self.create_bill_page_ui.productTable.setRowCount(0)
        for product in products:
            row_position = self.create_bill_page_ui.productTable.rowCount()
            self.create_bill_page_ui.productTable.insertRow(row_position)
            for col, data in enumerate(product):
                self.create_bill_page_ui.productTable.setItem(row_position, col, QTableWidgetItem(str(data)))

    def update_selected_products(self):
        print("update_selected_products called")
        selected_rows = self.create_bill_page_ui.productTable.selectionModel().selectedRows()
        self.current_selection = []
        for row in selected_rows:
            row_data = []
            for column in range(self.create_bill_page_ui.productTable.columnCount()):
                item = self.create_bill_page_ui.productTable.item(row.row(), column)
                if item:
                    row_data.append(item.text())
            if row_data:
                self.current_selection.append(tuple(row_data))

        print("Current selection:", self.current_selection)

    def update_pdf_viewer(self):
        # Add the currently selected products to the main list
        for product in self.current_selection:
            menge_value = self.create_bill_page_ui.mengeInput.text() if self.create_bill_page_ui.mengeInput.text() else ''  # Get Menge value
            if menge_value:  # If Menge has a value
                product_with_menge = (product[0], menge_value, product[1], product[2])  # Arrange columns as (CodeNr, Menge, Name, SalesPrice)
            else:
                product_with_menge = (product[0], '', product[1], product[2])  # Arrange columns as (CodeNr, Menge, Name, SalesPrice)

            if product_with_menge not in self.selected_products:
                self.selected_products.append(product_with_menge)

        # Collect input data for Info
        name = self.create_bill_page_ui.nameInput.text()
        age = self.create_bill_page_ui.ageInput.text()
        email = self.create_bill_page_ui.emailInput.text()

        # Collect input data for Address
        address = self.create_bill_page_ui.addressInput.text()
        phone_number = self.create_bill_page_ui.phoneNumberInput.text()

        # Path to save the PDF
        self.pdf_path = 'bill.pdf'

        # Generate the PDF with updated selected products
        self.generate_pdf(self.pdf_path, name, age, email, address, phone_number, self.selected_products)

        # Load the created PDF into the PDF viewer
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)

    def handle_remove_last_row(self):
        print('handle_remove_last_row called')
        if self.selected_products:
            self.selected_products.pop()  # Remove last product from selected list
            self.current_selection = []
            self.update_pdf_viewer()  # Regenerate PDF with updated list
            print('Row removed. Remaining products:', self.selected_products)
        else:
            QMessageBox.warning(self.create_bill_page, 'Remove Error', 'No rows to remove from PDF.')

    def generate_pdf(self, pdf_path, name, age, email, address, phone_number, selected_products):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Bill Information', 0, 1, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        # Info section (left side)
        pdf.cell(0, 10, f'Name: {name}', 0, 1)
        pdf.cell(0, 10, f'Age: {age}', 0, 1)
        pdf.cell(0, 10, f'Email: {email}', 0, 1)
        
        pdf.ln(10)  # Add some space

        # Address section (center)
        pdf.cell(0, 10, f'Address: {address}', 0, 1)
        pdf.cell(0, 10, f'Phone Number: {phone_number}', 0, 1)

        pdf.ln(10)  # Add some space

        # Order section (right side)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Order:', 0, 1)

        # Table headers with background color
        pdf.set_fill_color(200, 220, 255)  # Light blue background
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'CodeNr', 1, 0, 'C', 1)  # CodeNr column
        pdf.cell(40, 10, 'Menge', 1, 0, 'C', 1)  # Menge column
        pdf.cell(60, 10, 'Name', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'SalesPrice', 1, 1, 'C', 1)

        # Reset font for table rows
        pdf.set_font('Arial', '', 12)
        pdf.set_fill_color(240, 240, 240)  # Light gray background for rows

        # Adding the selected products to the PDF table
        for product in selected_products:
            pdf.cell(40, 10, product[0], 1, 0, 'C', 1)  # CodeNr
            pdf.cell(40, 10, product[1], 1, 0, 'C', 1)  # Menge
            pdf.cell(60, 10, product[2], 1, 0, 'C', 1)  # Name
            pdf.cell(40, 10, product[3], 1, 1, 'C', 1)  # SalesPrice

        pdf.output(pdf_path)

    def export_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.create_bill_page, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            copyfile(self.pdf_path, file_path)
            QMessageBox.information(self.create_bill_page, "Export Successful", f"PDF exported successfully to {file_path}")
