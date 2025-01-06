import sys
from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow
import os
from PyQt5.QtGui import QFontDatabase, QFont

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
    
    # Load all custom fonts
    loaded_fonts = load_custom_fonts()  # Get a list of all loaded fonts

    print("Available custom fonts:", loaded_fonts)

    # Optionally, choose one font from the loaded fonts
    if "Rubik" in loaded_fonts:
        custom_font = QFont("Rubik", 9)
    else:
        custom_font = QFont("Tahoma", 10)  # Fallback font if "Oswald" is not loaded

    app.setFont(custom_font)  # Optionally, apply it globally or to specific widgets

    # Load and apply stylesheet
    stylesheet = load_stylesheet('resources/styles/style.qss')
    app.setStyleSheet(stylesheet)
    
    # Create the MainWindow instance
    window = MainWindow()
    
    # Set initial opacity to 0 (fully transparent)
    window.fade_effect.setOpacity(0)
    
    # Show the MainWindow
    window.show()
    
    # Start the fade-in animation
    window.fade_animation.start()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
