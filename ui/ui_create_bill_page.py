from PyQt5 import QtCore, QtGui, QtWidgets
from app.widgets.pdf_viewer_widget import PDFViewerWidget

class Ui_CreateBillPage(object):
    def setupUi(self, CreateBillPage):
        CreateBillPage.setObjectName("CreateBillPage")
        CreateBillPage.resize(800, 600)

        # Main layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(CreateBillPage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Left half: Inputs and buttons
        self.leftWidget = QtWidgets.QWidget(CreateBillPage)
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftLayout.setObjectName("leftLayout")
        
        # Add header label above buttons
        # self.headerLabel = QtWidgets.QLabel("Create Bill", self.leftWidget)
        # self.headerLabel.setObjectName("headerLabel")
        # self.headerLabel.setAlignment(QtCore.Qt.AlignCenter)  # Center the label horizontally
        # self.leftLayout.addWidget(self.headerLabel)
        
        # Horizontal layout for buttons
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.leftLayout.addLayout(self.buttonsLayout)

        # Buttons for sections
        self.allgemeinButton = QtWidgets.QPushButton("Allgemein", self.leftWidget)  # Changed from "Info" to "Allgemein"
        self.allgemeinButton.setObjectName("allgemeinButton")
        self.buttonsLayout.addWidget(self.allgemeinButton)
        
        self.kundeButton = QtWidgets.QPushButton("Kunde", self.leftWidget)  # Changed from "Address" to "Kunde"
        self.kundeButton.setObjectName("kundeButton")
        self.buttonsLayout.addWidget(self.kundeButton)
        
        self.artikelButton = QtWidgets.QPushButton("Artikel", self.leftWidget)  # Changed from "Order" to "Artikel"
        self.artikelButton.setObjectName("artikelButton")
        self.buttonsLayout.addWidget(self.artikelButton)

        # StackedWidget for different inputs
        self.inputsStackedWidget = QtWidgets.QStackedWidget(self.leftWidget)
        self.inputsStackedWidget.setObjectName("inputsStackedWidget")
        self.leftLayout.addWidget(self.inputsStackedWidget)

        # Allgemein inputs (formerly Info inputs)
        self.allgemeinPage = QtWidgets.QWidget()
        self.allgemeinPage.setObjectName("allgemeinPage")
        self.allgemeinLayout = QtWidgets.QVBoxLayout(self.allgemeinPage)
        self.nameInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.nameInput.setPlaceholderText("Name")
        self.allgemeinLayout.addWidget(self.nameInput)
        self.ageInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.ageInput.setPlaceholderText("Age")
        self.allgemeinLayout.addWidget(self.ageInput)
        self.emailInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.emailInput.setPlaceholderText("Email")
        self.allgemeinLayout.addWidget(self.emailInput)
        self.addAllgemeinButton = QtWidgets.QPushButton("Add Info", self.allgemeinPage)
        self.addAllgemeinButton.setObjectName("addAllgemeinButton")
        self.allgemeinLayout.addWidget(self.addAllgemeinButton)
        self.inputsStackedWidget.addWidget(self.allgemeinPage)



        # Kunde inputs (formerly Address inputs)
        self.kundePage = QtWidgets.QWidget()
        self.kundePage.setObjectName("kundePage")
        self.kundeLayout = QtWidgets.QVBoxLayout(self.kundePage)

        # 1st Row: Anrede (select menu) and UID-NR
        self.anredeUIDLayout = QtWidgets.QHBoxLayout()
        
        self.anredeLabel = QtWidgets.QLabel("Anrede")
        self.anredeSelect = QtWidgets.QComboBox(self.kundePage)
        self.anredeSelect.setMinimumWidth(150) 
        self.anredeSelect.addItems(["Herr", "Frau", "Firma"])  # Sample options
        self.anredeUIDLayout.addWidget(self.anredeLabel)
        self.anredeUIDLayout.addWidget(self.anredeSelect)

        self.uidNrLabel = QtWidgets.QLabel("UID-NR")
        self.uidNrInput = QtWidgets.QLineEdit(self.kundePage)
        self.uidNrInput.setPlaceholderText("UID-NR")
        self.anredeUIDLayout.addWidget(self.uidNrLabel)
        self.anredeUIDLayout.addWidget(self.uidNrInput)
        
        self.kundeLayout.addLayout(self.anredeUIDLayout)

        # 2nd Row: Kunde and Keine MwSt (Checkbox)
        self.kundeMwstLayout = QtWidgets.QHBoxLayout()
        
        self.kundeLabel = QtWidgets.QLabel("Kunde")
        self.kundeInput = QtWidgets.QLineEdit(self.kundePage)
        self.kundeInput.setPlaceholderText("Kunde")
        self.kundeMwstLayout.addWidget(self.kundeLabel)
        self.kundeMwstLayout.addWidget(self.kundeInput)

        self.Kunden_Nr = QtWidgets.QLineEdit(self.kundePage)
        self.Kunden_Nr.setPlaceholderText("Kunde")
        self.Kunden_Nr.hide()

        self.kundeMwstLayout.addWidget(self.kundeInput)

        self.telefon = QtWidgets.QLineEdit(self.kundePage)
        self.telefon.setPlaceholderText("Kunde")
        self.telefon.hide()
          
        self.kundeMwstLayout.addWidget(self.telefon)


        self.keineMwstCheckbox = QtWidgets.QCheckBox("Keine MwSt")
        self.kundeMwstLayout.addWidget(self.keineMwstCheckbox)

        self.kundeLayout.addLayout(self.kundeMwstLayout)

        # 3rd Row: Kontaktperson
        self.contactLayout = QtWidgets.QHBoxLayout()
        self.kontaktpersonLabel = QtWidgets.QLabel("Kontaktperson")
        self.kontaktpersonInput = QtWidgets.QLineEdit(self.kundePage)
        self.kontaktpersonInput.setPlaceholderText("Kontaktperson")

        self.contactLayout.addWidget(self.kontaktpersonLabel)
        self.contactLayout.addWidget(self.kontaktpersonInput)

        self.telefonLabel = QtWidgets.QLabel("Telefon")
        self.telefonInput = QtWidgets.QLineEdit(self.kundePage)
        self.telefonInput.setPlaceholderText("Telefon")

        self.contactLayout.addWidget(self.telefonLabel)
        self.contactLayout.addWidget(self.telefonInput)

        self.kundeLayout.addLayout(self.contactLayout)

        # 4th Row: Adresse and Lieferadresse
        self.adresseLieferadresseLayout = QtWidgets.QHBoxLayout()

        self.adresseLabel = QtWidgets.QLabel("Adresse")
        self.adresseInput = QtWidgets.QLineEdit(self.kundePage)
        self.adresseInput.setPlaceholderText("Adresse")
        self.adresseLieferadresseLayout.addWidget(self.adresseLabel)
        self.adresseLieferadresseLayout.addWidget(self.adresseInput)

        self.lieferadresseLabel = QtWidgets.QLabel("Lieferadresse")
        self.lieferadresseInput = QtWidgets.QLineEdit(self.kundePage)
        self.lieferadresseInput.setPlaceholderText("Lieferadresse")
        self.adresseLieferadresseLayout.addWidget(self.lieferadresseLabel)
        self.adresseLieferadresseLayout.addWidget(self.lieferadresseInput)

        self.kundeLayout.addLayout(self.adresseLieferadresseLayout)

        # 5th Row: PLZ and Ort
        self.plzOrtLayout = QtWidgets.QHBoxLayout()

        self.plzLabel = QtWidgets.QLabel("PLZ")
        self.plzInput = QtWidgets.QLineEdit(self.kundePage)
        self.plzInput.setPlaceholderText("PLZ")
        self.plzOrtLayout.addWidget(self.plzLabel)
        self.plzOrtLayout.addWidget(self.plzInput)

        self.ortLabel = QtWidgets.QLabel("Ort")
        self.ortInput = QtWidgets.QLineEdit(self.kundePage)
        self.ortInput.setPlaceholderText("Ort")
        self.plzOrtLayout.addWidget(self.ortLabel)
        self.plzOrtLayout.addWidget(self.ortInput)

        self.kundeLayout.addLayout(self.plzOrtLayout)

        # 6th Row: Land (select menu)
        self.landLabel = QtWidgets.QLabel("Land")
        self.landSelect = QtWidgets.QComboBox(self.kundePage)
        self.landSelect.addItems(["Germany", "Austria", "Switzerland"])  # Sample countries
        self.kundeLayout.addWidget(self.landLabel)
        self.kundeLayout.addWidget(self.landSelect)

        # Table for Customers (connected to DB)
        self.kundeContainer = QtWidgets.QWidget(self.kundePage)
        self.kundeContainer.setObjectName("kundeContainer")
        self.kundeContainerLayout = QtWidgets.QVBoxLayout(self.kundeContainer)
        self.kundeContainerLayout.setContentsMargins(10, 120, 10, 10)
        self.kundeContainerLayout.setSpacing(10)  # Remove space between elements
        self.kundeContainerLayout.setAlignment(QtCore.Qt.AlignTop)

        # Search input for Customer table
        self.kundeSearchInput = QtWidgets.QLineEdit(self.kundeContainer)
        self.kundeSearchInput.setPlaceholderText("Search Customer Name")
        self.kundeSearchInput.setObjectName("kundeSearch")
        self.kundeContainerLayout.addWidget(self.kundeSearchInput)

        # Customer table
        self.customerTable = QtWidgets.QTableWidget(self.kundeContainer)
        self.customerTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.customerTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.customerTable.setObjectName("customerTable")

        self.customerTable.setColumnCount(6)
        self.customerTable.setHorizontalHeaderLabels(["Nummer", "Kunde", "Adresse", "PLZ", "Ort", "telefon"])
        
        # Adjusting the table size and column width
        self.customerTable.setFixedHeight(250)
        self.customerTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.customerTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.customerTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.customerTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.kundeContainerLayout.addWidget(self.customerTable)

        # Add entity and remove last row buttons (same as Artikel)
        self.kundeButtonsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.addKundeEntityButton = QtWidgets.QPushButton(self.kundeContainer)
        self.addKundeEntityButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addKundeEntityButton.setText("Add Customer")
        self.kundeButtonsHorizontalLayout.addWidget(self.addKundeEntityButton)
        
        self.removeKundeLastRowButton = QtWidgets.QPushButton(self.kundeContainer)
        self.removeKundeLastRowButton.setIcon(QtGui.QIcon('resources/icons/x.png'))
        self.removeKundeLastRowButton.setText("Remove last row")
        self.kundeButtonsHorizontalLayout.addWidget(self.removeKundeLastRowButton)
        
        self.kundeContainerLayout.addLayout(self.kundeButtonsHorizontalLayout)

        self.kundeLayout.addWidget(self.kundeContainer)

        # Add the Kunde page to the stacked widget
        self.inputsStackedWidget.addWidget(self.kundePage)

        # Artikel inputs (formerly Order inputs)
        self.artikelPage = QtWidgets.QWidget()
        self.artikelPage.setObjectName("artikelPage")
        self.artikelLayout = QtWidgets.QVBoxLayout(self.artikelPage)

        # Inputs section above artikelContainer
        self.inputsSection = QtWidgets.QWidget()
        self.inputsSectionLayout = QtWidgets.QVBoxLayout(self.inputsSection)

        self.inputsSection.setContentsMargins(0, 70, 0, 0)
        self.inputsSection.setObjectName("inputsSection")

        # Kapitel and Unterkapitel
        self.kapitelUnterkapitelLayout = QtWidgets.QHBoxLayout()
        
        self.kapitelLabel = QtWidgets.QLabel("Kapitel")
        self.kapitelInput = QtWidgets.QLineEdit(self.inputsSection)
        self.kapitelInput.setPlaceholderText("Kapitel")
        self.kapitelUnterkapitelLayout.addWidget(self.kapitelLabel)
        self.kapitelUnterkapitelLayout.addWidget(self.kapitelInput)

        self.unterkapitelLabel = QtWidgets.QLabel("Unterkapitel")
        self.unterkapitelInput = QtWidgets.QLineEdit(self.inputsSection)
        self.unterkapitelInput.setPlaceholderText("Unterkapitel")
        self.kapitelUnterkapitelLayout.addWidget(self.unterkapitelLabel)
        self.kapitelUnterkapitelLayout.addWidget(self.unterkapitelInput)
        self.inputsSectionLayout.addLayout(self.kapitelUnterkapitelLayout)

        # Preis netto and Rabatt in %
        self.preisRabattLayout = QtWidgets.QHBoxLayout()
        
        # New Name Input Added Here
        self.artikelNameLabel = QtWidgets.QLabel("Name")
        self.artikelNameInput = QtWidgets.QLineEdit(self.inputsSection)
        self.artikelNameInput.setPlaceholderText("Name")
        self.preisRabattLayout.addWidget(self.artikelNameLabel)
        self.preisRabattLayout.addWidget(self.artikelNameInput)

        # Existing Preis netto Input
        self.preisNettoLabel = QtWidgets.QLabel("Preis netto")
        self.preisNettoInput = QtWidgets.QLineEdit(self.inputsSection)
        self.preisNettoInput.setPlaceholderText("Preis netto")
        self.preisRabattLayout.addWidget(self.preisNettoLabel)
        self.preisRabattLayout.addWidget(self.preisNettoInput)

        # Existing Rabatt in % Input
        self.rabattLabel = QtWidgets.QLabel("Rabatt in %")
        self.rabattInput = QtWidgets.QLineEdit(self.inputsSection)
        self.rabattInput.setPlaceholderText("Rabatt in %")
        self.preisRabattLayout.addWidget(self.rabattLabel)
        self.preisRabattLayout.addWidget(self.rabattInput)
        self.inputsSectionLayout.addLayout(self.preisRabattLayout)

        # Menge, Einheit, MwSt. in %, Summe Netto
        self.mengeEinheitLayout = QtWidgets.QHBoxLayout()
        
        self.mengeLabel = QtWidgets.QLabel("Menge")
        self.mengeInput = QtWidgets.QLineEdit(self.inputsSection)
        self.mengeInput.setPlaceholderText("Menge")
        self.mengeEinheitLayout.addWidget(self.mengeLabel)
        self.mengeEinheitLayout.addWidget(self.mengeInput)

        self.einheitLabel = QtWidgets.QLabel("Einheit")
        self.einheitInput = QtWidgets.QLineEdit(self.inputsSection)
        self.einheitInput.setPlaceholderText("Einheit")
        self.mengeEinheitLayout.addWidget(self.einheitLabel)
        self.mengeEinheitLayout.addWidget(self.einheitInput)

        self.mwstLabel = QtWidgets.QLabel("MwSt. in %")
        self.mwstInput = QtWidgets.QLineEdit(self.inputsSection)
        self.mwstInput.setPlaceholderText("MwSt. in %")
        self.mengeEinheitLayout.addWidget(self.mwstLabel)
        self.mengeEinheitLayout.addWidget(self.mwstInput)

        self.summeNettoLabel = QtWidgets.QLabel("Summe Netto")
        self.summeNettoInput = QtWidgets.QLineEdit(self.inputsSection)
        self.summeNettoInput.setPlaceholderText("Summe Netto")
        self.mengeEinheitLayout.addWidget(self.summeNettoLabel)
        self.mengeEinheitLayout.addWidget(self.summeNettoInput)

        self.inputsSectionLayout.addLayout(self.mengeEinheitLayout)
        self.artikelLayout.addWidget(self.inputsSection)

        # Artikel container (formerly orderContainer)
        self.artikelContainer = QtWidgets.QWidget(self.artikelPage)
        self.artikelContainer.setObjectName("artikelContainer")
        self.artikelContainerLayout = QtWidgets.QVBoxLayout(self.artikelContainer)
        self.artikelContainerLayout.setContentsMargins(10, 120, 10, 10)
        self.artikelContainerLayout.setSpacing(10)  # Remove space between elements
        self.artikelContainerLayout.setAlignment(QtCore.Qt.AlignTop)  # Center the content

        # Search input and product table
        self.artikelSearchInput = QtWidgets.QLineEdit(self.artikelContainer)
        self.artikelSearchInput.setPlaceholderText("Search Product Name")
        self.artikelSearchInput.setObjectName("artikelSearch")
        self.artikelContainerLayout.addWidget(self.artikelSearchInput)
        
        self.productTable = QtWidgets.QTableWidget(self.artikelContainer)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.productTable.setObjectName("artikelTable")

        self.productTable.setColumnCount(3)
        self.productTable.setHorizontalHeaderLabels(["CodeNr", "Name", "SalesPrice"])
        
        # Adjusting the table size and column width
        self.productTable.setFixedHeight(250)  # Adjust the table height as needed
        self.productTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.artikelContainerLayout.addWidget(self.productTable)

        # Add entity and remove last row buttons on the same horizontal line
        self.buttonsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.addEntityButton = QtWidgets.QPushButton(self.artikelContainer)
        self.addEntityButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addEntityButton.setText("Add entity")
        self.buttonsHorizontalLayout.addWidget(self.addEntityButton)
        
        self.removeLastRowButton = QtWidgets.QPushButton(self.artikelContainer)
        self.removeLastRowButton.setIcon(QtGui.QIcon('resources/icons/x.png'))
        self.removeLastRowButton.setText("Remove last row")
        self.buttonsHorizontalLayout.addWidget(self.removeLastRowButton)
        
        self.artikelContainerLayout.addLayout(self.buttonsHorizontalLayout)

        self.artikelLayout.addWidget(self.artikelContainer)
        self.inputsStackedWidget.addWidget(self.artikelPage)

        # Export button (only for allgemein and kunde tabs)
        self.exportButton = QtWidgets.QPushButton("Export to PDF", self.leftWidget)
        self.exportButton.setObjectName("exportButton")
        self.leftLayout.addWidget(self.exportButton)
        
        self.horizontalLayout.addWidget(self.leftWidget)
        
        # Right half: PDF viewer
        self.pdfViewer = PDFViewerWidget(CreateBillPage)
        self.horizontalLayout.addWidget(self.pdfViewer)

        self.retranslateUi(CreateBillPage)
        QtCore.QMetaObject.connectSlotsByName(CreateBillPage)

    def retranslateUi(self, CreateBillPage):
        _translate = QtCore.QCoreApplication.translate
        CreateBillPage.setWindowTitle(_translate("CreateBillPage", "Create Bill Page"))
