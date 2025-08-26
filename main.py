import sys

from gui import GUI
from downloader import Downloader

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))

    worker = Downloader()
    window = GUI(on_download=worker.start_download, on_convert=worker.mp3_to_raw)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
