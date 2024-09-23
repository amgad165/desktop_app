from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1700, 850)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main horizontal layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Sidebar QFrame
        self.sidebar = QtWidgets.QFrame(self.centralwidget)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sidebar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sidebar.setFixedWidth(150)  # Set a fixed width for the sidebar

        # Vertical layout for sidebar content
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # No margins
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addSpacing(4)
        # Container widget for home icon and label
        self.homeContainer = QtWidgets.QWidget(self.sidebar)
        self.homeContainer.setObjectName("sideContainer")
        
        # Horizontal layout for home icon and label
        self.homeLayout = QtWidgets.QHBoxLayout(self.homeContainer)
        self.homeLayout.setContentsMargins(10, 0, 0, 0)
        self.homeLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.homeLayout.setObjectName("homeLayout")
        self.homeLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Home Icon button
        self.homeIconButton = QtWidgets.QPushButton(self.homeContainer)
        self.homeIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.homeIconButton.setObjectName("sideIconButton")
        icon_home = QtGui.QIcon("resources/icons/home.png")  # Set the path to your icon file
        self.homeIconButton.setIcon(icon_home)
        self.homeIconButton.setIconSize(self.homeIconButton.size())  # Use button's size as icon size
        self.homeLayout.addWidget(self.homeIconButton)

        # Home Label
        self.homeLabel = QtWidgets.QLabel(self.homeContainer)
        self.homeLabel.setObjectName("sideLabel")
        self.homeLabel.setFixedHeight(50)  # Set a fixed height
        self.homeLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.homeLayout.addWidget(self.homeLabel)

        # Add home container to the sidebar
        self.verticalLayout.addWidget(self.homeContainer)

        # Add margin between home and create bill containers
        self.verticalLayout.addSpacing(4)  # Add spacing between containers

        # Container widget for create bill icon and label
        self.createBillContainer = QtWidgets.QWidget(self.sidebar)
        self.createBillContainer.setObjectName("sideContainer")
        
        # Horizontal layout for create bill icon and label
        self.createBillLayout = QtWidgets.QHBoxLayout(self.createBillContainer)
        self.createBillLayout.setContentsMargins(10, 0, 0, 0)
        self.createBillLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.createBillLayout.setObjectName("createBillLayout")
        self.createBillLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Create Bill Icon button
        self.createBillIconButton = QtWidgets.QPushButton(self.createBillContainer)
        self.createBillIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.createBillIconButton.setObjectName("sideIconButton")
        icon_create_bill = QtGui.QIcon("resources/icons/bill.png")  # Set the path to your icon file
        self.createBillIconButton.setIcon(icon_create_bill)
        self.createBillIconButton.setIconSize(self.createBillIconButton.size())  # Use button's size as icon size
        self.createBillLayout.addWidget(self.createBillIconButton)

        # Create Bill Label
        self.createBillLabel = QtWidgets.QLabel(self.createBillContainer)
        self.createBillLabel.setObjectName("sideLabel")
        self.createBillLabel.setFixedHeight(50)  # Set a fixed height
        self.createBillLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.createBillLayout.addWidget(self.createBillLabel)

        # Add create bill container to the sidebar
        self.verticalLayout.addWidget(self.createBillContainer)

        # Add margin between create bill and customers containers
        self.verticalLayout.addSpacing(4)



        # Container widget for documents icon and label (dropdown)
        self.documentContainer = QtWidgets.QWidget(self.sidebar)
        self.documentContainer.setObjectName("sideContainer")

        # Horizontal layout for documents icon, label, and dropdown arrow
        self.documentLayout = QtWidgets.QHBoxLayout(self.documentContainer)
        self.documentLayout.setContentsMargins(10, 0, 0, 0)
        self.documentLayout.setSpacing(1)
        self.documentLayout.setObjectName("documentLayout")
        self.documentLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Document Icon button
        self.documentIconButton = QtWidgets.QPushButton(self.documentContainer)
        self.documentIconButton.setFixedSize(20, 20)
        self.documentIconButton.setObjectName("sideIconButton")
        icon_document = QtGui.QIcon("resources/icons/document.png")  # Set the path to your document icon file
        
        self.documentIconButton.setIcon(icon_document)
        self.documentIconButton.setIconSize(self.documentIconButton.size())
        self.documentLayout.addWidget(self.documentIconButton)

        # Document Label
        self.documentLabel = QtWidgets.QLabel(self.documentContainer)
        self.documentLabel.setObjectName("sideLabel")
        self.documentLabel.setFixedHeight(50)
        self.documentLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.documentLayout.addWidget(self.documentLabel)

        # Add a down arrow icon next to the document label
        self.arrowIconButton = QtWidgets.QPushButton(self.documentContainer)
        self.arrowIconButton.setFixedSize(20, 20)
        self.arrowIconButton.setObjectName("sideIconButton")
        icon_arrow_down = QtGui.QIcon("resources/icons/arrow_down.png")  # Set the path to your arrow icon
        self.arrowIconButton.setIcon(icon_arrow_down)
        self.arrowIconButton.setIconSize(self.arrowIconButton.size())
        self.documentLayout.addWidget(self.arrowIconButton)

        # Add document container to the sidebar
        self.verticalLayout.addWidget(self.documentContainer)

        # Dropdown items (initially hidden)
        self.documentItemsContainer = QtWidgets.QWidget(self.sidebar)
        self.documentItemsLayout = QtWidgets.QVBoxLayout(self.documentItemsContainer)
        self.documentItemsContainer.setObjectName("drop_container")
        self.documentItemsContainer.setVisible(False)  # Hidden by default

        # Add three items (Item 1, Item 2, Item 3) with icons
        self.item1Container = QtWidgets.QWidget(self.documentItemsContainer)
        self.item1Layout = QtWidgets.QHBoxLayout(self.item1Container)
        self.item1Icon = QtWidgets.QPushButton(self.item1Container)
        self.item1Icon.setFixedSize(20, 20)
        icon_item1 = QtGui.QIcon("resources/icons/offer.png")  # Set the path to your item 1 icon
        self.item1Icon.setObjectName("sideIconButton")
        self.item1Icon.setIcon(icon_item1)
        self.item1Icon.setIconSize(self.item1Icon.size())


        self.item1Layout.addWidget(self.item1Icon)

        self.item1Label = QtWidgets.QLabel("Angebot")
        self.item1Label.setObjectName("drop_item")
        self.item1Layout.addWidget(self.item1Label)

        self.item1Container.setObjectName("sideContainer")
        self.documentItemsLayout.addWidget(self.item1Container)

        # Item 2
        self.item2Container = QtWidgets.QWidget(self.documentItemsContainer)
        self.item2Layout = QtWidgets.QHBoxLayout(self.item2Container)
        self.item2Icon = QtWidgets.QPushButton(self.item2Container)
        self.item2Icon.setFixedSize(20, 20)
        icon_item2 = QtGui.QIcon("resources/icons/item2.png")  # Set the path to your item 2 icon
        self.item2Icon.setIcon(icon_item2)
        self.item2Icon.setIconSize(self.item2Icon.size())
        self.item2Icon.setObjectName("sideIconButton")


        self.item2Layout.addWidget(self.item2Icon)

        self.item2Label = QtWidgets.QLabel("Item 2")
        self.item2Label.setObjectName("drop_item")
        self.item2Layout.addWidget(self.item2Label)

        self.documentItemsLayout.addWidget(self.item2Container)

        # Item 3
        self.item3Container = QtWidgets.QWidget(self.documentItemsContainer)
        self.item3Layout = QtWidgets.QHBoxLayout(self.item3Container)
        self.item3Icon = QtWidgets.QPushButton(self.item3Container)
        self.item3Icon.setFixedSize(20, 20)
        icon_item3 = QtGui.QIcon("resources/icons/item3.png")  # Set the path to your item 3 icon
        self.item3Icon.setIcon(icon_item3)
        self.item3Icon.setIconSize(self.item3Icon.size())

        self.item3Layout.addWidget(self.item3Icon)

        self.item3Label = QtWidgets.QLabel("Item 3")
        self.item3Label.setObjectName("drop_item")
        self.item3Layout.addWidget(self.item3Label)

        self.documentItemsLayout.addWidget(self.item3Container)
        # Add the documentItemsContainer to the sidebar layout
        self.verticalLayout.addWidget(self.documentItemsContainer)

        # Add spacing between customers and documents
        self.verticalLayout.addSpacing(4)

        # Container widget for customers icon and label
        self.customersContainer = QtWidgets.QWidget(self.sidebar)
        self.customersContainer.setObjectName("sideContainer")
        
        # Horizontal layout for customers icon and label
        self.customersLayout = QtWidgets.QHBoxLayout(self.customersContainer)
        self.customersLayout.setContentsMargins(10, 0, 0, 0)
        self.customersLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.customersLayout.setObjectName("customersLayout")
        self.customersLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Customers Icon button
        self.customersIconButton = QtWidgets.QPushButton(self.customersContainer)
        self.customersIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.customersIconButton.setObjectName("sideIconButton")
        icon_customers = QtGui.QIcon("resources/icons/user.png")  # Set the path to your icon file
        self.customersIconButton.setIcon(icon_customers)
        self.customersIconButton.setIconSize(self.customersIconButton.size())  # Use button's size as icon size

        self.customersLayout.addWidget(self.customersIconButton)

        # Customers Label
        self.customersLabel = QtWidgets.QLabel(self.customersContainer)
        self.customersLabel.setObjectName("sideLabel")
        self.customersLabel.setFixedHeight(50)  # Set a fixed height
        self.customersLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.customersLayout.addWidget(self.customersLabel)

        # Add customers container to the sidebar
        self.verticalLayout.addWidget(self.customersContainer)

        # Add margin between customers and products containers
        self.verticalLayout.addSpacing(4)



        # Container widget for workers icon and label
        self.workersContainer = QtWidgets.QWidget(self.sidebar)
        self.workersContainer.setObjectName("sideContainer")
        
        # Horizontal layout for customers icon and label
        self.workersLayout = QtWidgets.QHBoxLayout(self.workersContainer)
        self.workersLayout.setContentsMargins(10, 0, 0, 0)
        self.workersLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.workersLayout.setObjectName("workersLayout")
        self.workersLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Customers Icon button
        self.workersIconButton = QtWidgets.QPushButton(self.workersContainer)
        self.workersIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.workersIconButton.setObjectName("sideIconButton")
        icon_workers = QtGui.QIcon("resources/icons/work.png")  # Set the path to your icon file
        self.workersIconButton.setIcon(icon_workers)
        self.workersIconButton.setIconSize(self.workersIconButton.size())  # Use button's size as icon size

        self.workersLayout.addWidget(self.workersIconButton)

        # Customers Label
        self.workersLabel = QtWidgets.QLabel(self.workersContainer)
        self.workersLabel.setObjectName("sideLabel")
        self.workersLabel.setFixedHeight(50)  # Set a fixed height
        self.workersLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.workersLayout.addWidget(self.workersLabel)

        # Add customers container to the sidebar
        self.verticalLayout.addWidget(self.workersContainer)

        # Add margin between customers and products containers
        self.verticalLayout.addSpacing(4)





        # Container widget for products icon and label
        self.productsContainer = QtWidgets.QWidget(self.sidebar)
        self.productsContainer.setObjectName("sideContainer")
        
        # Horizontal layout for products icon and label
        self.productsLayout = QtWidgets.QHBoxLayout(self.productsContainer)
        self.productsLayout.setContentsMargins(10, 0, 0, 0)
        self.productsLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.productsLayout.setObjectName("productsLayout")
        self.productsLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Products Icon button
        self.productsIconButton = QtWidgets.QPushButton(self.productsContainer)
        self.productsIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.productsIconButton.setObjectName("sideIconButton")
        icon_products = QtGui.QIcon("resources/icons/products.png")  # Set the path to your icon file
        self.productsIconButton.setIcon(icon_products)
        self.productsIconButton.setIconSize(self.productsIconButton.size())  # Use button's size as icon size

        self.productsLayout.addWidget(self.productsIconButton)

        # Products Label
        self.productsLabel = QtWidgets.QLabel(self.productsContainer)
        self.productsLabel.setObjectName("sideLabel")
        self.productsLabel.setFixedHeight(50)  # Set a fixed height
        self.productsLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.productsLayout.addWidget(self.productsLabel)

        # Add products container to the sidebar
        self.verticalLayout.addWidget(self.productsContainer)

        # Add a spacer item to push labels to the top and extend sidebar to full height
        self.verticalLayout.addSpacerItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Add sidebar to the main layout
        self.horizontalLayout.addWidget(self.sidebar)

        # Stacked Widget
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.homeLabel.setText(_translate("MainWindow", "Home"))
        self.createBillLabel.setText(_translate("MainWindow", "Create Bill"))
        self.documentLabel.setText(_translate("MainWindow", "Documents"))
        self.customersLabel.setText(_translate("MainWindow", "Customers"))
        self.workersLabel.setText(_translate("MainWindow", "Workers"))

        self.productsLabel.setText(_translate("MainWindow", "Products"))
