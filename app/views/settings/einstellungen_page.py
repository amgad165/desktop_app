from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel,
    QTableWidget, QTableWidgetItem, QStackedWidget, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from app.models.app_models import Anreden, Einheiten, Lander, Zahlungsarten, session


class EinstellungenPage(QWidget):
    def __init__(self, parent=None):
        super(EinstellungenPage, self).__init__(parent)
        self.parent = parent

        # Main Layout
        main_layout = QVBoxLayout(self)  # Changed to QVBoxLayout for top-down arrangement
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Layout for Back Button
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("border: none; background-color: transparent;")
        back_button.clicked.connect(self.parent.go_back_to_settings_page)

        top_layout.addWidget(back_button)
        main_layout.addLayout(top_layout)

        # Bottom Layout for Sidebar and Content
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1c1c1e;
                color: #dcdcdc;
                font-size: 16px;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2a2a2c;
            }
            QListWidget::item:selected {
                background-color: #256d85;
                color: white;
            }
        """)
        self.sidebar.addItem("Anreden")
        self.sidebar.addItem("Einheiten")
        self.sidebar.addItem("Lander")
        self.sidebar.addItem("Zahlungsarten")
        self.sidebar.currentRowChanged.connect(self.change_table)
        bottom_layout.addWidget(self.sidebar)

        # Stacked Widget for Table Content
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #2c2c2e; padding: 10px;")
        bottom_layout.addWidget(self.stacked_widget)

        main_layout.addLayout(bottom_layout)

        # Add Tables
        self.add_table_section("Anreden", ["ID", "Gender"], Anreden, ["gender"])
        self.add_table_section("Einheiten", ["ID", "Unit"], Einheiten, ["unit"])
        self.add_table_section("Lander", ["ID", "Country"], Lander, ["land"])
        self.add_table_section("Zahlungsarten", ["ID", "Payment Method"], Zahlungsarten, ["payment_method"])


    def add_table_section(self, title, headers, model, input_labels):
        # Table Section
        table_section = QWidget()
        layout = QVBoxLayout(table_section)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px 0; color: #dcdcdc;")
        layout.addWidget(title_label)

        # Table
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable direct editing
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1c1c1e;
                border: 1px solid #3a3a3c;
                color: #dcdcdc;
                alternate-background-color: #2c2c2e;
            }
            QTableWidget::item {
                color: #dcdcdc;
            }
            QTableWidget::item:selected {
                background-color: #3a3a3c;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c2c2e;
                color: #dcdcdc;
                border: 1px solid #3a3a3c;
                height: 35px; /* Adjusts the overall height of header sections */
            }
        """)
        table.setAlternatingRowColors(True)
        layout.addWidget(table)

        # Load initial data from the database
        self.load_table_data(table, model)

        # Input Form
        form_layout = QFormLayout()
        form_inputs = {}
        for label in input_labels:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {label.lower()}")
            input_field.setStyleSheet("""
                QLineEdit {
                    background-color: #1c1c1e;
                    border: 1px solid #3a3a3c;
                    border-radius: 4px;
                    padding: 5px;
                    color: #dcdcdc;
                }
                QLineEdit:focus {
                    border-color: #3498db;
                }
            """)
            form_layout.addRow(label.capitalize(), input_field)
            form_inputs[label] = input_field
        layout.addLayout(form_layout)

        # Add, Edit, Delete Buttons
        # Add Button with Icon
        button_layout = QHBoxLayout()
 
        add_button = QPushButton("Add")
        add_button.setStyleSheet(self.get_button_style("#27ae60", "#2ecc71"))
        add_button.setIcon(QIcon("resources/icons/plus.png"))  # Replace with the path to your add icon
        add_button.clicked.connect(lambda: self.add_record(model, form_inputs, table))

        # Edit Button with Icon
        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet(self.get_button_style("#f39c12", "#f1c40f"))
        edit_button.setIcon(QIcon("resources/icons/edit.png"))  # Replace with the path to your edit icon
        edit_button.clicked.connect(lambda: self.edit_record(model, form_inputs, table))

        # Delete Button with Icon
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(self.get_button_style("#c0392b", "#e74c3c"))
        delete_button.setIcon(QIcon("resources/icons/x.png"))  # Replace with the path to your delete icon
        delete_button.clicked.connect(lambda: self.delete_record(model, table))

        # Add buttons to layout
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        # Add the section to the stacked widget
        self.stacked_widget.addWidget(table_section)

    def load_table_data(self, table, model):
        """Load data from the database into the table."""
        table.setRowCount(0)  # Clear existing rows
        records = session.query(model).all()
        for record in records:
            row = table.rowCount()
            table.insertRow(row)
            for col, attr in enumerate(record.__table__.columns.keys()):
                value = getattr(record, attr, "")
                table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_record(self, model, form_inputs, table):
        """Add a new record to the database and refresh the table."""
        try:
            new_record = model()
            for key, input_field in form_inputs.items():
                setattr(new_record, key, input_field.text())
            session.add(new_record)
            session.commit()
            self.load_table_data(table, model)
            for input_field in form_inputs.values():
                input_field.clear()
            QMessageBox.information(self, "Success", f"New {model.__tablename__} record added.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add record: {str(e)}")

    def edit_record(self, model, form_inputs, table):
        """Edit the selected record."""
        try:
            selected_row = table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Warning", "Please select a record to edit.")
                return
            record_id = int(table.item(selected_row, 0).text())
            record = session.query(model).get(record_id)
            for key, input_field in form_inputs.items():
                setattr(record, key, input_field.text())
            session.commit()
            self.load_table_data(table, model)
            QMessageBox.information(self, "Success", "Record updated successfully.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update record: {str(e)}")

    def delete_record(self, model, table):
        """Delete the selected record."""
        try:
            selected_row = table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Warning", "Please select a record to delete.")
                return
            record_id = int(table.item(selected_row, 0).text())
            record = session.query(model).get(record_id)
            session.delete(record)
            session.commit()
            self.load_table_data(table, model)
            QMessageBox.information(self, "Success", "Record deleted successfully.")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to delete record: {str(e)}")

    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 7px 15px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def change_table(self, index):
        """Change the displayed table section based on sidebar selection."""
        self.stacked_widget.setCurrentIndex(index)
