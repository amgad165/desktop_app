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
        # Add workersLabel at the top of the page
        self.workersLabel = QtWidgets.QLabel("Workers List", self)
        self.workersLabel.setObjectName("workersLabel")

        # Set the font size and style
        font = QtGui.QFont()
        font.setPointSize(20)
        self.workersLabel.setFont(font)

        # Center align the label
        self.workersLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.workersLabel)

        # Search bar
        self.searchInput = QtWidgets.QLineEdit(self)
        self.searchInput.setPlaceholderText("Search Workers")
        self.searchInput.textChanged.connect(self.filter_workers)
        self.layout.addWidget(self.searchInput)

        # Table for workers
        self.workersTable = QtWidgets.QTableWidget(self)
        self.workersTable.setColumnCount(9)
        self.workersTable.setHorizontalHeaderLabels(
            ["Status", "Nummer", "Worker", "Adresse", "PLZ", "Ort", "Telefon", "Mobil", "eMail"]
        )
        self.workersTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.workersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.workersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.workersTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.workersTable)

        # Buttons for add, edit, and delete
        self.buttonsLayout = QtWidgets.QHBoxLayout()

        # Add button
        self.addButton = QPushButton("Add", self)
        self.addButton.setIcon(QtGui.QIcon('resources/icons/plus.png'))
        self.addButton.setIconSize(QtCore.QSize(17, 17))
        self.addButton.setStyleSheet("font-size: 16px;")

        # Edit button
        self.editButton = QPushButton("Edit", self)
        self.editButton.setIcon(QtGui.QIcon('resources/icons/edit.png'))
        self.editButton.setIconSize(QtCore.QSize(16, 16))
        self.editButton.setStyleSheet("font-size: 16px;")

        # Delete button
        self.deleteButton = QPushButton("Delete", self)
        self.deleteButton.setIcon(QtGui.QIcon('resources/icons/delete.png'))
        self.deleteButton.setIconSize(QtCore.QSize(17, 17))
        self.deleteButton.setStyleSheet("font-size: 16px;")

        # Add buttons to layout
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.editButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.layout.addLayout(self.buttonsLayout)

        self.retranslateUi()
        self.load_workers()

        # Connect buttons to functions
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
            QMessageBox.warning(self, "Edit Error", "Please select a worker to edit.")
            return
        worker_id = self.workersTable.item(selected_row, 1).text()
        worker = session.query(Worker).filter_by(nummer=worker_id).first()

        if not worker:
            QMessageBox.warning(self, "Edit Error", "Worker not found.")
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
            QMessageBox.warning(self, "Delete Error", "Please select a worker to delete.")
            return
        worker_id = self.workersTable.item(selected_row, 1).text()
        worker = session.query(Worker).filter_by(nummer=worker_id).first()

        if not worker:
            QMessageBox.warning(self, "Delete Error", "Worker not found.")
            return

        reply = QMessageBox.question(self, 'Delete Confirmation',
                                     "Are you sure you want to delete this worker?",
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

        for label, field in fields:
            layout.addRow(label, field)

        self.saveButton = QPushButton("Save", self)
        self.cancelButton = QPushButton("Cancel", self)
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
