from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from app.models.app_models import Worker, session  # Import the Worker model

class WorkersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("WorkersPage")
        self.resize(1000, 600)

        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("mainLayout")

        # Title label
        self.workersLabel = QtWidgets.QLabel("Mitarbeiterliste", self)
        self.workersLabel.setObjectName("workersLabel")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.workersLabel.setFont(font)
        self.workersLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.workersLabel)

        # --- Styled search container ---
        self.searchContainer = QtWidgets.QWidget(self)
        self.searchContainer.setFixedHeight(60)
        self.searchContainer.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 20px;
            }
        """)
        self.searchContainerLayout = QtWidgets.QHBoxLayout(self.searchContainer)
        self.searchContainerLayout.setContentsMargins(12, 6, 12, 6)
        self.searchContainerLayout.setSpacing(8)

        # Search icon
        searchIconLabel = QtWidgets.QLabel()
        searchIconLabel.setFixedSize(28, 28)
        searchIconLabel.setAlignment(QtCore.Qt.AlignCenter)

        iconPath = "resources/icons/search_blue.png"
        pixmap = QtGui.QPixmap(iconPath)
        if pixmap.isNull():
            import os
            absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), iconPath)
            pixmap = QtGui.QPixmap(absolute_path)
        if pixmap.isNull():
            searchIconLabel.setText("🔍")
            searchIconLabel.setStyleSheet("QLabel { color: #666; font-size: 16px; background: transparent; }")
        else:
            scaledPixmap = QtGui.QPixmap(22, 22)
            scaledPixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(scaledPixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            painter.drawPixmap(0, 0, 22, 22, pixmap.scaled(22, 22, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            painter.end()
            searchIconLabel.setPixmap(scaledPixmap)
        searchIconLabel.setStyleSheet("QLabel { background: transparent; padding: 0px; margin: 0px; }")

        self.searchContainerLayout.addWidget(searchIconLabel)
        self.searchContainerLayout.addSpacing(8)

        # Search input
        self.searchInput = QtWidgets.QLineEdit()
        self.searchInput.setPlaceholderText("Suche...")
        self.searchInput.textChanged.connect(self.filter_workers)
        self.searchInput.setStyleSheet("""
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
        self.searchInput.setMinimumWidth(400)
        self.searchContainerLayout.addWidget(self.searchInput, 1)

        self.searchContainerLayout.addStretch()

        # --- Icon-only buttons with hover ---
        iconBtnStyle = """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
                border-radius: 8px;
            }
        """

        self.addButton = QtWidgets.QPushButton()
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus_b.png'))
        self.addButton.setIconSize(QtCore.QSize(22, 22))
        self.addButton.setToolTip("Mitarbeiter hinzufügen")
        self.addButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.addButton)

        self.editButton = QtWidgets.QPushButton()
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit_b.png'))
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setToolTip("Mitarbeiter bearbeiten")
        self.editButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.editButton)

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete_b.png'))
        self.deleteButton.setIconSize(QtCore.QSize(22, 22))
        self.deleteButton.setToolTip("Mitarbeiter löschen")
        self.deleteButton.setStyleSheet(iconBtnStyle)
        self.searchContainerLayout.addWidget(self.deleteButton)

        self.layout.addWidget(self.searchContainer)

        # Workers table
        self.workersTable = QtWidgets.QTableWidget(self)
        self.workersTable.setColumnCount(9)
        self.workersTable.setHorizontalHeaderLabels([
            "Status", "Nummer", "Worker", "Adresse", "PLZ", "Ort", "Telefon", "Mobil", "eMail"
        ])
        self.workersTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.workersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.workersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.workersTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.workersTable)

        self.retranslateUi()
        self.load_workers()

        # Connect signals
        self.addButton.clicked.connect(self.add_worker)
        self.editButton.clicked.connect(self.edit_worker)
        self.deleteButton.clicked.connect(self.delete_worker)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("WorkersPage", "Workers Page"))

    def load_workers(self):
        self.workersTable.setRowCount(0)
        workers = session.query(Worker).all()  # Use the session to query Workers
        for worker in workers:
            row_position = self.workersTable.rowCount()
            self.workersTable.insertRow(row_position)
            self.workersTable.setItem(row_position, 0, QTableWidgetItem(worker.status or ""))
            self.workersTable.setItem(row_position, 1, QTableWidgetItem(worker.nummer))
            self.workersTable.setItem(row_position, 2, QTableWidgetItem(worker.worker))
            self.workersTable.setItem(row_position, 3, QTableWidgetItem(worker.adresse))
            self.workersTable.setItem(row_position, 4, QTableWidgetItem(worker.plz))
            self.workersTable.setItem(row_position, 5, QTableWidgetItem(worker.ort))
            self.workersTable.setItem(row_position, 6, QTableWidgetItem(worker.telefon))
            self.workersTable.setItem(row_position, 7, QTableWidgetItem(worker.mobil or ""))
            self.workersTable.setItem(row_position, 8, QTableWidgetItem(worker.email))

    def filter_workers(self):
        filter_text = self.searchInput.text().lower()
        for row in range(self.workersTable.rowCount()):
            item = self.workersTable.item(row, 2)  # Assuming "Worker" (Name) is in the 3rd column
            self.workersTable.setRowHidden(row, filter_text not in item.text().lower())

    def add_worker(self):
        dialog = WorkerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_worker = dialog.get_worker_data()
            # Save to database
            worker = Worker(**new_worker)
            session.add(worker)
            session.commit()
            self.load_workers()

    def edit_worker(self):
        selected_row = self.workersTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Bitte wählen Sie einen Mitarbeiter zum Bearbeiten aus.")
            return
        worker_id = self.workersTable.item(selected_row, 1).text()
        worker = session.query(Worker).filter_by(nummer=worker_id).first()

        if not worker:
            QMessageBox.warning(self, "Bearbeitungsfehler", "Mitarbeiter nicht gefunden.")
            return

        dialog = WorkerDialog(self, worker)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_worker_data()
            for key, value in updated_data.items():
                setattr(worker, key, value)
            session.commit()
            self.load_workers()

    def delete_worker(self):
        selected_row = self.workersTable.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Löschfehler", "Bitte wählen Sie einen Mitarbeiter zum Löschen aus.")
            return
        worker_id = self.workersTable.item(selected_row, 1).text()
        worker = session.query(Worker).filter_by(nummer=worker_id).first()

        if not worker:
            QMessageBox.warning(self, "Löschfehler", "Mitarbeiter nicht gefunden.")
            return

        reply = QMessageBox.question(self, 'Löschbestätigung',
                                     "Sind Sie sicher, dass Sie diesen Mitarbeiter löschen möchten?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            session.delete(worker)
            session.commit()
            self.load_workers()

class WorkerDialog(QDialog):
    def __init__(self, parent=None, worker=None):
        super().__init__(parent)
        self.worker = worker
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Worker Details")
        self.setModal(True)
        layout = QFormLayout(self)

        # Style for labels
        label_style = "color: white; font-size: 14px;"

        # Fields
        self.numberEdit = QLineEdit(self)
        self.nameEdit = QLineEdit(self)
        self.addressEdit = QLineEdit(self)
        self.zipCodeEdit = QLineEdit(self)
        self.cityEdit = QLineEdit(self)
        self.phoneEdit = QLineEdit(self)
        self.mobileEdit = QLineEdit(self)
        self.emailEdit = QLineEdit(self)

        fields = [
            ("Number", self.numberEdit),
            ("Name", self.nameEdit),
            ("Address", self.addressEdit),
            ("ZIP Code", self.zipCodeEdit),
            ("City", self.cityEdit),
            ("Phone", self.phoneEdit),
            ("Mobile", self.mobileEdit),
            ("Email", self.emailEdit),
        ]

        for label_text, field in fields:
            label = QtWidgets.QLabel(label_text)
            label.setStyleSheet(label_style)
            layout.addRow(label, field)

            layout.addRow(label, field)

        self.saveButton = QPushButton("Speichern", self)
        self.cancelButton = QPushButton("Stornieren", self)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow(button_layout)

        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        if self.worker:
            self.load_worker_data()

    def load_worker_data(self):
        self.numberEdit.setText(self.worker.nummer)
        self.nameEdit.setText(self.worker.worker)
        self.addressEdit.setText(self.worker.adresse)
        self.zipCodeEdit.setText(self.worker.plz)
        self.cityEdit.setText(self.worker.ort)
        self.phoneEdit.setText(self.worker.telefon)
        self.mobileEdit.setText(self.worker.mobil or "")
        self.emailEdit.setText(self.worker.email)

    def get_worker_data(self):
        return {
            'nummer': self.numberEdit.text(),
            'worker': self.nameEdit.text(),
            'adresse': self.addressEdit.text(),
            'plz': self.zipCodeEdit.text(),
            'ort': self.cityEdit.text(),
            'telefon': self.phoneEdit.text(),
            'mobil': self.mobileEdit.text() or None,
            'email': self.emailEdit.text(),
        }
