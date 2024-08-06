import sys
from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow

def load_stylesheet(file_path):
    with open(file_path, 'r') as file:
        stylesheet = file.read()
    return stylesheet

def main():
    app = QApplication(sys.argv)
    
    # Load and apply stylesheet
    stylesheet = load_stylesheet('resources/styles/style.qss')
    app.setStyleSheet(stylesheet)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
