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
        
        # Horizontal layout for buttons
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.leftLayout.addLayout(self.buttonsLayout)

        # Buttons for sections
        self.infoButton = QtWidgets.QPushButton("Info", self.leftWidget)
        self.infoButton.setObjectName("infoButton")
        self.buttonsLayout.addWidget(self.infoButton)
        
        self.addressButton = QtWidgets.QPushButton("Address", self.leftWidget)
        self.addressButton.setObjectName("addressButton")
        self.buttonsLayout.addWidget(self.addressButton)
        
        self.orderButton = QtWidgets.QPushButton("Order", self.leftWidget)
        self.orderButton.setObjectName("orderButton")
        self.buttonsLayout.addWidget(self.orderButton)

        # StackedWidget for different inputs
        self.inputsStackedWidget = QtWidgets.QStackedWidget(self.leftWidget)
        self.inputsStackedWidget.setObjectName("inputsStackedWidget")
        self.leftLayout.addWidget(self.inputsStackedWidget)


        # Info inputs
        self.infoPage = QtWidgets.QWidget()
        self.infoPage.setObjectName("infoPage")
        self.infoLayout = QtWidgets.QVBoxLayout(self.infoPage)
        self.nameInput = QtWidgets.QLineEdit(self.infoPage)
        self.nameInput.setPlaceholderText("Name")
        self.infoLayout.addWidget(self.nameInput)
        self.ageInput = QtWidgets.QLineEdit(self.infoPage)
        self.ageInput.setPlaceholderText("Age")
        self.infoLayout.addWidget(self.ageInput)
        self.emailInput = QtWidgets.QLineEdit(self.infoPage)
        self.emailInput.setPlaceholderText("Email")
        self.infoLayout.addWidget(self.emailInput)
        self.addInfoButton = QtWidgets.QPushButton("Add Info", self.infoPage)
        self.addInfoButton.setObjectName("addInfoButton")
        self.infoLayout.addWidget(self.addInfoButton)
        self.inputsStackedWidget.addWidget(self.infoPage)

        # Address inputs
        self.addressPage = QtWidgets.QWidget()
        self.addressPage.setObjectName("addressPage")
        self.addressLayout = QtWidgets.QVBoxLayout(self.addressPage)
        self.addressInput = QtWidgets.QLineEdit(self.addressPage)
        self.addressInput.setPlaceholderText("Address")
        self.addressLayout.addWidget(self.addressInput)
        self.phoneNumberInput = QtWidgets.QLineEdit(self.addressPage)
        self.phoneNumberInput.setPlaceholderText("Phone Number")
        self.addressLayout.addWidget(self.phoneNumberInput)
        self.addAddressDataButton = QtWidgets.QPushButton("Add Address Data", self.addressPage)
        self.addAddressDataButton.setObjectName("addAddressDataButton")
        self.addressLayout.addWidget(self.addAddressDataButton)
        self.inputsStackedWidget.addWidget(self.addressPage)

        # Order inputs
        self.orderPage = QtWidgets.QWidget()
        self.orderPage.setObjectName("orderPage")
        self.orderLayout = QtWidgets.QVBoxLayout(self.orderPage)

        # Inputs section above orderContainer
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
        self.orderNameLabel = QtWidgets.QLabel("Name")
        self.orderNameInput = QtWidgets.QLineEdit(self.inputsSection)
        self.orderNameInput.setPlaceholderText("Name")
        self.preisRabattLayout.addWidget(self.orderNameLabel)
        self.preisRabattLayout.addWidget(self.orderNameInput)

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
        self.orderLayout.addWidget(self.inputsSection)

        # Order container
        self.orderContainer = QtWidgets.QWidget(self.orderPage)
        self.orderContainer.setObjectName("orderContainer")
        self.orderContainerLayout = QtWidgets.QVBoxLayout(self.orderContainer)
        self.orderContainerLayout.setContentsMargins(10, 120, 10, 10)
        self.orderContainerLayout.setSpacing(10)  # Remove space between elements
        self.orderContainerLayout.setAlignment(QtCore.Qt.AlignTop)  # Center the content


        # Search input and product table
        self.orderSearchInput = QtWidgets.QLineEdit(self.orderContainer)
        self.orderSearchInput.setPlaceholderText("Search Product Name")
        self.orderSearchInput.setObjectName("orderSearch")
        self.orderContainerLayout.addWidget(self.orderSearchInput)
        
        self.productTable = QtWidgets.QTableWidget(self.orderContainer)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.productTable.setObjectName("orderTable")

        self.productTable.setColumnCount(3)
        self.productTable.setHorizontalHeaderLabels(["CodeNr", "Name", "SalesPrice"])
        
        # Adjusting the table size and column width
        self.productTable.setFixedHeight(180)  # Adjust the table height as needed
        self.productTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.orderContainerLayout.addWidget(self.productTable)

        # Add entity and remove last row buttons on the same horizontal line
        self.buttonsHorizontalLayout = QtWidgets.QHBoxLayout()
        self.addEntityButton = QtWidgets.QPushButton(self.orderContainer)
        self.addEntityButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addEntityButton.setText("Add entity")
        self.buttonsHorizontalLayout.addWidget(self.addEntityButton)
        
        self.removeLastRowButton = QtWidgets.QPushButton(self.orderContainer)
        self.removeLastRowButton.setIcon(QtGui.QIcon('resources/icons/x.png'))
        self.removeLastRowButton.setText("Remove last row")
        self.buttonsHorizontalLayout.addWidget(self.removeLastRowButton)
        
        self.orderContainerLayout.addLayout(self.buttonsHorizontalLayout)

        self.orderLayout.addWidget(self.orderContainer)
        self.inputsStackedWidget.addWidget(self.orderPage)

        # Export button (only for info and address tabs)
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
