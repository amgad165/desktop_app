from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtWidgets
from ui.ui_create_bill_page import Ui_CreateBillPage
from app.views.batch_product_dialog import BatchProductDialog  # Import the dialog

from fpdf import FPDF
from PIL import Image
from io import BytesIO
from shutil import copyfile
from app.models.app_models import Bankverbindung, CompanyDetails, Nummernvergabe, session, Product, Customer,Document, billSettings,engine  # Ensure Customer is imported
from sqlalchemy.orm import sessionmaker
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPagedPaintDevice
from PyQt5.QtCore import QUrl
import subprocess
import os
import platform
from datetime import datetime
from urllib.parse import quote

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

    def reset_page(self):
        """Resets all fields, selections, and data on the Create Bill page."""
        # Clear all text inputs
        self.create_bill_page_ui.betreffInput.clear()
        self.create_bill_page_ui.datumInput.clear()
        self.create_bill_page_ui.leistungszeitraumInput.clear()
        self.create_bill_page_ui.referenzInput.clear()
        self.create_bill_page_ui.summeNettoInput.clear()
        # self.create_bill_page_ui.summeBruttoInput.clear()
        self.create_bill_page_ui.kundeInput.clear()
        self.create_bill_page_ui.lieferadresseInput.clear()
        self.create_bill_page_ui.plzInput.clear()
        self.create_bill_page_ui.ortInput.clear()

        # Reset dropdowns and radio buttons
        self.create_bill_page_ui.bearbeiterSelect.setCurrentIndex(0)
        self.create_bill_page_ui.anredeSelect.setCurrentIndex(0)
        self.create_bill_page_ui.landSelect.setCurrentIndex(0)
        self.create_bill_page_ui.nettoRadioButton.setChecked(False)
        self.create_bill_page_ui.bruttoRadioButton.setChecked(False)

        # Clear customer and product table selections
        self.create_bill_page_ui.customerTable.clearSelection()
        self.create_bill_page_ui.productTable.clearSelection()

        # Reset internal state
        self.selected_products = []
        self.current_selection = []
        self.current_customer_selection = []
        self.kunde_dict = {}
        self.allgemein_dict = {}

        # Reset inputsStackedWidget to the default page (e.g., allgemeinPage)
        self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.allgemeinPage)

        print("Page reset successfully.")


    def reset_pdf_viewer(self):
        """
        Resets the PDF viewer by clearing the loaded PDF.
        """
        self.pdf_path = None  # Clear the stored path
        self.create_bill_page_ui.pdfViewer.load_pdf(None)  # Unload the current PDF
        print("PDF Viewer has been reset.")


    def setup_page(self, page_type):

        self.reset_page()
        self.reset_pdf_viewer()
        self.page_type = page_type  # Store page_type as an instance variable


        nummernvergabe = session.query(Nummernvergabe).first()

        """Customizes the Create Bill page based on the page type passed."""
        if page_type == "Angebot":
            if nummernvergabe:
                if nummernvergabe.betreff_angebot:
                    self.create_bill_page_ui.betreffInput.setText(nummernvergabe.betreff_angebot)
                else:
                    self.create_bill_page_ui.betreffInput.setText("Angebot")
            
        elif page_type == "Rechnung":
            if nummernvergabe:
                if nummernvergabe.betreff_rechnung:
                    self.create_bill_page_ui.betreffInput.setText(nummernvergabe.betreff_rechnung)
                else:
                    self.create_bill_page_ui.betreffInput.setText("Rechnung")

        elif page_type == "Lieferschein":
            if nummernvergabe:
                if nummernvergabe.betreff_lieferschein:
                    self.create_bill_page_ui.betreffInput.setText(nummernvergabe.betreff_lieferschein)
                else:
                    self.create_bill_page_ui.betreffInput.setText("Lieferschein")

        else:
            pass

        print(f"Page set up as {page_type}")

    def setup_connections(self):
        if self.connections_setup:
            return

        self.connections_setup = True  # Set the flag to True after setting up connections

        # Highlight allgemeinButton by default
        self.highlight_button(self.create_bill_page_ui.allgemeinButton)

        # Connect action buttons
        self.create_bill_page_ui.addEntityButton.clicked.connect(self.update_pdf_artikel)
        self.create_bill_page_ui.exportButton.clicked.connect(self.export_pdf)
        self.create_bill_page_ui.saveOrderButton.clicked.connect(self.save_to_order)
        self.create_bill_page_ui.printButton.clicked.connect(self.print_pdf)

        # Connect section buttons
        self.create_bill_page_ui.allgemeinButton.clicked.connect(
            lambda: self.show_inputs("allgemein", self.create_bill_page_ui.allgemeinButton))
        self.create_bill_page_ui.kundeButton.clicked.connect(
            lambda: self.show_inputs("kunde", self.create_bill_page_ui.kundeButton))
        self.create_bill_page_ui.artikelButton.clicked.connect(
            lambda: self.show_inputs("artikel", self.create_bill_page_ui.artikelButton))

        # Connect page-specific buttons
        self.create_bill_page_ui.addAllgemeinButton.clicked.connect(self.update_pdf_allgemein)
        self.create_bill_page_ui.addKundeEntityButton.clicked.connect(self.update_pdf_kunde)
        self.create_bill_page_ui.removeKundeLastRowButton.clicked.connect(self.clear_kunde_inputs)

        # Connect table functionality
        self.create_bill_page_ui.artikelSearchInput.textChanged.connect(self.filter_products)
        self.create_bill_page_ui.kundeSearchInput.textChanged.connect(self.filter_customers)
        self.create_bill_page_ui.productTable.itemSelectionChanged.connect(self.update_selected_products)
        self.create_bill_page_ui.customerTable.itemClicked.connect(self.on_customer_table_item_clicked)
        
        # Connect batch and row buttons
        self.create_bill_page_ui.removeLastRowButton.clicked.connect(self.handle_remove_last_row)
        self.create_bill_page_ui.batchButton.clicked.connect(self.handle_add_batch)

        print("Connections have been set up.")

    def show_inputs(self, section, clicked_button):
        if section == "allgemein":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.allgemeinPage)
        elif section == "kunde":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.kundePage)
        elif section == "artikel":
            self.create_bill_page_ui.inputsStackedWidget.setCurrentWidget(self.create_bill_page_ui.artikelPage)



        # Highlight the clicked button
        self.highlight_button(clicked_button)

    def highlight_button(self, clicked_button):
        # Reset styles for all buttons
        default_style = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px 10px;
            }
        """
        highlighted_style = """
            QPushButton {
                background-color: #6887b6;
                color: black;
                border: 1px solid #0056b3;
                padding: 5px 10px;
            }
        """
        # Reset styles
        self.create_bill_page_ui.allgemeinButton.setStyleSheet(default_style)
        self.create_bill_page_ui.kundeButton.setStyleSheet(default_style)
        self.create_bill_page_ui.artikelButton.setStyleSheet(default_style)

        # Apply the highlighted style to the clicked button
        clicked_button.setStyleSheet(highlighted_style)


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


        # Calculate the total price
        settings = session.query(billSettings).first()
        mwst = settings.VAT if settings else None  # Get VAT if it exists, else None
        
        payment_type = settings.prices_is if settings else None

        total_price = 0.0
        for product in self.selected_products:
            try:
                menge = float(product[1])  # Second index (quantity)
                price = float(product[3])  # Last index (price)
                subtotal = menge * price  # Calculate subtotal (quantity * price)

                if payment_type == "Netto":
                    # Add VAT only for Netto
                    if mwst is not None:
                        subtotal *= (1 + mwst / 100)  # Add VAT to the subtotal
                elif payment_type == "Brutto":
                    # No need to add VAT for Brutto; it's already included in the price
                    pass

                total_price += subtotal  # Add to the total price
            except ValueError:
                # Handle cases where quantity or price is invalid
                print(f"Invalid value for product: {product}")
                continue

        
        

        # Update the summeNettoInput field
        self.create_bill_page_ui.summeNettoInput.setText(f"{total_price:.2f}")
        self.pdf_path = 'bill.pdf'

        self.generate_pdf(self.pdf_path, self.allgemein_dict, self.kunde_dict, self.selected_products)
        self.create_bill_page_ui.pdfViewer.load_pdf(self.pdf_path)

    def clear_kunde_inputs(self):
        self.create_bill_page_ui.kundeInput.clear()
        self.create_bill_page_ui.adresseInput.clear()
        self.create_bill_page_ui.plzInput.clear()
        self.create_bill_page_ui.ortInput.clear()
        self.create_bill_page_ui.telefonInput.clear()
        self.create_bill_page_ui.Kunden_Nr.clear()
        self.create_bill_page_ui.uidNrInput.clear()

        # Clear the selected customer
        self.current_customer_selection = []
        self.kunde_dict = None
        self.update_pdf_kunde(cleared=True)

    def update_pdf_kunde(self,cleared=False):

        if cleared:
            self.kunde_dict = None
        else:
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
                     'bearbeiter':self.create_bill_page_ui.bearbeiterSelect.currentText(),'referenz':self.create_bill_page_ui.referenzInput.text(),
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


    def handle_add_batch(self):
        # Open the batch product dialog
        dialog = BatchProductDialog(self.products, self.create_bill_page)
        if dialog.exec_():
            # Fetch selected products
            product_with_menge = dialog.add_all_products()

            [self.selected_products.append(product) for product in product_with_menge if product not in self.selected_products]

            # Update the PDF
            self.update_pdf_artikel()

    def generate_pdf(self, pdf_path, allgemein_dict, kunde_dict, selected_products): 
        class PDF(FPDF):
            def footer(self):
                self.set_y(-35)  # Move footer higher
                self.set_line_width(0.5)
                self.line(10, self.get_y(), 200, self.get_y())  # Horizontal line

                self.ln(5)  # Space after the line
                self.set_font('Arial', 'B', 14)
                self.cell(0, 5, 'Bankverbindung', 0, 1, 'C')  # Centered title

                bank_details = session.query(Bankverbindung).first()
                if bank_details:
                    self.ln(3)  # Space between title and details
                    self.set_font('Arial', '', 12)
                    self.cell(0, 5, f"Institut: {bank_details.institut}, Referenz: {allgemein_dict.get("referenz")} ,Inhaber: {bank_details.inhaber}", 0, 1, 'C')
                    self.cell(0, 5, f"IBAN: {bank_details.iban}, BIC: {bank_details.bic}", 0, 1, 'C')

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
            # pdf.cell(0, line_height, company_details.land, ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.telefon}', ln=True, align='R')
            pdf.cell(0, line_height, f'{company_details.email}', ln=True, align='R')
            # pdf.cell(0, line_height, f'{company_details.steuernummer}', ln=True, align='R')

            pdf.set_xy(10, pdf.get_y() + 2)
            pdf.set_line_width(0.5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())

            pdf.ln(8)

        if kunde_dict:
            
            # Display Kunde info on the left
            pdf.set_xy(10, pdf.get_y())  # Start from the left
            pdf.set_font('Arial', 'B', 14)  # Bold and larger font for the title
            pdf.cell(0, 6, 'Lieferadresse:', 0, 1, 'L')

            pdf.ln(2)  # Add a space between the title and the content

            pdf.set_font('Arial', '', 12)  # Regular font for the following lines
            pdf.cell(0, 6, f'{kunde_dict.get("kunde")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("adresse")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("plz")} {kunde_dict.get("ort")}', 0, 1)
            pdf.cell(0, 6, f'{kunde_dict.get("land")}', 0, 1)

            # Display KundenInfo (aligned to the right with background color)
            kunden_info_x = 134  # Position on the right side
            kunden_info_y = pdf.get_y() - 34  # Align with the top of Kunde info

            pdf.set_xy(kunden_info_x, kunden_info_y)
            pdf.cell(80, 30, '', 0, 1, 'R')  # Container without background color

            # Position title inside the container with larger font and bold
            pdf.set_xy(kunden_info_x + 5, kunden_info_y + 2)  # Add padding inside the container
            pdf.set_font('Arial', 'B', 14)  # Bold and larger font for the title
            pdf.cell(0, 6, 'Kundeninfo:', 0, 1, 'L')

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
            pdf.ln(2)  # Add a space between the title and the content


        pdf.set_font('Arial', 'B', 12)

        # Table Header (with only a bottom border)
        pdf.cell(30, 10, 'CodeNr', 0, 0, 'C')
        pdf.cell(60, 10, 'Produkt', 0, 0, 'C')
        pdf.cell(30, 10, 'Menge', 0, 0, 'C')
        pdf.cell(30, 10, 'Einzelpreis', 0, 0, 'C')
        pdf.cell(40, 10, 'Gesamtsumme', 0, 1, 'C')

        # Draw horizontal line under header
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

        pdf.set_font('Arial', '', 12)

        # Initialize total values
        subtotal = 0.0  

        # Table Data (without any borders or background)
        for product in selected_products:
            menge = float(product[1])  # Menge (Quantity)
            einzelpreis = float(product[3])  # Einzelpreis (Unit Price)
            gesamtsumme = menge * einzelpreis  # Gesamtsumme

            # Accumulate subtotal
            subtotal += gesamtsumme

            pdf.cell(30, 10, product[0], 0, 0, 'C')  # CodeNr
            pdf.cell(60, 10, product[2], 0, 0, 'C')  # Produkt
            pdf.cell(30, 10, str(menge), 0, 0, 'C')  # Menge
            pdf.cell(30, 10, f"{einzelpreis:.2f}", 0, 0, 'C')  # Einzelpreis
            pdf.cell(40, 10, f"{gesamtsumme:.2f}", 0, 1, 'C')  # Gesamtsumme

        # Draw horizontal line under the last row
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

        # Retrieve VAT percentage
        settings = session.query(billSettings).first()
        mwst = float(settings.VAT) if settings else 0.0  # Ensure a numeric value

        # Calculate VAT and total
        vat_amount = subtotal * (mwst / 100)
        total_amount = subtotal + vat_amount

        # Add totals below the table
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(150, 10, "Zwischensumme:", 0, 0, 'R')
        pdf.cell(40, 10, f"{subtotal:.2f}", 0, 1, 'R')

        pdf.cell(150, 10, f"MwSt. ({mwst}%):", 0, 0, 'R')
        pdf.cell(40, 10, f"{vat_amount:.2f}", 0, 1, 'R')

        pdf.cell(150, 10, "Gesamtbetrag:", 0, 0, 'R')
        pdf.cell(40, 10, f"{total_amount:.2f}", 0, 1, 'R')

        # Save the PDF
        pdf.output(pdf_path)


    def export_pdf(self):
        """Export the PDF document to a user-specified location"""
        if not hasattr(self, 'pdf_path') or not self.pdf_path or not os.path.exists(self.pdf_path):
            QMessageBox.warning(
                self.create_bill_page,
                "Export Fehler",
                "Es gibt kein PDF-Dokument zum Exportieren."
            )
            return False
        
        # Generate a default filename based on document type and current date
        default_name = f"{self.page_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
        # Show save dialog
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.create_bill_page, 
            "PDF speichern", 
            os.path.join(os.path.expanduser("~"), "Downloads", default_name),
            "PDF Dateien (*.pdf);;Alle Dateien (*)", 
            options=options
        )
        
        if file_path:
            try:
                # Ensure file has .pdf extension
                if not file_path.lower().endswith('.pdf'):
                    file_path += '.pdf'
                    
                # Copy the PDF file
                copyfile(self.pdf_path, file_path)
                
                # Save document to database
                self.save_to_order()

                QMessageBox.information(
                    self.create_bill_page, 
                    "Export erfolgreich", 
                    f"PDF wurde erfolgreich exportiert nach:\n{file_path}"
                )
                return True
            except Exception as e:
                QMessageBox.critical(
                    self.create_bill_page, 
                    "Export Fehler", 
                    f"Fehler beim Exportieren der PDF: {str(e)}"
                )
                return False
        return False

    def print_pdf(self):
        """Print the PDF document using system default PDF viewer"""
        if not hasattr(self, 'pdf_path') or not self.pdf_path or not os.path.exists(self.pdf_path):
            QMessageBox.warning(
                self.create_bill_page,
                "Drucken Fehler",
                "Es gibt kein PDF-Dokument zum Drucken."
            )
            return False
            
        try:
            # Get absolute path to the PDF
            file_path = os.path.abspath(self.pdf_path)
            
            # Use system-specific commands
            system = platform.system()
            
            if system == "Windows":
                # Windows - use shell command to print
                os.startfile(file_path, 'print')
                success_message = "PDF wurde an den Drucker gesendet."
            elif system == "Darwin":  # macOS
                # Open with Preview on macOS
                subprocess.run(['open', '-a', 'Preview', file_path])
                success_message = "PDF wurde in Preview geöffnet. Bitte verwenden Sie den Drucken-Dialog."
            else:  # Linux and other Unix systems
                # Use xdg-open on Linux
                subprocess.run(['xdg-open', file_path])
                success_message = "PDF wurde mit dem Standardbetrachter geöffnet. Bitte verwenden Sie den Drucken-Dialog."
                
            QMessageBox.information(
                self.create_bill_page, 
                "Drucken", 
                success_message
            )
            return True
        except Exception as e:
            QMessageBox.critical(
                self.create_bill_page, 
                "Drucken Fehler", 
                f"Fehler beim Drucken der PDF: {str(e)}"
            )
            return False


    def save_to_order(self):
        """Save the document to the database and optionally close the window"""
        # Create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        # Retrieve VAT and payment type settings
        settings = session.query(billSettings).first()
        mwst = settings.VAT if settings else None
        payment_type = settings.prices_is if settings else None

        # Calculate summe_netto and summe_brutto
        summe_netto = 0.0
        summe_brutto = 0.0

        for product in self.selected_products:
            try:
                menge = float(product[1])  # Second index (quantity)
                price = float(product[3])  # Last index (price)
                subtotal = menge * price  # Quantity * price

                if payment_type == "Netto":
                    summe_netto += subtotal
                    if mwst is not None:
                        summe_brutto += subtotal * (1 + mwst / 100)  # Add VAT to Netto
                    else:
                        summe_brutto += subtotal  # If no VAT, Brutto equals Netto
                elif payment_type == "Brutto":
                    summe_brutto += subtotal
                    if mwst is not None:
                        summe_netto += subtotal / (1 + mwst / 100)  # Remove VAT from Brutto
                    else:
                        summe_netto += subtotal  # If no VAT, Netto equals Brutto
            except ValueError:
                # Handle cases where quantity or price is invalid
                print(f"Invalid value for product: {product}")
                continue

        # Create a new Document instance and populate it with data from the UI
        document = Document(
            status=True,  # Replace with actual logic if needed
            datum=self.create_bill_page_ui.datumInput.text(),
            betreff=self.create_bill_page_ui.betreffInput.text(),
            kundennummer=self.create_bill_page_ui.Kunden_Nr.text(),
            kunde=self.create_bill_page_ui.kundeInput.text(),
            adresse=self.create_bill_page_ui.adresseInput.text(),
            plz=self.create_bill_page_ui.plzInput.text(),
            ort=self.create_bill_page_ui.ortInput.text(),
            leistungszeitraum=self.create_bill_page_ui.leistungszeitraumInput.text(),
            lieferadresse=self.create_bill_page_ui.lieferadresseInput.text(),
            projekt='Projekt',  # Replace with actual project data
            summe_netto=round(summe_netto, 2),
            summe_brutto=round(summe_brutto, 2),
            summe_kommentare='Kommentare',  # Replace with actual comments
            doc_type=self.page_type,  # Ensure this is set correctly based on the page type
        )

        # Add the document to the session and commit it to the database
        try:
            session.add(document)
            session.commit()
            QMessageBox.information(self.create_bill_page, "Speichern erfolgreich", "Dokument wurde erfolgreich gespeichert.")
            
            # Return to the main page if requested
            if hasattr(self, 'stacked_widget'):
                self.stacked_widget.setCurrentIndex(0)
                
            return True
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            QMessageBox.critical(self.create_bill_page, "Speichern fehlgeschlagen", f"Fehler beim Speichern des Dokuments: {str(e)}")
            return False
        finally:
            session.close()  # Close the session