from PyQt5 import QtWidgets, QtCore, QtGui
from app.models.app_models import Product, session


class CartItemWidget(QtWidgets.QWidget):
    def __init__(self, product, quantity, onRemove, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            CartItemWidget {
                background-color: white;
                border-radius: 8px;
                margin: 4px;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        # Main layout with proper spacing
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)
        
        # Left side: Product info container
        infoContainer = QtWidgets.QWidget()
        infoLayout = QtWidgets.QVBoxLayout(infoContainer)
        infoLayout.setContentsMargins(0, 0, 0, 0)
        infoLayout.setSpacing(2)
        
        # Product name with quantity
        nameLabel = QtWidgets.QLabel(f"{quantity}x {product.produkt}")
        nameLabel.setFont(QtGui.QFont("Poppins", 11, QtGui.QFont.Bold))
        nameLabel.setWordWrap(True)
        infoLayout.addWidget(nameLabel)
        
        layout.addWidget(infoContainer, 1)
        
        # Right side: Price container
        priceContainer = QtWidgets.QWidget()
        priceLayout = QtWidgets.QVBoxLayout(priceContainer)
        priceLayout.setContentsMargins(0, 0, 0, 0)
        priceLayout.setSpacing(2)
        priceLayout.setAlignment(QtCore.Qt.AlignRight)
        
        # Unit price
        unitPriceLabel = QtWidgets.QLabel(f"{product.verkaufspreis:.2f} €")
        unitPriceLabel.setAlignment(QtCore.Qt.AlignRight)
        unitPriceLabel.setFont(QtGui.QFont("Poppins", 10))
        priceLayout.addWidget(unitPriceLabel)
        
        # Total price
        totalPrice = product.verkaufspreis * quantity
        totalPriceLabel = QtWidgets.QLabel(f"Summe: {totalPrice:.2f} €")
        totalPriceLabel.setAlignment(QtCore.Qt.AlignRight)
        totalPriceLabel.setStyleSheet("color: #666;")
        totalPriceLabel.setFont(QtGui.QFont("Poppins", 9))
        priceLayout.addWidget(totalPriceLabel)
        
        layout.addWidget(priceContainer)
        
        # Add spacing before remove button
        layout.addSpacing(15)
        
        # Modern remove button
        removeButton = QtWidgets.QPushButton("✕")
        removeButton.setFixedSize(40, 40)
        removeButton.setCursor(QtCore.Qt.PointingHandCursor)  # Change cursor on hover
        removeButton.setStyleSheet("""
            QPushButton {
                background-color: #FF4C4C;
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding: 0;
                margin: 0;
                text-align: center;
                line-height: 40px;
                box-shadow: 0 2px 4px rgba(255, 76, 76, 0.3);
            }
            QPushButton:hover {
                background-color: #ff6666;
                box-shadow: 0 4px 8px rgba(255, 76, 76, 0.4);
            }
            QPushButton:pressed {
                background-color: #ff3333;
                box-shadow: 0 1px 2px rgba(255, 76, 76, 0.3);
            }
        """)
        removeButton.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        removeButton.clicked.connect(onRemove)
        layout.addWidget(removeButton)
        
        # Set size policies for responsive behavior
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred
        )


class CasherPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cartItems = {}  # Store as {product: (quantity, card, quantityInput)}
        self.initUI()



    def initUI(self):
        # Main layout
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setSpacing(0)  # Remove spacing between left and right containers

        # Left side: Search bar, product count, product display
        self.leftContainer = QtWidgets.QWidget()  # Container for the left layout
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftContainer)
        self.leftContainer.setStyleSheet("background-color: #f6f6f6;")
        self.leftLayout.setContentsMargins(20, 20, 20, 20)  # Add padding around the content

        # Search container with modern design
        self.searchContainer = QtWidgets.QWidget()
        self.searchContainer.setFixedHeight(60)
        self.searchContainer.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)
        self.searchContainerLayout = QtWidgets.QHBoxLayout(self.searchContainer)
        self.searchContainerLayout.setContentsMargins(12, 6, 12, 6)  # Reduced vertical padding
        self.searchContainerLayout.setSpacing(8)

        # Search icon with proper loading and display
        searchIconLabel = QtWidgets.QLabel()
        searchIconLabel.setFixedSize(28, 28)
        searchIconLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        # First try relative path
        iconPath = "resources/icons/search_blue.png"
        pixmap = QtGui.QPixmap(iconPath)
        
        # If relative path fails, try absolute path
        if pixmap.isNull():
            import os
            absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), iconPath)
            print(f"Versuche absoluten Pfad: {absolute_path}")
            pixmap = QtGui.QPixmap(absolute_path)

        if pixmap.isNull():
            print(f"❌ Icon konnte nicht geladen werden: {iconPath}")
            searchIconLabel.setText("🔍")  # Fallback: Unicode search icon
            searchIconLabel.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 16px;
                    background: transparent;
                }
            """)
        else:
            print(f"✅ Icon geladen: {pixmap.width()}x{pixmap.height()} Pixel")
            # Create a new pixmap with transparent background
            scaledPixmap = QtGui.QPixmap(22, 22)
            scaledPixmap.fill(QtCore.Qt.transparent)
            
            # Create painter for high-quality scaling
            painter = QtGui.QPainter(scaledPixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            
            # Draw the scaled image
            painter.drawPixmap(
                0, 0, 22, 22,
                pixmap.scaled(22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
            painter.end()
            
            # Set the final pixmap
            searchIconLabel.setPixmap(scaledPixmap)
            print(f"✅ Icon skaliert auf: {scaledPixmap.width()}x{scaledPixmap.height()} Pixel")

        # Ensure transparent background
        searchIconLabel.setStyleSheet("""
            QLabel {
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        
        self.searchContainerLayout.addWidget(searchIconLabel)

        # Add spacing after icon
        self.searchContainerLayout.addSpacing(8)

        # Modern search bar with adjusted styling
        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setPlaceholderText("Search products...")
        self.searchBar.textChanged.connect(self.filterProducts)
        self.searchBar.setStyleSheet("""
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
        self.searchBar.setMinimumWidth(400)
        self.searchContainerLayout.addWidget(self.searchBar, 1)  # Add stretch factor

        # Product count label with adjusted styling
        self.productCountLabel = QtWidgets.QLabel("Gesamtprodukte: 0")
        self.productCountLabel.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.searchContainerLayout.addWidget(self.productCountLabel)

        # Products container (scroll area for displaying products)
        self.productsScroll = QtWidgets.QScrollArea(self)
        self.productsContainer = QtWidgets.QWidget()
        self.productsLayout = QtWidgets.QGridLayout(self.productsContainer)
        self.productsLayout.setSpacing(20)  # Increase vertical space between cards
        self.productsScroll.setWidget(self.productsContainer)
        self.productsScroll.setWidgetResizable(True)
        self.productsScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.productsScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.productsScroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QWidget#scrollAreaWidgetContents {
                background: transparent;
            }
        """)

        # Add to left layout
        self.leftLayout.addWidget(self.searchContainer)
        self.leftLayout.addWidget(self.productsScroll)

        # Right side: Cart and sum total
        self.cartContainer = QtWidgets.QWidget()
        self.cartLayout = QtWidgets.QVBoxLayout(self.cartContainer)
        self.cartContainer.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-radius: 12px;
            }
        """)
        self.cartLayout.setContentsMargins(16, 16, 16, 16)
        self.cartLayout.setSpacing(12)

        # Cart header
        self.cartLabel = QtWidgets.QLabel("Warenkorb", self)
        self.cartLabel.setStyleSheet("color: #333; font-weight: bold; font-size: 18px; background: transparent;")
        self.cartLayout.addWidget(self.cartLabel)

        # Cart items scroll area
        self.cartScrollArea = QtWidgets.QScrollArea()
        self.cartScrollArea.setWidgetResizable(True)
        self.cartScrollArea.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
            }
        """)

        self.cartItemsWidget = QtWidgets.QWidget()
        self.cartListLayout = QtWidgets.QVBoxLayout(self.cartItemsWidget)
        self.cartListLayout.setSpacing(8)
        self.cartListLayout.setAlignment(QtCore.Qt.AlignTop)
        self.cartScrollArea.setWidget(self.cartItemsWidget)
        
        self.cartLayout.addWidget(self.cartScrollArea)

        # Totals section
        self.addTotalInfo()

        # Add left and right layouts to main layout with stretch factors
        self.mainLayout.addWidget(self.leftContainer, stretch=3)  # Left container with more space
        self.mainLayout.addWidget(self.cartContainer, stretch=1)  # Cart container with less space

        self.loadProducts()

    def addTotalInfo(self):
        # Totals container
        totalsWidget = QtWidgets.QWidget()
        totalsLayout = QtWidgets.QVBoxLayout(totalsWidget)
        totalsLayout.setSpacing(8)
        
        # Total labels with German formatting
        self.subTotalLabel = QtWidgets.QLabel("Netto: 0,00 €")
        self.taxLabel = QtWidgets.QLabel("10% MwSt: 0,00 €")
        self.totalLabel = QtWidgets.QLabel("Summe: 0,00 €")
        
        for label in [self.subTotalLabel, self.taxLabel, self.totalLabel]:
            label.setFont(QtGui.QFont("Poppins", 11, QtGui.QFont.Bold))
            label.setStyleSheet("color: #333; background: transparent;")
            totalsLayout.addWidget(label)
        
        self.cartLayout.addWidget(totalsWidget)
        
        # Action buttons
        self.discountButton = QtWidgets.QPushButton("Rabatt in %")
        self.discountButton.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
        """)
        
        self.payButton = QtWidgets.QPushButton("Bezahlen")
        self.payButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        self.cartLayout.addWidget(self.discountButton)
        self.cartLayout.addWidget(self.payButton)
        
        # Action icons
        iconContainer = QtWidgets.QWidget()
        iconLayout = QtWidgets.QHBoxLayout(iconContainer)
        iconLayout.setAlignment(QtCore.Qt.AlignCenter)
        
        iconButtons = [
            ("pdf.png", "Rechnung"),
            ("email.png", "E-Mail"),
            ("print.png", "Drucken")
        ]
        
        for icon, tooltip in iconButtons:
            btn = QtWidgets.QPushButton()
            btn.setIcon(QtGui.QIcon(f"resources/icons/{icon}"))
            btn.setIconSize(QtCore.QSize(24, 24))
            btn.setFixedSize(40, 40)
            btn.setToolTip(tooltip)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border-radius: 20px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            iconLayout.addWidget(btn)
        
        self.cartLayout.addWidget(iconContainer)

    def loadProducts(self):
        # Load products from the database and display them
        products = session.query(Product).all()
        self.displayProducts(products)
        self.productCountLabel.setText(f"Gesamtprodukte: {len(products)}")

    def displayProducts(self, products):
        # Clear current products
        for i in reversed(range(self.productsLayout.count())):
            widget = self.productsLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Display product cards
        for i, product in enumerate(products):
            productCard = self.createProductCard(product)
            self.productsLayout.addWidget(productCard, i // 3, i % 3)

    def createProductCard(self, product):
        # Card container
        card = QtWidgets.QFrame()
        card.setFixedSize(350, 150)
        card.setStyleSheet("""
            QFrame {
                background-color: #8ba1c2;
                border-radius: 24px;
                border: none;
            }
        """)

        # Main layout
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(30)

        # Left: Icon
        iconLabel = QtWidgets.QLabel()
        iconLabel.setFixedSize(70, 70)
        iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        iconLabel.setStyleSheet("background: transparent;")
        
        # Load and scale icon
        pixmap = QtGui.QPixmap("resources/icons/shopping_cart_checkout2.png")
        if not pixmap.isNull():
            iconLabel.setPixmap(pixmap.scaled(60, 60, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        layout.addWidget(iconLabel)

        # Right: Product details
        detailsLayout = QtWidgets.QVBoxLayout()
        detailsLayout.setSpacing(8)
        detailsLayout.setContentsMargins(0, 0, 0, 0)
        detailsLayout.setAlignment(QtCore.Qt.AlignCenter)

        # Product name with proper font settings
        nameLabel = QtWidgets.QLabel(product.produkt)
        font = QtGui.QFont("Poppins", 14)
        font.setBold(True)
        nameLabel.setFont(font)
        nameLabel.setStyleSheet("""
            QLabel {
                color: black;
                background: none;
                padding: 2px 0;
            }
        """)
        nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        nameLabel.setWordWrap(True)
        nameLabel.setMinimumHeight(40)  # Ensure enough height for two lines
        detailsLayout.addWidget(nameLabel)

        # Price
        priceText = f"Preis: {product.verkaufspreis:.2f}€".replace(".", ",")
        priceLabel = QtWidgets.QLabel(priceText)
        priceLabel.setStyleSheet("""
            QLabel {
                color: black;
                font-family: 'Arial';
                font-size: 13px;
                background: none;
            }
        """)
        priceLabel.setAlignment(QtCore.Qt.AlignCenter)
        detailsLayout.addWidget(priceLabel)

        # Quantity input
        quantityInput = QtWidgets.QSpinBox()
        quantityInput.setRange(1, 100)
        quantityInput.setValue(1)
        quantityInput.setFixedSize(90, 30)
        quantityInput.setAlignment(QtCore.Qt.AlignCenter)
        quantityInput.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: black;
                border: none;
                border-radius: 10px;
                padding: 5px;
                font-family: 'Arial';
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0;
                border: none;
            }
        """)
        detailsLayout.addWidget(quantityInput, 0, QtCore.Qt.AlignCenter)

        # Add details layout directly to main layout
        layout.addLayout(detailsLayout, 1)

        # Click behavior
        def handleClick(event):
            if event.button() == QtCore.Qt.LeftButton:
                if product in self.cartItems:
                    quantity, _, _ = self.cartItems[product]
                    del self.cartItems[product]
                    self.removeFromCart(product)
                    card.setStyleSheet("""
                        QFrame {
                            background-color: #8ba1c2;
                            border-radius: 24px;
                            border: none;
                        }
                    """)
                else:
                    self.cartItems[product] = (quantityInput.value(), card, quantityInput)
                    self.addCartItemWidget(product, quantityInput.value())
                    self.updateTotals()
                    card.setStyleSheet("""
                        QFrame {
                            background-color: #4CAF50;
                            border-radius: 24px;
                            border: none;
                        }
                    """)

        card.mousePressEvent = handleClick

        # Set initial state if in cart
        if product in self.cartItems:
            card.setStyleSheet("""
                QFrame {
                    background-color: #4CAF50;
                    border-radius: 24px;
                    border: none;
                }
            """)

        return card

    def filterProducts(self):
        # Filter products based on search text
        searchText = self.searchBar.text().lower()
        filteredProducts = session.query(Product).filter(Product.produkt.ilike(f"%{searchText}%")).all()
        self.displayProducts(filteredProducts)

    def addToCart(self, product, card, quantity):
        if product in self.cartItems:
            # Remove from cart
            del self.cartItems[product]
            self.removeFromCart(product)
            card.setStyleSheet("""
                QFrame {
                    background-color: #8ba1c2;
                    border-radius: 24px;
                    border: none;
                }
            """)
        else:
            # Add to cart
            self.cartItems[product] = (quantity, card, quantityInput) # type: ignore
            self.addCartItemWidget(product, quantity)
            self.updateTotals()
            card.setStyleSheet("""
                QFrame {
                    background-color: #4CAF50;
                    border-radius: 24px;
                    border: none;
                }
            """)

    def addCartItemWidget(self, product, quantity):
        cartItem = CartItemWidget(
            product,
            quantity,
            lambda: self.removeFromCart(product)
        )
        self.cartListLayout.addWidget(cartItem)

    def removeFromCart(self, product):
        # Remove the product from the cart list
        for i in range(self.cartListLayout.count()):
            itemWidget = self.cartListLayout.itemAt(i).widget()
            if itemWidget:
                nameLabel = itemWidget.findChild(QtWidgets.QLabel)
                if nameLabel and product.produkt in nameLabel.text():
                    itemWidget.setParent(None)
                    break

        # Reset the card color and quantity if product is in cartItems
        if product in self.cartItems:
            quantity, card, quantityInput = self.cartItems[product]
            # Reset card color
            card.setStyleSheet("""
                QFrame {
                    background-color: #8ba1c2;
                    border-radius: 24px;
                    border: none;
                }
            """)
            # Reset quantity to 1
            quantityInput.setValue(1)
            del self.cartItems[product]
        
        self.updateTotals()

    def updateTotals(self):
        # Update subtotal, tax, and total
        subtotal = sum(product.verkaufspreis * quantity for product, (quantity, _, _) in self.cartItems.items())
        tax = subtotal * 0.1  # Example tax rate
        total = subtotal + tax
        
        # Format numbers with German locale (comma as decimal separator)
        self.subTotalLabel.setText(f"Netto: {subtotal:.2f} €".replace(".", ","))
        self.taxLabel.setText(f"10% MwSt: {tax:.2f} €".replace(".", ","))
        self.totalLabel.setText(f"Summe: {total:.2f} €".replace(".", ","))


