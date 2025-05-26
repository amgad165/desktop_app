import sys
from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow
import os
from PyQt5.QtGui import QFontDatabase, QFont
from app.controllers.license_manager import is_license_active, activate_license
from PyQt5.QtWidgets import QInputDialog, QMessageBox

def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        stylesheet = file.read()
    return stylesheet

# Load all custom fonts and store their family names
def load_custom_fonts():
    font_dir = os.path.join('resources', 'fonts')
    loaded_fonts = []

    # Iterate through the font directory and load each font
    for font_name in os.listdir(font_dir):
        font_path = os.path.join(font_dir, font_name)
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            for font_family in font_families:
                loaded_fonts.append(font_family)
                print(f"Font loaded successfully: {font_family}")
        else:
            print(f"Failed to load font: {font_path}")

    return loaded_fonts

def main():
    app = QApplication(sys.argv)

    # Check if the license is active
    if not is_license_active():
        license_key, ok = QInputDialog.getText(None, "License Activation", "Enter your license key:")
        if ok and license_key:
            if activate_license(license_key):
                QMessageBox.information(None, "Success", "License activated successfully.")
            else:
                QMessageBox.critical(None, "Error", "Invalid or already used license key. Exiting application.")
                sys.exit(1)
        else:
            sys.exit(1)

    # Proceed with application launch
    loaded_fonts = load_custom_fonts()
    app.setFont(QFont("Rubik", 9) if "Rubik" in loaded_fonts else QFont("Arial", 10))

    stylesheet = load_stylesheet('resources/styles/style.qss')
    app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.fade_effect.setOpacity(0)
    window.show()
    window.fade_animation.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
