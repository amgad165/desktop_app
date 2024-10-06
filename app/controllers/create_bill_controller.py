from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtWidgets
from ui.ui_create_bill_page import Ui_CreateBillPage
from fpdf import FPDF
from PIL import Image
from io import BytesIO
from shutil import copyfile
import pyodbc
from app.models.app_models import CompanyDetails, session, Product, Customer, engine  # Ensure Customer is imported
from sqlalchemy.orm import sessionmaker

class CreateBillController:
    def __init__(self, stacked_widget):
        self.stacked_widget = stacked_widget
        self.create_bill_page = QWidget()
        self.create_bill_page_ui = Ui_CreateBillPage()
        self.create_bill_page_ui.setupUi(self.create_bill_page)

        self.selected_products = []
        self.current_selection = []
        self.current_customer_selection = []  # For Kunde

        self.kunde_dict = {}
        self.allgemein_dict = {}

        self.connections_setup = False  # Flag to ensure connections are only set up once
        self.setup_connections()
        self.load_products()
        self.load_customers()  # Load customer data
        self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.allgemeinPage)

    def setup_page(self, page_type):
        """Customizes the Create Bill page based on the page type passed."""
        if page_type == "Angebot":
            self.create_bill_page_ui.betreffInput.setText("Angebot")
            
        elif page_type == "Rechnung":
            pass
        elif page_type == "Lieferschein":
            pass
        else:
            pass

        print(f"Page set up as {page_type}")

    def setup_connections(self):
        if self.connections_setup:
            return

        self.connections_setup = True  # Set the flag to True after setting up connections

        # Connect buttons
        self.create_bill_page_ui.addEntityButton.clicked.connect(self.update_pdf_artikel)
        self.create_bill_page_ui.exportButton.clicked.connect(self.export_pdf)

        # Allgemein page connections
        self.create_bill_page_ui.allgemeinButton.clicked.connect(lambda: self.show_inputs("allgemein"))
        self.create_bill_page_ui.addAllgemeinButton.clicked.connect(self.update_pdf_allgemein)

        # Kunde page connections
        self.create_bill_page_ui.kundeButton.clicked.connect(lambda: self.show_inputs("kunde"))
        self.create_bill_page_ui.addKundeEntityButton.clicked.connect(self.update_pdf_kunde)
        self.create_bill_page_ui.customerTable.itemClicked.connect(self.on_customer_table_item_clicked)  # Connect table item clicked

        # Artikel page connections
        self.create_bill_page_ui.artikelButton.clicked.connect(lambda: self.show_inputs("artikel"))
        self.create_bill_page_ui.artikelSearchInput.textChanged.connect(self.filter_products)
        self.create_bill_page_ui.productTable.itemSelectionChanged.connect(self.update_selected_products)
        self.create_bill_page_ui.removeLastRowButton.clicked.connect(self.handle_remove_last_row)

        print("Connections have been set up.")

    def show_inputs(self, section):
        if section == "allgemein":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.allgemeinPage)
        elif section == "kunde":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.kundePage)
        elif section == "artikel":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.artikelPage)

    def load_products(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            products = session.query(Product.nummer, Product.produkt, Product.verkaufspreis).all()

            session.close()

            product_list = [(product.nummer, product.produkt, product.verkaufspreis) for product in products]

            self.products = product_list
            self.display_products(product_list)

        except Exception as e:
            QMessageBox.critical(self.create_bill_page, "Database Error", f"Could not load products: {e}")

    def load_customers(self):
        try:
            # Create a session to interact with the database
            Session = sessionmaker(bind=engine)
            session = Session()

            # Query the customers table
            customers = session.query(Customer.nummer, Customer.kunde, Customer.adresse, Customer.plz, Customer.ort, Customer.telefon).all()

            # Close the session
            session.close()

            # Convert the result into a list of tuples
            customer_list = [(customer.nummer, customer.kunde, customer.adresse, customer.plz, customer.ort, customer.telefon) for customer in customers]

            # Display the customers in the UI
            self.display_customers(customer_list)

        except Exception as e:
            # Handle any database errors
            QMessageBox.critical(self.create_bill_page, "Database Error", f"Could not load customers: {e}")


    def display_products(self, products):
        self.create_bill_page_ui.productTable.setRowCount(0)
        for product in products:
            row_position = self.create_bill_page_ui.productTable.rowCount()
            self.create_bill_page_ui.productTable.insertRow(row_position)
            for col, data in enumerate(product):
                self.create_bill_page_ui.productTable.setItem(row_position, col, QTableWidgetItem(str(data)))

    def display_customers(self, customers):
        self.create_bill_page_ui.customerTable.setRowCount(0)
        for customer in customers:
            row_position = self.create_bill_page_ui.customerTable.rowCount()
            self.create_bill_page_ui.customerTable.insertRow(row_position)
            for col, data in enumerate(customer):
                self.create_bill_page_ui.customerTable.setItem(row_position, col, QTableWidgetItem(str(data)))


    def filter_products(self):
        filter_text = self.create_bill_page_ui.artikelSearchInput.text().lower()
        for row in range(self.create_bill_page_ui.productTable.rowCount()):
            item = self.create_bill_page_ui.productTable.item(row, 1)
            if filter_text in item.text().lower():
                self.create_bill_page_ui.productTable.setRowHidden(row, False)
            else:
                self.create_bill_page_ui.productTable.setRowHidden(row, True)

    def filter_customers(self):
        filter_text = self.create_bill_page_ui.kundeSearchInput.text().lower()
        for row in range(self.create_bill_page_ui.customerTable.rowCount()):
            item = self.create_bill_page_ui.customerTable.item(row, 1)  # Assuming 'kunde' is the second column
            if filter_text in item.text().lower():
                self.create_bill_page_ui.customerTable.setRowHidden(row, False)
            else:
                self.create_bill_page_ui.customerTable.setRowHidden(row, True)

    def on_customer_table_item_clicked(self, item):
        row = item.row()
        
        # Helper function to safely get text from table items
        def get_item_text(row, column):
            table_item = self.create_bill_page_ui.customerTable.item(row, column)
            return table_item.text() if table_item is not None else ""

        # Get values from the customer table
        kunden_nr = get_item_text(row, 0)  # Kundennummer column
        kunde = get_item_text(row, 1)  # Kunde column
        adresse = get_item_text(row, 2)  # Adresse column
        plz = get_item_text(row, 3)  # PLZ column
        ort = get_item_text(row, 4)  # Ort column
        telefon = get_item_text(row, 5)  # Ort column

        # Update the input fields
        self.create_bill_page_ui.Kunden_Nr.setText(kunden_nr)
        self.create_bill_page_ui.kundeInput.setText(kunde)
        self.create_bill_page_ui.adresseInput.setText(adresse)
        self.create_bill_page_ui.plzInput.setText(plz)
        self.create_bill_page_ui.ortInput.setText(ort)
        self.create_bill_page_ui.telefonInput.setText(telefon)


    def update_selected_products(self):
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

        if self.current_selection:
            selected_product = self.current_selection[0]
            name = selected_product[1]
            sales_price = selected_product[2]

            self.create_bill_page_ui.artikelNameInput.setText(name)
            self.create_bill_page_ui.preisNettoInput.setText(sales_price)





    def update_pdf_artikel(self):
        for product in self.current_selection:
            name_input_value = self.create_bill_page_ui.artikelNameInput.text()
            sales_price_input_value = self.create_bill_page_ui.preisNettoInput.text()
            menge_value = self.create_bill_page_ui.mengeInput.text() if self.create_bill_page_ui.mengeInput.text() else ''

            if menge_value:
                product_with_menge = (product[0], menge_value, name_input_value, sales_price_input_value)
            else:
                product_with_menge = (product[0], '', name_input_value, sales_price_input_value)

            if product_with_menge not in self.selected_products:
                self.selected_products.append(product_with_menge)

        # name = self.create_bill_page_ui.nameInput.text()
        # age = self.create_bill_page_ui.ageInput.text()
        # email = self.create_bill_page_ui.emailInput.text()


        self.pdf_path = 'bill.pdf'

        self.generate_pdf(self.pdf_path, self.allgemein_dict, self.kunde_dict, self.selected_products)
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)


    def update_pdf_kunde(self):


        # name = self.create_bill_page_ui.nameInput.text()
        # age = self.create_bill_page_ui.ageInput.text()
        # email = self.create_bill_page_ui.emailInput.text()

        self.kunde_dict ={'kunde':self.create_bill_page_ui.kundeInput.text(),'adresse':self.create_bill_page_ui.adresseInput.text(),
                     'plz':self.create_bill_page_ui.plzInput.text(),'ort':self.create_bill_page_ui.ortInput.text(),
                     'land':self.create_bill_page_ui.landSelect.currentText(),
                     'kunden_nr':self.create_bill_page_ui.Kunden_Nr.text(),
                     'telefon':self.create_bill_page_ui.telefonInput.text(),
                     'uid_nr':self.create_bill_page_ui.uidNrInput.text(),
                     }
        self.pdf_path = 'bill.pdf'

        self.generate_pdf(self.pdf_path, self.allgemein_dict, self.kunde_dict, self.selected_products)
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)

    def update_pdf_allgemein(self):



        self.allgemein_dict ={'betreff':self.create_bill_page_ui.betreffInput.text(),'date':self.create_bill_page_ui.datumInput.text(),
                     'bearbeiter':self.create_bill_page_ui.bearbeiterSelect.currentText()
                     }
        self.pdf_path = 'bill.pdf'

        self.generate_pdf(self.pdf_path, self.allgemein_dict, self.kunde_dict, self.selected_products)
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)


    def handle_remove_last_row(self):
        if self.selected_products:
            self.selected_products.pop()
            self.current_selection = []
            self.update_pdf_artikel()
        else:
            QMessageBox.warning(self.create_bill_page, 'Remove Error', 'No rows to remove from PDF.')

    def generate_pdf(self, pdf_path, allgemein_dict, kunde_dict, selected_products): 
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
            if company_details.logo_image:
                logo_image = Image.open(BytesIO(company_details.logo_image))
                logo_image_path = 'temp_logo.png'
                logo_image.save(logo_image_path)
                pdf.image(logo_image_path, x=10, y=10, w=30)

            pdf.set_xy(50, 10)
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, company_details.firmenname, ln=True, align='L')

            pdf.set_xy(140, 10)
            pdf.set_font('Arial', '', 12)

            line_height = 6
            pdf.cell(0, line_height, f'{company_details.adresse}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.plz} {company_details.ort}', ln=True, align='R')
            pdf.cell(0, line_height, company_details.land, ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.telefon}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.email}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.steuernummer}', ln=True, align='R')

            pdf.set_xy(10, pdf.get_y() + 2)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())

            pdf.ln(8)

        if kunde_dict:
            
            # Display Kunde info on the left
            pdf.set_xy(10, pdf.get_y())  # Start from the left
            pdf.cell(0, 6, f'{kunde_dict.get("kunde")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("adresse")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("plz")} {kunde_dict.get("ort")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("land")}', 0, 1)

            # Display KundenInfo (aligned to the right with background color)
            kunden_info_x = 120  # Position on the right side
            kunden_info_y = pdf.get_y() - 30  # Align with the top of Kunde info

            pdf.set_xy(kunden_info_x, kunden_info_y)
            pdf.set_fill_color(200, 220, 255)  # Background color for the container
            pdf.cell(80, 30, '', 0, 1, 'R', 1)  # Container with background color

            # Position title inside the container with larger font and bold
            pdf.set_xy(kunden_info_x + 5, kunden_info_y + 2)  # Add padding inside the container
            pdf.set_font('Arial', 'B', 14)  # Bold and larger font for the title
            pdf.cell(0, 6, 'Kundeninfo', 0, 1, 'L')

            # Reset font to normal size and not bold for the rest of the data
            pdf.set_font('Arial', '', 12)  # Regular font for the following lines

            # Define the label width to align values
            label_width = 35  # Adjust this based on your needs
            value_x_offset = kunden_info_x + 5 + label_width

            # Kunden-Nr
            pdf.set_xy(kunden_info_x + 5, kunden_info_y + 10)
            pdf.cell(label_width, 6, 'Kunden-Nr:', 0, 0, 'L')  # Print label with fixed width
            pdf.set_xy(value_x_offset, kunden_info_y + 10)
            pdf.cell(0, 6, kunde_dict.get("kunden_nr"), 0, 1, 'L')  # Print value aligned

            # Telefon
            pdf.set_xy(kunden_info_x + 5, kunden_info_y + 16)
            pdf.cell(label_width, 6, 'Telefon:', 0, 0, 'L')  # Print label with fixed width
            pdf.set_xy(value_x_offset, kunden_info_y + 16)
            pdf.cell(0, 6, kunde_dict.get("telefon"), 0, 1, 'L')  # Print value aligned

            # UID-Nr
            pdf.set_xy(kunden_info_x + 5, kunden_info_y + 22)
            pdf.cell(label_width, 6, 'UID-Nr:', 0, 0, 'L')  # Print label with fixed width
            pdf.set_xy(value_x_offset, kunden_info_y + 22)
            pdf.cell(0, 6, kunde_dict.get("uid_nr"), 0, 1, 'L')  # Print value aligned


            pdf.ln(20)
        else:

            # Define a constant height for the Kunde info section
            KUNDE_INFO_HEIGHT = 40  # Adjust this value as needed

            # Add the same height of space if kunde_dict is not provided
            pdf.ln(KUNDE_INFO_HEIGHT)


        if allgemein_dict:
            # Display Betreff info on the left
            pdf.set_xy(10, pdf.get_y())  # Start from the left
            pdf.set_font('Arial', 'B', 14)  # Bold and larger font for the title
            pdf.cell(0, 6, f'{allgemein_dict.get("betreff")}', 0, 1)
            pdf.set_font('Arial', '', 12)  # Regular font for the following lines

            # Display Date and Bearbeiter info on the right with labels
            right_x = 150  # Position on the right side
            current_y = pdf.get_y() - 6  # Adjust y position to align with Betreff

            pdf.set_xy(right_x, current_y)
            pdf.cell(0, 6, 'Date:', 0, 1, 'L')
            pdf.set_xy(right_x + 20, current_y)
            pdf.cell(0, 6, f'{allgemein_dict.get("date")}', 0, 1, 'L')

            pdf.set_xy(right_x, current_y + 6)
            pdf.cell(0, 6, 'Bearbeiter:', 0, 1, 'L')
            pdf.set_xy(right_x + 20, current_y + 6)
            pdf.cell(0, 6, f'  {allgemein_dict.get("bearbeiter")}', 0, 1, 'L')
            

        # Rest of the order details (this remains the same as your original code)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Order:', 0, 1)

        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, 'CodeNr', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'Menge', 1, 0, 'C', 1)
        pdf.cell(60, 10, 'Name', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'SalesPrice', 1, 1, 'C', 1)

        pdf.set_font('Arial', '', 12)
        pdf.set_fill_color(240, 240, 240)

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
