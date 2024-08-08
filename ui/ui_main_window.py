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

        # Container widget for home icon and label
        self.homeContainer = QtWidgets.QWidget(self.sidebar)
        self.homeContainer.setObjectName("homeContainer")
        
        # Horizontal layout for home icon and label
        self.homeLayout = QtWidgets.QHBoxLayout(self.homeContainer)
        self.homeLayout.setContentsMargins(10, 0, 0, 0)
        self.homeLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.homeLayout.setObjectName("homeLayout")
        self.homeLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Home Icon button
        self.homeIconButton = QtWidgets.QPushButton(self.homeContainer)
        self.homeIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.homeIconButton.setObjectName("homeIconButton")
        icon_home = QtGui.QIcon("resources/icons/home.png")  # Set the path to your icon file
        self.homeIconButton.setIcon(icon_home)
        self.homeIconButton.setIconSize(self.homeIconButton.size())  # Use button's size as icon size
        self.homeLayout.addWidget(self.homeIconButton)

        # Home Label
        self.homeLabel = QtWidgets.QLabel(self.homeContainer)
        self.homeLabel.setObjectName("homeLabel")
        self.homeLabel.setFixedHeight(50)  # Set a fixed height
        self.homeLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.homeLayout.addWidget(self.homeLabel)

        # Add home container to the sidebar
        self.verticalLayout.addWidget(self.homeContainer)

        # Add margin between home and create bill containers
        self.verticalLayout.addSpacing(4)  # Add spacing between containers

        # Container widget for create bill icon and label
        self.createBillContainer = QtWidgets.QWidget(self.sidebar)
        self.createBillContainer.setObjectName("createBillContainer")
        
        # Horizontal layout for create bill icon and label
        self.createBillLayout = QtWidgets.QHBoxLayout(self.createBillContainer)
        self.createBillLayout.setContentsMargins(10, 0, 0, 0)
        self.createBillLayout.setSpacing(1)  # Adjust spacing to bring icon and label closer
        self.createBillLayout.setObjectName("createBillLayout")
        self.createBillLayout.setAlignment(QtCore.Qt.AlignCenter)  # Center the content

        # Create Bill Icon button
        self.createBillIconButton = QtWidgets.QPushButton(self.createBillContainer)
        self.createBillIconButton.setFixedSize(20, 20)  # Set the size of the icon button
        self.createBillIconButton.setObjectName("createBillIconButton")
        icon_create_bill = QtGui.QIcon("resources/icons/bill.png")  # Set the path to your icon file
        self.createBillIconButton.setIcon(icon_create_bill)
        self.createBillIconButton.setIconSize(self.createBillIconButton.size())  # Use button's size as icon size
        self.createBillLayout.addWidget(self.createBillIconButton)

        # Create Bill Label
        self.createBillLabel = QtWidgets.QLabel(self.createBillContainer)
        self.createBillLabel.setObjectName("createBillLabel")
        self.createBillLabel.setFixedHeight(50)  # Set a fixed height
        self.createBillLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.createBillLayout.addWidget(self.createBillLabel)

        # Add create bill container to the sidebar
        self.verticalLayout.addWidget(self.createBillContainer)

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