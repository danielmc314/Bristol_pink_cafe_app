import sys
from PySide6.QtWidgets import QApplication
from ui.app_window import AppWindow

from database.database_manager import create_tables


def main():
    
    #create tables for database if they dont exist already
    create_tables()

    app = QApplication(sys.argv)

    window = AppWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


