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
        self.buttonsLayout.addWidget(self.infoButton)
        self.addressButton = QtWidgets.QPushButton("Address", self.leftWidget)
        self.buttonsLayout.addWidget(self.addressButton)
        self.orderButton = QtWidgets.QPushButton("Order", self.leftWidget)
        self.buttonsLayout.addWidget(self.orderButton)

        # StackedWidget for different inputs
        self.inputsStackedWidget = QtWidgets.QStackedWidget(self.leftWidget)
        self.leftLayout.addWidget(self.inputsStackedWidget)

        # Info inputs
        self.infoPage = QtWidgets.QWidget()
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
        self.inputsStackedWidget.addWidget(self.infoPage)

        # Address inputs
        self.addressPage = QtWidgets.QWidget()
        self.addressLayout = QtWidgets.QVBoxLayout(self.addressPage)
        self.addressInput = QtWidgets.QLineEdit(self.addressPage)
        self.addressInput.setPlaceholderText("Address")
        self.addressLayout.addWidget(self.addressInput)
        self.phoneNumberInput = QtWidgets.QLineEdit(self.addressPage)
        self.phoneNumberInput.setPlaceholderText("Phone Number")
        self.addressLayout.addWidget(self.phoneNumberInput)
        self.inputsStackedWidget.addWidget(self.addressPage)

        # Order inputs
        self.orderPage = QtWidgets.QWidget()
        self.orderLayout = QtWidgets.QVBoxLayout(self.orderPage)
        self.orderSearchInput = QtWidgets.QLineEdit(self.orderPage)
        self.orderSearchInput.setPlaceholderText("Search Product Name")
        self.orderLayout.addWidget(self.orderSearchInput)

        # Table widget for Product display
        self.productTable = QtWidgets.QTableWidget(self.orderPage)
        self.productTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.productTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.productTable.setColumnCount(3)
        self.productTable.setHorizontalHeaderLabels(["CodeNr", "Name", "SalesPrice"])
        
        # Adjusting the table size and column width
        self.productTable.setFixedHeight(150)  # Adjust the table height as needed
        self.productTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        # self.productTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.orderLayout.addWidget(self.productTable)
        self.inputsStackedWidget.addWidget(self.orderPage)

        # Submit and export buttons
        self.submitButton = QtWidgets.QPushButton("Submit", self.leftWidget)
        self.leftLayout.addWidget(self.submitButton)
        self.exportButton = QtWidgets.QPushButton("Export to PDF", self.leftWidget)
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