from PyQt5 import QtCore, QtGui, QtWidgets
from app.widgets.pdf_viewer_widget import PDFViewerWidget
from app.models.app_models import Worker, session
from app.models.app_models import Anreden, Lander, Einheiten, Zahlungsarten , Nummernvergabe , billSettings

class Ui_CreateBillPage(object):
    def setupUi(self, CreateBillPage):
        CreateBillPage.setObjectName("CreateBillPage")
        CreateBillPage.resize(820, 600)

        # Main layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(CreateBillPage)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Left half: Inputs and buttons
        self.leftWidget = QtWidgets.QWidget(CreateBillPage)
        self.leftWidget.setMaximumWidth(820)  # Set minimum width for the left widget

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

        # Betreff and Datum (in the same line)
        self.betreffDatumLayout = QtWidgets.QHBoxLayout()

        self.betreffLabel = QtWidgets.QLabel("Betreff")
        self.betreffInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.betreffDatumLayout.addWidget(self.betreffLabel)
        self.betreffDatumLayout.addWidget(self.betreffInput)

        self.datumLabel = QtWidgets.QLabel("Datum")
        self.datumInput = QtWidgets.QDateEdit(self.allgemeinPage)
        self.datumInput.setCalendarPopup(True)
        self.datumInput.setMinimumWidth(100) 

        self.betreffDatumLayout.addWidget(self.datumLabel)
        self.betreffDatumLayout.addWidget(self.datumInput)

        self.allgemeinLayout.addLayout(self.betreffDatumLayout)

        # Leistungszeitraum
        self.leistungszeitraumLayout = QtWidgets.QHBoxLayout()
        self.leistungszeitraumLabel = QtWidgets.QLabel("Leistungszeitraum")
        self.leistungszeitraumInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.leistungszeitraumLayout.addWidget(self.leistungszeitraumLabel)
        self.leistungszeitraumLayout.addWidget(self.leistungszeitraumInput)
        self.allgemeinLayout.addLayout(self.leistungszeitraumLayout)

        # Referenz
        self.referenzLayout = QtWidgets.QHBoxLayout()
        self.referenzLabel = QtWidgets.QLabel("Referenz")
        self.referenzInput = QtWidgets.QLineEdit(self.allgemeinPage)
        self.referenzLayout.addWidget(self.referenzLabel)
        self.referenzLayout.addWidget(self.referenzInput)
        self.allgemeinLayout.addLayout(self.referenzLayout)


        # Bearbeiter and Preise sind (Netto/Brutto)
        self.bearbeiterLayout = QtWidgets.QHBoxLayout()
        self.bearbeiterLayout.setSpacing(10)  # Optional: Adjust spacing between containers

        # Container 1: Bearbeiter Label and Select (left-aligned)
        self.bearbeiterContainerLayout = QtWidgets.QHBoxLayout()
        self.bearbeiterLabel = QtWidgets.QLabel("Bearbeiter")
        self.bearbeiterSelect = QtWidgets.QComboBox(self.allgemeinPage)

        worker_names = [worker.worker for worker in session.query(Worker).all()]
        # Populate the combo box with all worker names at once
        self.bearbeiterSelect.addItems(worker_names)       
         
        self.bearbeiterSelect.setMinimumWidth(150) 

        self.bearbeiterContainerLayout.addWidget(self.bearbeiterLabel)
        self.bearbeiterContainerLayout.addWidget(self.bearbeiterSelect)

        # Align the container to the leftmost side
        self.bearbeiterLayout.addLayout(self.bearbeiterContainerLayout)
        self.bearbeiterLayout.addItem(QtWidgets.QSpacerItem(60, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        # Container 2: Preise sind Label and Radio Buttons (right-aligned)
        self.preiseContainerLayout = QtWidgets.QHBoxLayout()
        self.preiseSindLabel = QtWidgets.QLabel("Preise sind:")
        self.nettoRadioButton = QtWidgets.QRadioButton("Netto", self.allgemeinPage)
        self.bruttoRadioButton = QtWidgets.QRadioButton("Brutto", self.allgemeinPage)
        self.preiseContainerLayout.addWidget(self.preiseSindLabel)
        self.preiseContainerLayout.addWidget(self.nettoRadioButton)
        self.preiseContainerLayout.addWidget(self.bruttoRadioButton)

        # Align the container to the rightmost side
        self.bearbeiterLayout.addLayout(self.preiseContainerLayout)

        # Add the main bearbeiterLayout to the allgemeinLayout
        self.allgemeinLayout.addLayout(self.bearbeiterLayout)

        self.inputsStackedWidget.addWidget(self.allgemeinPage)



        self.addAllgemeinButton = QtWidgets.QPushButton("Hinzufügen", self.allgemeinPage)
        self.addAllgemeinButton.setObjectName("addAllgemeinButton")
        self.addAllgemeinButton.setStyleSheet("background-color: #6887b6;")
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
        self.anredeUIDLayout.addWidget(self.anredeLabel)
        self.anredeUIDLayout.addWidget(self.anredeSelect)
        anrede_options = [anrede.gender for anrede in session.query(Anreden).all()]
        self.anredeSelect.addItems(anrede_options)

        self.uidNrLabel = QtWidgets.QLabel("UID-NR")
        self.uidNrInput = QtWidgets.QLineEdit(self.kundePage)
        self.anredeUIDLayout.addWidget(self.uidNrLabel)
        self.anredeUIDLayout.addWidget(self.uidNrInput)
        
        self.kundeLayout.addLayout(self.anredeUIDLayout)

        # 2nd Row: Kunde and Keine MwSt (Checkbox)
        self.kundeMwstLayout = QtWidgets.QHBoxLayout()
        
        self.kundeLabel = QtWidgets.QLabel("Kunde")
        self.kundeInput = QtWidgets.QLineEdit(self.kundePage)
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

        self.contactLayout.addWidget(self.kontaktpersonLabel)
        self.contactLayout.addWidget(self.kontaktpersonInput)

        self.telefonLabel = QtWidgets.QLabel("Telefon")
        self.telefonInput = QtWidgets.QLineEdit(self.kundePage)

        self.contactLayout.addWidget(self.telefonLabel)
        self.contactLayout.addWidget(self.telefonInput)

        self.kundeLayout.addLayout(self.contactLayout)

        # 4th Row: Adresse and Lieferadresse
        self.adresseLieferadresseLayout = QtWidgets.QHBoxLayout()

        self.adresseLabel = QtWidgets.QLabel("Adresse")
        self.adresseInput = QtWidgets.QLineEdit(self.kundePage)
        self.adresseLieferadresseLayout.addWidget(self.adresseLabel)
        self.adresseLieferadresseLayout.addWidget(self.adresseInput)

        self.lieferadresseLabel = QtWidgets.QLabel("Lieferadresse")
        self.lieferadresseInput = QtWidgets.QLineEdit(self.kundePage)
        self.adresseLieferadresseLayout.addWidget(self.lieferadresseLabel)
        self.adresseLieferadresseLayout.addWidget(self.lieferadresseInput)

        self.kundeLayout.addLayout(self.adresseLieferadresseLayout)

        # 5th Row: PLZ and Ort
        self.plzOrtLayout = QtWidgets.QHBoxLayout()

        self.plzLabel = QtWidgets.QLabel("PLZ")
        self.plzInput = QtWidgets.QLineEdit(self.kundePage)
        self.plzOrtLayout.addWidget(self.plzLabel)
        self.plzOrtLayout.addWidget(self.plzInput)

        self.ortLabel = QtWidgets.QLabel("Ort")
        self.ortInput = QtWidgets.QLineEdit(self.kundePage)
        self.plzOrtLayout.addWidget(self.ortLabel)
        self.plzOrtLayout.addWidget(self.ortInput)

        self.kundeLayout.addLayout(self.plzOrtLayout)

        # 6th Row: Land (select menu)
        self.landLabel = QtWidgets.QLabel("Land")
        self.landSelect = QtWidgets.QComboBox(self.kundePage)
        lander_options = [land.land for land in session.query(Lander).all()]
        self.landSelect.addItems(lander_options)
        # self.landSelect.setMaximumWidth(150)

        self.kundeLayout.addWidget(self.landLabel)
        self.kundeLayout.addWidget(self.landSelect)

        # Table for Customers (connected to DB)
        self.kundeContainer = QtWidgets.QWidget(self.kundePage)
        self.kundeContainer.setObjectName("kundeContainer")
        self.kundeContainerLayout = QtWidgets.QVBoxLayout(self.kundeContainer)
        self.kundeContainerLayout.setContentsMargins(10, 120, 10, 10)
        self.kundeContainerLayout.setSpacing(10)  # Remove space between elements
        self.kundeContainerLayout.setAlignment(QtCore.Qt.AlignTop)

       # --- Styled search container for Customer ---
        self.kundeSearchContainer = QtWidgets.QWidget(self.kundeContainer)
        self.kundeSearchContainer.setFixedHeight(60)
        self.kundeSearchContainer.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)
        self.kundeSearchContainerLayout = QtWidgets.QHBoxLayout(self.kundeSearchContainer)
        self.kundeSearchContainerLayout.setContentsMargins(12, 6, 12, 6)
        self.kundeSearchContainerLayout.setSpacing(8)

        # Search icon
        searchIconLabel = QtWidgets.QLabel()
        searchIconLabel.setFixedSize(28, 28)
        searchIconLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Load icon
        iconPath = "resources/icons/search_blue.png"
        pixmap = QtGui.QPixmap(iconPath)

        if pixmap.isNull():
            import os
            absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), iconPath)
            pixmap = QtGui.QPixmap(absolute_path)

        if pixmap.isNull():
            searchIconLabel.setText("🔍")
            searchIconLabel.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 16px;
                    background: transparent;
                }
            """)
        else:
            scaledPixmap = QtGui.QPixmap(22, 22)
            scaledPixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(scaledPixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.drawPixmap(
                0, 0, 22, 22,
                pixmap.scaled(22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            painter.end()
            searchIconLabel.setPixmap(scaledPixmap)

        searchIconLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)

        self.kundeSearchContainerLayout.addWidget(searchIconLabel)
        self.kundeSearchContainerLayout.addSpacing(8)

        # Styled customer search input
        self.kundeSearchInput = QtWidgets.QLineEdit()
        self.kundeSearchInput.setPlaceholderText("Search Customer Name")
        self.kundeSearchInput.setObjectName("kundeSearch")
        self.kundeSearchInput.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                outline: none;
            }
        """)
        self.kundeSearchInput.setMinimumWidth(400)
        self.kundeSearchContainerLayout.addWidget(self.kundeSearchInput, 1)

        # Add the full container to the layout
        self.kundeContainerLayout.addWidget(self.kundeSearchContainer)

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
        self.addKundeEntityButton.setFixedHeight(40)
        # self.addKundeEntityButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addKundeEntityButton.setText("hinzufügen")
        self.kundeButtonsHorizontalLayout.addWidget(self.addKundeEntityButton)
        
        self.removeKundeLastRowButton = QtWidgets.QPushButton(self.kundeContainer)
        self.removeKundeLastRowButton.setFixedHeight(40)
        # self.removeKundeLastRowButton.setIcon(QtGui.QIcon('resources/icons/x.png'))
        self.removeKundeLastRowButton.setText("Klare Eingaben")
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
        self.kapitelUnterkapitelLayout.addWidget(self.kapitelLabel)
        self.kapitelUnterkapitelLayout.addWidget(self.kapitelInput)

        self.unterkapitelLabel = QtWidgets.QLabel("Unterkapitel")
        self.unterkapitelInput = QtWidgets.QLineEdit(self.inputsSection)
        self.kapitelUnterkapitelLayout.addWidget(self.unterkapitelLabel)
        self.kapitelUnterkapitelLayout.addWidget(self.unterkapitelInput)
        self.inputsSectionLayout.addLayout(self.kapitelUnterkapitelLayout)

        # Preis netto and Rabatt in %
        self.preisRabattLayout = QtWidgets.QHBoxLayout()
        
        # New Name Input Added Here
        self.artikelNameLabel = QtWidgets.QLabel("Name")
        self.artikelNameInput = QtWidgets.QLineEdit(self.inputsSection)
        self.preisRabattLayout.addWidget(self.artikelNameLabel)
        self.preisRabattLayout.addWidget(self.artikelNameInput)

        # Existing Preis netto Input
        self.preisNettoLabel = QtWidgets.QLabel("Preis netto")
        self.preisNettoInput = QtWidgets.QLineEdit(self.inputsSection)
        self.preisRabattLayout.addWidget(self.preisNettoLabel)
        self.preisRabattLayout.addWidget(self.preisNettoInput)

        # Existing Rabatt in % Input
        self.rabattLabel = QtWidgets.QLabel("Rabatt in %")
        self.rabattInput = QtWidgets.QLineEdit(self.inputsSection)
        self.preisRabattLayout.addWidget(self.rabattLabel)
        self.preisRabattLayout.addWidget(self.rabattInput)
        self.inputsSectionLayout.addLayout(self.preisRabattLayout)

        # Menge, Einheit, MwSt. in %, Summe Netto
        self.mengeEinheitLayout = QtWidgets.QHBoxLayout()
        
        self.mengeLabel = QtWidgets.QLabel("Menge")
        self.mengeInput = QtWidgets.QLineEdit(self.inputsSection)
        self.mengeInput.setText("1")
        self.mengeEinheitLayout.addWidget(self.mengeLabel)
        self.mengeEinheitLayout.addWidget(self.mengeInput)

        # Einheit (converted to select)
        self.einheitLabel = QtWidgets.QLabel("Einheit")
        self.einheitSelect = QtWidgets.QComboBox(self.inputsSection)
        self.einheitSelect.setPlaceholderText("Wählen Sie eine Einheit")
        # Populate Einheit select options directly
        einheiten = session.query(Einheiten).all()
        self.einheitSelect.clear()
        for einheit in einheiten:
            self.einheitSelect.addItem(einheit.unit, einheit.id)  # Assuming Einheiten has 'name' and 'id' fields
        self.mengeEinheitLayout.addWidget(self.einheitLabel)
        self.mengeEinheitLayout.addWidget(self.einheitSelect)

        # MwSt (fetch from billSettings)
        self.mwstLabel = QtWidgets.QLabel("MwSt. in %")
        self.mwstInput = QtWidgets.QLineEdit(self.inputsSection)
        # Populate MwSt input directly
        settings = session.query(billSettings).first()
        if settings:
            self.mwstInput.setText(f"{settings.VAT} %")
            self.mwstInput.setReadOnly(True)
        self.mengeEinheitLayout.addWidget(self.mwstLabel)
        self.mengeEinheitLayout.addWidget(self.mwstInput)

        self.summeNettoLabel = QtWidgets.QLabel("Summe Netto")
        self.summeNettoInput = QtWidgets.QLineEdit(self.inputsSection)
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

        # --- Styled search container for Produkt (Artikel) ---
        self.artikelSearchContainer = QtWidgets.QWidget(self.artikelContainer)
        self.artikelSearchContainer.setFixedHeight(60)
        self.artikelSearchContainer.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)
        self.artikelSearchContainerLayout = QtWidgets.QHBoxLayout(self.artikelSearchContainer)
        self.artikelSearchContainerLayout.setContentsMargins(12, 6, 12, 6)
        self.artikelSearchContainerLayout.setSpacing(8)

        # Search icon
        searchIconLabelArtikel = QtWidgets.QLabel()
        searchIconLabelArtikel.setFixedSize(28, 28)
        searchIconLabelArtikel.setAlignment(QtCore.Qt.AlignCenter)

        # Load icon
        iconPath = "resources/icons/search_blue.png"
        pixmap = QtGui.QPixmap(iconPath)

        if pixmap.isNull():
            import os
            absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), iconPath)
            pixmap = QtGui.QPixmap(absolute_path)

        if pixmap.isNull():
            searchIconLabelArtikel.setText("🔍")
            searchIconLabelArtikel.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 16px;
                    background: transparent;
                }
            """)
        else:
            scaledPixmap = QtGui.QPixmap(22, 22)
            scaledPixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(scaledPixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.drawPixmap(
                0, 0, 22, 22,
                pixmap.scaled(22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            painter.end()
            searchIconLabelArtikel.setPixmap(scaledPixmap)

        searchIconLabelArtikel.setStyleSheet("""
            QLabel {
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)

        self.artikelSearchContainerLayout.addWidget(searchIconLabelArtikel)
        self.artikelSearchContainerLayout.addSpacing(8)

        # Styled artikel search input
        self.artikelSearchInput = QtWidgets.QLineEdit()
        self.artikelSearchInput.setPlaceholderText("Produkt suchen")
        self.artikelSearchInput.setObjectName("artikelSearch")
        self.artikelSearchInput.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                border-radius: 12px;
                padding: 8px 12px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                outline: none;
            }
        """)
        self.artikelSearchInput.setMinimumWidth(400)
        self.artikelSearchContainerLayout.addWidget(self.artikelSearchInput, 1)

        # Add the full container to the layout
        self.artikelContainerLayout.addWidget(self.artikelSearchContainer)
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
        # self.addEntityButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addEntityButton.setFixedHeight(40)
        self.addEntityButton.setText("hinzufügen")
        self.buttonsHorizontalLayout.addWidget(self.addEntityButton)
        
        self.removeLastRowButton = QtWidgets.QPushButton(self.artikelContainer)
        self.removeLastRowButton.setFixedHeight(40)

        # self.removeLastRowButton.setIcon(QtGui.QIcon('resources/icons/x.png'))
        self.removeLastRowButton.setText("Rückgängig")
        self.buttonsHorizontalLayout.addWidget(self.removeLastRowButton)
        

        # # Add this code in the setupUi method of Ui_CreateBillPage
        # self.addBatchButton = QtWidgets.QPushButton(self.artikelContainer)
        # self.addBatchButton.setFixedHeight(40)
        # # self.addBatchButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        # self.addBatchButton.setText("viele Produkte hinzufügen")
        # self.buttonsHorizontalLayout.addWidget(self.addBatchButton)  # Assuming verticalLayout contains buttons


        self.artikelContainerLayout.addLayout(self.buttonsHorizontalLayout)

        self.artikelLayout.addWidget(self.artikelContainer)
        self.inputsStackedWidget.addWidget(self.artikelPage)

        # # Create a horizontal layout for the buttons
        # self.buttonLayout = QtWidgets.QHBoxLayout()

        # # Create a horizontal layout for buttons
        # self.buttonLayout = QtWidgets.QHBoxLayout()

        # # Export button
        # self.exportButton = QtWidgets.QPushButton("Als PDF exportieren", self.leftWidget)
        # self.exportButton.setObjectName("exportButton")
        # self.exportButton.setStyleSheet("background-color: #6887b6; ")
        # self.buttonLayout.addWidget(self.exportButton)

        # # Save order button
        # self.saveOrderButton = QtWidgets.QPushButton("Speichern", self.leftWidget)
        # self.saveOrderButton.setObjectName("saveOrderButton")
        # self.saveOrderButton.setStyleSheet("background-color: #6887b6;")
        # self.buttonLayout.addWidget(self.saveOrderButton)

        # # Print button
        # self.printButton = QtWidgets.QPushButton("Drucken", self.leftWidget)
        # self.printButton.setObjectName("printButton")
        # self.printButton.setStyleSheet("background-color: #6887b6;")
        # self.buttonLayout.addWidget(self.printButton)

        # # Add the horizontal button layout to the main vertical layout
        # self.leftLayout.addLayout(self.buttonLayout)

         # Add left widget to the main horizontal layout
        self.horizontalLayout.addWidget(self.leftWidget)


        # Right half: Create a container widget for the PDF viewer and buttons
        self.rightContainer = QtWidgets.QWidget(CreateBillPage)
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightContainer)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)  # Set left, top, right, bottom margins

        # PDF viewer container
        self.pdfViewerContainer = QtWidgets.QWidget(self.rightContainer)
        self.pdfViewerLayout = QtWidgets.QVBoxLayout(self.pdfViewerContainer)
        self.pdfViewer = PDFViewerWidget(self.pdfViewerContainer)
        self.pdfViewerLayout.addWidget(self.pdfViewer)
        self.rightLayout.addWidget(self.pdfViewerContainer)

        # Buttons container
        self.rightButtonsContainer = QtWidgets.QWidget(self.rightContainer)
        self.rightButtonsLayout = QtWidgets.QHBoxLayout(self.rightButtonsContainer)  # Changed to QHBoxLayout



        # Batch button (icon only, square, with background color)
        self.batchButton = QtWidgets.QPushButton(self.rightButtonsContainer)
        self.batchButton.setObjectName("batchButton")

        self.batchButton.setIcon(QtGui.QIcon("resources/icons/plus_circle.png"))
        self.batchButton.setIconSize(QtCore.QSize(46, 46))  # Set the icon size
        self.batchButton.setFixedSize(50, 50)  # Set the button size (square)

        # Hover effect
        self.batchButton.setStyleSheet("""
            QPushButton {
            background-color: #6887b6;
            border-radius: 15px;
            }
            QPushButton:hover {
            background-color: #506c8e;  /* Slightly darker shade for hover */
            }
        """)

        self.rightButtonsLayout.addWidget(self.batchButton)
        self.batchButton.hide()  # Hide by default

        # Show/hide batchButton depending on the current tab
        def update_batch_button_visibility(index):
            # index 2 is artikelPage (assuming order: 0=allgemein, 1=kunde, 2=artikel)
            self.batchButton.setVisible(index == 2)

        self.inputsStackedWidget.currentChanged.connect(update_batch_button_visibility)
        # Set initial visibility
        update_batch_button_visibility(self.inputsStackedWidget.currentIndex())


        # Export button (icon only, square, with background color)
        self.exportButton = QtWidgets.QPushButton(self.rightButtonsContainer)
        self.exportButton.setObjectName("exportButton")

        self.exportButton.setIcon(QtGui.QIcon("resources/icons/save_pdf.png"))
        self.exportButton.setIconSize(QtCore.QSize(46, 46))  # Set the icon size
        self.exportButton.setFixedSize(50, 50)  # Set the button size (square)

        # Hover effect
        self.exportButton.setStyleSheet("""
            QPushButton {
                background-color: #6887b6;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #506c8e;  /* Slightly darker shade for hover */
            }
        """)

        self.rightButtonsLayout.addWidget(self.exportButton)

        # Save order button (icon only, square, with background color)
        self.saveOrderButton = QtWidgets.QPushButton(self.rightButtonsContainer)
        self.saveOrderButton.setObjectName("saveOrderButton")

        self.saveOrderButton.setIcon(QtGui.QIcon("resources/icons/save.png"))
        self.saveOrderButton.setIconSize(QtCore.QSize(43, 43))  # Set the icon size
        self.saveOrderButton.setFixedSize(50, 50)  # Set the button size (square)

        # Hover effect
        self.saveOrderButton.setStyleSheet("""
            QPushButton {
                background-color: #6887b6;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #506c8e;  /* Slightly darker shade for hover */
            }
        """)

        self.rightButtonsLayout.addWidget(self.saveOrderButton)

        # Print button (icon only, square, with background color)
        self.printButton = QtWidgets.QPushButton(self.rightButtonsContainer)
        self.printButton.setObjectName("printButton")

        self.printButton.setIcon(QtGui.QIcon("resources/icons/print.png"))
        self.printButton.setIconSize(QtCore.QSize(48, 48))  # Set the icon size
        self.printButton.setFixedSize(50, 50)  # Set the button size (square)

        # Hover effect
        self.printButton.setStyleSheet("""
            QPushButton {
                background-color: #6887b6;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #506c8e;  /* Slightly darker shade for hover */
            }
        """)

        self.rightButtonsLayout.addWidget(self.printButton)


        # Center the buttons by setting alignment for the layout
        self.rightButtonsLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Add buttons container to the right layout
        self.rightLayout.addWidget(self.rightButtonsContainer)

        # Add right container to the main layout
        self.horizontalLayout.addWidget(self.rightContainer)

        self.retranslateUi(CreateBillPage)
        QtCore.QMetaObject.connectSlotsByName(CreateBillPage)

    def retranslateUi(self, CreateBillPage):
        _translate = QtCore.QCoreApplication.translate
        CreateBillPage.setWindowTitle(_translate("CreateBillPage", "Create Bill Page"))
