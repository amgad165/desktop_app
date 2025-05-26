from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem, QPushButton, QListWidget, QLabel,
    QTableWidget, QTableWidgetItem, QStackedWidget, QLineEdit, QMessageBox, QInputDialog,QHeaderView
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from app.models.app_models import Anreden, Einheiten, Lander, Zahlungsarten, session


class EinstellungenPage(QWidget):
    def __init__(self, parent=None):
        super(EinstellungenPage, self).__init__(parent)
        self.parent = parent

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Layout (Back Button)
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setIcon(QIcon("resources/icons/arrow-left.png"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("border: none; background-color: transparent;")
        back_button.clicked.connect(self.parent.go_back_to_settings_page)

        top_layout.addWidget(back_button)
        main_layout.addLayout(top_layout)

        # Bottom Layout (Sidebar + Content)
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(20)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(400)
        self.sidebar.setSpacing(10)
        self.sidebar.setStyleSheet("""
            QListWidget {
                border: none;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            }
            QListWidget::item {
                background-color: #e8e4e4;
                padding: 5px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                margin: 3px 0px;
                text-align: center;
            }
            QListWidget::item:selected {
                background-color: #b8b4b4;
            }
        """)

        # Sidebar Items
        items = ["Anreden", "Einheiten", "Lander", "Zahlungsarten"]
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignCenter)
            self.sidebar.addItem(item)

        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_table)
        bottom_layout.addWidget(self.sidebar)

        # Content Area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #ffffff; border-radius: 10px; padding: 20px;")
        bottom_layout.addWidget(self.stacked_widget, 1)

        main_layout.addLayout(bottom_layout)

        # Add Tables
        self.add_table_section("Anreden", ["ID", "Gender"], Anreden, ["gender"])
        self.add_table_section("Einheiten", ["ID", "Unit"], Einheiten, ["unit"])
        self.add_table_section("Lander", ["ID", "Country"], Lander, ["land"])
        self.add_table_section("Zahlungsarten", ["ID", "Payment Method"], Zahlungsarten, ["payment_method"])

    def add_table_section(self, title, headers, model, input_labels):
        table_section = QWidget()
        layout = QVBoxLayout(table_section)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #1c1c1e; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Input Form & Add Button
        input_layout = QHBoxLayout()
        form_inputs = {}

        for label in input_labels:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {label.lower()}")
            input_layout.addWidget(input_field)
            form_inputs[label] = input_field

        add_button = self.create_button("", "#27ae60", "#2ecc71", "resources/icons/plus.png")
        add_button.setFixedSize(40, 40)
        add_button.clicked.connect(lambda: self.add_record(model, form_inputs, table))
        input_layout.addWidget(add_button)

        layout.addLayout(input_layout)

        # Table
        table = QTableWidget()
        table.setColumnCount(len(headers) + 2)  # Extra columns for Edit & Delete
        table.setHorizontalHeaderLabels(headers + ["Edit", "Delete"])
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(True)

        # Set column width for value cells
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Expand value column
        table.setColumnHidden(0, True)  # Hide the ID column

        # Set width for edit and delete buttons
        table.setColumnWidth(len(headers), 60)  # Edit button column
        table.setColumnWidth(len(headers) + 1, 60)  # Delete button column
        table.verticalHeader().setVisible(False)


        # Hide Scrollbar and Adjust Styles
        table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                alternate-background-color: #f5f5f5;
            }
            QTableWidget::item {
                color: black; /* Ensure table text is black */
            }
            QTableWidget::item:selected {
                background-color: #b8b4b4;
                color: white;
            }
            QHeaderView::section {
                background-color: #333; /* Dark background */
                color: white; /* White text for contrast */
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #aaa;
                padding: 5px;
            }
            QScrollBar:vertical {
                width: 0px; /* Hide scrollbar */
                background: transparent;
            }
        """)



        layout.addWidget(table)

        self.load_table_data(table, model)
        self.stacked_widget.addWidget(table_section)

    def create_button(self, text, color, hover_color, icon_path):
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        return button

    def load_table_data(self, table, model):
        table.setRowCount(0)
        records = session.query(model).all()

        for record in records:
            row = table.rowCount()
            table.insertRow(row)

            for col, attr in enumerate(record.__table__.columns.keys()):
                table.setItem(row, col, QTableWidgetItem(str(getattr(record, attr, ""))))

            # Edit Button (Dark Background)
            edit_button = QPushButton()
            edit_button.setIcon(QIcon("resources/icons/edit.png"))
            edit_button.setStyleSheet("background-color: #333; border-radius: 5px;")
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(lambda _, r=record, t=table: self.edit_record(r, model, t))

            # Delete Button (Dark Background)
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("resources/icons/x.png"))
            delete_button.setStyleSheet("background-color: #333; border-radius: 5px;")
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda _, r=record, t=table: self.delete_record(r, model, t))

            table.setCellWidget(row, len(record.__table__.columns.keys()), edit_button)
            table.setCellWidget(row, len(record.__table__.columns.keys()) + 1, delete_button)

            # Set column width to avoid button overlay issues
            table.setRowHeight(row, 40)
            table.setColumnWidth(len(record.__table__.columns.keys()), 50)
            table.setColumnWidth(len(record.__table__.columns.keys()) + 1, 50)

    def add_record(self, model, form_inputs, table):
        try:
            new_record = model()
            for key, input_field in form_inputs.items():
                setattr(new_record, key, input_field.text())
            session.add(new_record)
            session.commit()
            self.load_table_data(table, model)
            for input_field in form_inputs.values():
                input_field.clear()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to add record: {str(e)}")

    def edit_record(self, record, model, table):
        new_value, ok = QInputDialog.getText(self, "Edit Record", f"Enter new value:")
        if ok and new_value.strip():
            setattr(record, list(record.__table__.columns.keys())[1], new_value.strip())
            session.commit()
            self.load_table_data(table, model)

    def delete_record(self, record, model, table):
        session.delete(record)
        session.commit()
        self.load_table_data(table, model)

    def change_table(self, index):
        self.stacked_widget.setCurrentIndex(index)
