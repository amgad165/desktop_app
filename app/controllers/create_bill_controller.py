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

        self.setup_connections()
        self.load_products()
        self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.infoPage)
    
    def setup_connections(self):
        self.create_bill_page_ui.submitButton.clicked.connect(self.update_pdf_viewer)
        self.create_bill_page_ui.exportButton.clicked.connect(self.export_pdf)
        self.create_bill_page_ui.infoButton.clicked.connect(lambda: self.show_inputs("info"))
        self.create_bill_page_ui.addressButton.clicked.connect(lambda: self.show_inputs("address"))
        self.create_bill_page_ui.orderButton.clicked.connect(lambda: self.show_inputs("order"))
        self.create_bill_page_ui.orderSearchInput.textChanged.connect(self.filter_products)
        self.create_bill_page_ui.productTable.itemSelectionChanged.connect(self.update_selected_products)

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
        search_term = self.create_bill_page_ui.orderSearchInput.text().lower()
        filtered_products = [product for product in self.products if search_term in product[1].lower()]
        self.display_products(filtered_products)

    def display_products(self, products):
        self.create_bill_page_ui.productTable.setRowCount(0)
        for product in products:
            row_position = self.create_bill_page_ui.productTable.rowCount()
            self.create_bill_page_ui.productTable.insertRow(row_position)
            for col, data in enumerate(product):
                self.create_bill_page_ui.productTable.setItem(row_position, col, QTableWidgetItem(str(data)))

    def update_selected_products(self):
        selected_rows = self.create_bill_page_ui.productTable.selectionModel().selectedRows()
        selected_data = []

        for row in selected_rows:
            row_data = []
            for column in range(self.create_bill_page_ui.productTable.columnCount()):
                item = self.create_bill_page_ui.productTable.item(row.row(), column)
                if item:
                    row_data.append(item.text())
            if row_data:
                selected_data.append(tuple(row_data))

        self.selected_products = selected_data
        print("Selected products:", self.selected_products)

    def update_pdf_viewer(self):
        name = self.create_bill_page_ui.nameInput.text()
        age = self.create_bill_page_ui.ageInput.text()
        email = self.create_bill_page_ui.emailInput.text()
        address = self.create_bill_page_ui.addressInput.text()
        phone_number = self.create_bill_page_ui.phoneNumberInput.text()

        self.pdf_path = 'bill.pdf'

        # Generate the PDF
        self.generate_pdf(self.pdf_path, name, age, email, address, phone_number, self.selected_products)

        # Load the created PDF into the PDF viewer
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)
    
    def export_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.create_bill_page, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            copyfile(self.pdf_path, file_path)
            QMessageBox.information(self.create_bill_page, "Export Successful", f"PDF exported successfully to {file_path}")

    def generate_pdf(self, pdf_path):
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Bill Information', 0, 1, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        
        # Info section
        pdf.set_x(10)  # Left alignment
        pdf.cell(0, 10, f'Name: {self.data["info"]["Name"]}', 0, 1)
        pdf.cell(0, 10, f'Age: {self.data["info"]["Age"]}', 0, 1)
        pdf.cell(0, 10, f'Email: {self.data["info"]["Email"]}', 0, 1)
        
        # Address section
        pdf.set_x(pdf.w / 2 - 30)  # Center alignment
        pdf.cell(0, 10, f'Address: {self.data["address"]["Address"]}', 0, 1)
        pdf.cell(0, 10, f'Phone Number: {self.data["address"]["Phone Number"]}', 0, 1)
        
        # Order section
        pdf.set_x(pdf.w - 70)  # Right alignment
        pdf.cell(0, 10, f'Order Date: {self.data["order"]["Order Date"]}', 0, 1)

        pdf.output(pdf_path)
