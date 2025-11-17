import sys
from PyQt6.QtWidgets import QApplication
from dataforge.main_app import MainApp


def main():
    """Startet die DataForge-GUI."""
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    # sys.exit(app.exec())
    app.exec()


if __name__ == "__main__":
    main()
