from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtWidgets
from ui.ui_create_bill_page import Ui_CreateBillPage
from fpdf import FPDF
from PIL import Image
from io import BytesIO
from shutil import copyfile
import pyodbc
from app.models.app_models import CompanyDetails, session

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
        
        # Clear the current selection list
        self.current_selection = []
        
        for row in selected_rows:
            row_data = []
            for column in range(self.create_bill_page_ui.productTable.columnCount()):
                item = self.create_bill_page_ui.productTable.item(row.row(), column)
                if item:
                    row_data.append(item.text())
            
            if row_data:
                # Append the row data as a tuple (CodeNr, Name, SalesPrice, ...)
                self.current_selection.append(tuple(row_data))
        
        # Debug: print the current selection
        print("Current selection:", self.current_selection)
        
        # If there's a selection, move values to the input fields
        if self.current_selection:
            selected_product = self.current_selection[0]  # Get the first selected product
            name = selected_product[1]  # Assuming 'Name' is in the second column
            sales_price = selected_product[2]  # Assuming 'SalesPrice' is in the third column
            
            # Update the 'Name' input field
            self.create_bill_page_ui.orderNameInput.setText(name)  # 'nameInput' from the UI
            
            # Update the 'Preis Netto' input field
            self.create_bill_page_ui.preisNettoInput.setText(sales_price)  # 'priesNettoInput' from the UI


    def update_pdf_viewer(self):
        # Add the currently selected products to the main list
        for product in self.current_selection:
            # Get the values from the input fields (not from the selected table row)
            name_input_value = self.create_bill_page_ui.orderNameInput.text()  # 'Name' from input
            sales_price_input_value = self.create_bill_page_ui.preisNettoInput.text()  # 'Preis Netto' from input
            menge_value = self.create_bill_page_ui.mengeInput.text() if self.create_bill_page_ui.mengeInput.text() else ''  # Get Menge value
            
            if menge_value:  # If Menge has a value
                product_with_menge = (product[0], menge_value, name_input_value, sales_price_input_value)  # Use edited inputs
            else:
                product_with_menge = (product[0], '', name_input_value, sales_price_input_value)  # Use edited inputs

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
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        # Fetch company details from the database
        company_details = session.query(CompanyDetails).first()

        if company_details:
            # Add company logo if available
            if company_details.logo_image:
                logo_image = Image.open(BytesIO(company_details.logo_image))
                logo_image_path = 'temp_logo.png'
                logo_image.save(logo_image_path)
                pdf.image(logo_image_path, x=10, y=10, w=30)

            # Place Firmenname beside the logo
            pdf.set_xy(50, 10)  # Adjust the positioning as necessary
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, company_details.firmenname, ln=True, align='L')

            # Align the remaining company details to the right side of the PDF
            pdf.set_xy(140, 10)  # Set starting point for address details
            pdf.set_font('Arial', '', 12)

            # Reduced space between address lines
            line_height = 6  # Adjust this value for less/more space between lines
            pdf.cell(0, line_height, f'{company_details.adresse}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.plz} {company_details.ort}', ln=True, align='R')
            pdf.cell(0, line_height, company_details.land, ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.telefon}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.email}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.steuernummer}', ln=True, align='R')

            # Draw a horizontal line below the address info
            pdf.set_xy(10, pdf.get_y() + 2)  # Move cursor to the line position (adjust as necessary)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Coordinates of the line (200 is the page width)

            pdf.ln(8)  # Add small space after the horizontal line

        # Add recipient info
        pdf.cell(0, 10, f'Name: {name}', 0, 1)
        pdf.cell(0, 10, f'Age: {age}', 0, 1)
        pdf.cell(0, 10, f'Email: {email}', 0, 1)

        pdf.ln(8)  # Adjust this space as needed

        # Address section (center)
        pdf.cell(0, 10, f'Address: {address}', 0, 1)
        pdf.cell(0, 10, f'Phone Number: {phone_number}', 0, 1)

        pdf.ln(8)  # Adjust this space as needed

        # Order section (right side)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Order:', 0, 1)

        # Table headers with background color
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'CodeNr', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'Menge', 1, 0, 'C', 1)
        pdf.cell(60, 10, 'Name', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'SalesPrice', 1, 1, 'C', 1)

        # Reset font for table rows
        pdf.set_font('Arial', '', 12)
        pdf.set_fill_color(240, 240, 240)

        # Adding the selected products to the PDF table
        for product in selected_products:
            pdf.cell(40, 10, product[0], 1, 0, 'C', 1)
            pdf.cell(40, 10, product[1], 1, 0, 'C', 1)
            pdf.cell(60, 10, product[2], 1, 0, 'C', 1)
            pdf.cell(40, 10, product[3], 1, 1, 'C', 1)

        pdf.output(pdf_path)


    def export_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.create_bill_page, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            copyfile(self.pdf_path, file_path)
            QMessageBox.information(self.create_bill_page, "Export Successful", f"PDF exported successfully to {file_path}")
