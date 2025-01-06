from PyQt5 import QtWidgets, QtCore, QtGui
from app.models.app_models import Product, session


class CasherPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cartItems = {}  # Store cart items as Product instances and quantities
        self.initUI()



    def initUI(self):
        # Main layout
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setSpacing(0)  # Remove spacing between left and right containers

        # Left side: Search bar, product count, product display
        self.leftContainer = QtWidgets.QWidget()  # Container for the left layout
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftContainer)
        self.leftContainer.setStyleSheet("background-color: #f6f6f6;")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins for compact layout

        # Centered Search bar layout with different color
        self.searchContainer = QtWidgets.QWidget(self)
        self.searchContainerLayout = QtWidgets.QHBoxLayout(self.searchContainer)
        self.searchContainer.setStyleSheet("background-color: #282c3c; padding: 5px; border-radius: 1px;")



        self.searchBar = QtWidgets.QLineEdit(self)
        self.searchBar.setPlaceholderText("Search products...")
        self.searchBar.setFixedWidth(300)  # Set a fixed width to avoid stretching too much
        self.searchBar.textChanged.connect(self.filterProducts)
        self.searchBar.setStyleSheet("background-color: #F5F5F5; border-radius: 10px; padding-left: 30px;")  # Add padding for icon

        # Add the search icon and search bar to the search container
        self.searchContainerLayout.addWidget(self.searchBar)
        
        self.productCountLabel = QtWidgets.QLabel("Total Products: 0", self)


        self.searchContainerLayout.addWidget(self.productCountLabel)
        self.searchContainerLayout.setAlignment(QtCore.Qt.AlignCenter)  # Align the search container to center

        # Products container (scroll area for displaying products)
        self.productsScroll = QtWidgets.QScrollArea(self)
        self.productsContainer = QtWidgets.QWidget()
        self.productsLayout = QtWidgets.QGridLayout(self.productsContainer)
        self.productsLayout.setSpacing(20)  # Increase vertical space between cards
        self.productsScroll.setWidget(self.productsContainer)
        self.productsScroll.setWidgetResizable(True)
        self.productsScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # Hide the vertical scrollbar
        self.productsScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar

        # Add to left layout
        self.leftLayout.addWidget(self.searchContainer)  # Add the centered search bar
        self.leftLayout.addWidget(self.productsScroll)

        # Right side: Cart and sum total
        self.cartContainer = QtWidgets.QWidget()  # Container for the cart layout
        self.cartLayout = QtWidgets.QVBoxLayout(self.cartContainer)
        self.cartContainer.setStyleSheet("background-color: #282c3c; border-radius: 1px;")

        self.cartLabel = QtWidgets.QLabel("Cart:", self)
        self.cartLabel.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        self.cartList = QtWidgets.QListWidget(self)
        self.cartList.setStyleSheet("background-color: #282c3c; color: white;")  # Style for cart list

        self.cartLayout.addWidget(self.cartLabel)
        self.cartLayout.addWidget(self.cartList)

        # Add payment button and total information
        self.addTotalInfo()

        # Add left and right layouts to main layout with stretch factors
        self.mainLayout.addWidget(self.leftContainer, stretch=3)  # Left container with more space
        self.mainLayout.addWidget(self.cartContainer, stretch=1)  # Cart container with less space

        self.loadProducts()

    def addTotalInfo(self):
        # Total information and pay button
        self.subTotalLabel = QtWidgets.QLabel("Subtotal: $0.00", self)
        self.subTotalLabel.setStyleSheet("color: white;")
        self.taxLabel = QtWidgets.QLabel("Tax: $0.00", self)
        self.taxLabel.setStyleSheet("color: white;")
        self.totalLabel = QtWidgets.QLabel("Total: $0.00", self)
        self.totalLabel.setStyleSheet("color: white;")

        self.cartLayout.addWidget(self.subTotalLabel)
        self.cartLayout.addWidget(self.taxLabel)
        self.cartLayout.addWidget(self.totalLabel)

        self.payButton = QtWidgets.QPushButton("Bezahlen", self)
        self.payButton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.cartLayout.addWidget(self.payButton)

    def loadProducts(self):
        # Load products from the database and display them
        products = session.query(Product).all()
        self.displayProducts(products)
        self.productCountLabel.setText(f"Total Products: {len(products)}")

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
        # Create a card for each product with fixed size
        card = QtWidgets.QFrame(self)
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet("background-color: #282c3c; padding: 1px;")
        card.setFixedSize(350, 150)  # Set fixed size for all product cards

        card.setObjectName("productCard")
        cardLayout = QtWidgets.QHBoxLayout(card)  # Change to horizontal layout

        # Product icon
        productIcon = QtWidgets.QLabel(self)
        productIcon.setPixmap(QtGui.QPixmap("resources/icons/shopping_cart_checkout.png").scaled(90, 90, QtCore.Qt.KeepAspectRatio))  # Product icon
        productIcon.setFixedWidth(90)
        productIcon.setFixedHeight(100)  # Set the height to fill the card
        iconLayout = QtWidgets.QVBoxLayout()  # Use a vertical layout for the icon
        iconLayout.addWidget(productIcon, alignment=QtCore.Qt.AlignVCenter)  # Center icon vertically

        # Create a vertical layout for the product details
        detailsLayout = QtWidgets.QVBoxLayout()
        
        # Product name and price labels
        nameLabel = QtWidgets.QLabel(product.produkt, card)
        nameLabel.setStyleSheet("color: white;")  # Change text color to white
        nameLabel.setFont(QtGui.QFont("Poppins", 12, QtGui.QFont.Bold))
        priceLabel = QtWidgets.QLabel(f"Price: ${product.verkaufspreis:.2f}", card)
        priceLabel.setStyleSheet("color: white;")  # Change text color to white
        priceLabel.setFont(QtGui.QFont("Poppins", 10))

        # Quantity input
        quantityInput = QtWidgets.QSpinBox(card)
        quantityInput.setRange(1, 100)
        quantityInput.setValue(1)
        quantityInput.setStyleSheet("background-color: whitesmoke;")  # Different background color for visibility

        # Add details to the details layout
        detailsLayout.addWidget(nameLabel)
        detailsLayout.addWidget(priceLabel)
        detailsLayout.addWidget(quantityInput)

        # Add icon and details layouts to the main card layout
        cardLayout.addLayout(iconLayout)  # Add the icon layout to the left
        cardLayout.addLayout(detailsLayout)  # Add the details layout to the right

        # Add product to cart on click, passing the selected quantity
        card.mousePressEvent = lambda event, p=product, q=quantityInput: self.addToCart(p, card, q.value())
        # Add hover effect
        # card.enterEvent = lambda event: card.setStyleSheet("background-color: #4CAF50; padding: 1px;")  # Change color on hover
        # card.leaveEvent = lambda event: card.setStyleSheet("background-color: #282c3c; padding: 1px;")  # Reset color when not hovered
        return card

    def filterProducts(self):
        # Filter products based on search text
        searchText = self.searchBar.text().lower()
        filteredProducts = session.query(Product).filter(Product.produkt.ilike(f"%{searchText}%")).all()
        self.displayProducts(filteredProducts)

    def addToCart(self, product, card, quantity):
        # Toggle product in cart
        if product in self.cartItems:
            # Remove the product if it's already in the cart
            del self.cartItems[product]
            self.removeFromCart(product)
            card.setStyleSheet("background-color: #282c3c;")  # Change back to original color
        else:
            # Add the product to the cart
            self.cartItems[product] = quantity
            self.cartList.addItem(f"🛒 {product.produkt} (Qty: {quantity}) - ${product.verkaufspreis * quantity:.2f}")
            self.updateTotals()
            card.setStyleSheet("background-color: #4CAF50;")

    def removeFromCart(self, product):
        # Remove the product from the cart list
        for index in range(self.cartList.count()):
            if product.produkt in self.cartList.item(index).text():
                self.cartList.takeItem(index)
                break
        self.updateTotals()

    def updateTotals(self):
        # Update subtotal, tax, and total
        subtotal = sum(product.verkaufspreis * quantity for product, quantity in self.cartItems.items())
        tax = subtotal * 0.1  # Example tax rate
        total = subtotal + tax

        self.subTotalLabel.setText(f"Subtotal: ${subtotal:.2f}")
        self.taxLabel.setText(f"Tax: ${tax:.2f}")
        self.totalLabel.setText(f"Total: ${total:.2f}")


