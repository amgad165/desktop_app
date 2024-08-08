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

        # Container for order section with background color
        self.orderContainer = QtWidgets.QWidget(self.orderPage)
        self.orderContainer.setObjectName("orderContainer")
        self.orderContainerLayout = QtWidgets.QVBoxLayout(self.orderContainer)
        self.orderContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.orderContainer.setObjectName("orderContainer")

        # Number of Products input
        self.numProductsInput = QtWidgets.QLineEdit(self.orderContainer)
        self.numProductsInput.setPlaceholderText("Number of Products")
        self.orderLayout.addWidget(self.numProductsInput)


        

        self.orderSearchInput = QtWidgets.QLineEdit(self.orderContainer)
        self.orderSearchInput.setPlaceholderText("Search Product Name")
        self.orderContainerLayout.addWidget(self.orderSearchInput)

        # Table widget for Product display
        self.productTable = QtWidgets.QTableWidget(self.orderContainer)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
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
