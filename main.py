import sys
from PySide6.QtWidgets import QApplication

from src.gui.gui import MainWindow

if __name__ == "__main__":
    main_gui = QApplication()
    main_window = MainWindow()
    main_window.show()

    sys.exit(main_gui.exec_())
