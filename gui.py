import time

from PyQt6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QSpinBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class GUI(QMainWindow):
    def __init__(self, on_download, on_convert):
        super().__init__()
        self.on_download = on_download
        self.on_convert = on_convert

        self.folder_path = "downloads"

        self.setWindowTitle("Spotify Downloader")
        self.setFixedSize(400, 450)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        # Title
        title_label = QLabel("Spotify Downloader")
        title_label.setFont(QFont("Arial", 25, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #4CAF50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input + Download Button
        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter playlist URL...")
        self.input_field.setFixedWidth(250)
        self.input_field.setFixedHeight(30)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                selection-background-color: rgba(0, 255, 0, 0.5);
                border: 2px solid #595757;
                border-radius: 8px;
                padding: 5px;
                background-color: #595757;
            }
            QLineEdit:hover {
                background-color: #4a4a4a;
            }
            QLineEdit:disabled {
                background-color: #302f2f;
            }
        """
        )

        self.download_button = QPushButton("Download")
        self.download_button.setFixedHeight(30)
        self.download_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #235225;
            }
        """
        )
        self.download_button.clicked.connect(self.on_download_clicked)
        self.download_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.download_button)

        # File Selection + Start NDX Button
        file_layout = QHBoxLayout()

        file_button_layout = QVBoxLayout()
        self.file_button = QPushButton("Select Folder")
        self.file_button.setFixedHeight(30)
        self.file_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #595757;
                border-radius: 8px;
                color: white;
                padding: 5px 15px;
                background-color: #595757;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #302f2f;
            }
        """
        )
        self.file_button.clicked.connect(self.select_file)
        self.file_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        file_button_layout.addWidget(self.file_button)

        spin_layout = QHBoxLayout()

        spin_label_1 = QLabel("Start")
        spin_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_box_1 = QSpinBox()
        self.spin_box_1.setFixedHeight(30)
        self.spin_box_1.setRange(1, 10000000)
        self.spin_box_1.setValue(0)
        self.spin_box_1.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_box_1.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_box_1.setToolTip("Start downloading from")
        self.spin_box_1.setStyleSheet(
            """
            QSpinBox {
                border: 2px solid #595757;
                border-radius: 8px;
                color: white;
                padding: 5px 15px;
                background-color: #595757;
                selection-background-color: rgba(0, 255, 0, 0.5);
            }
            QSpinBox:hover {
                background-color: #4a4a4a;
            }
            QSpinBox:disabled {
                background-color: #302f2f;
            }
        """
        )

        spin1_layout = QVBoxLayout()
        spin1_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        spin1_layout.setContentsMargins(0, 0, 0, 0)
        spin1_layout.setSpacing(0)
        spin1_layout.addWidget(spin_label_1)
        spin1_layout.addWidget(self.spin_box_1)

        spin_label_2 = QLabel("End")
        spin_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_box_2 = QSpinBox()
        self.spin_box_2.setFixedHeight(30)
        self.spin_box_2.setRange(1, 10000000)
        self.spin_box_2.setValue(15)
        self.spin_box_2.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_box_2.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_box_2.setToolTip("End downloading")
        self.spin_box_2.setStyleSheet(
            """
            QSpinBox {
                border: 2px solid #595757;
                border-radius: 8px;
                color: white;
                padding: 5px 15px;
                background-color: #595757;
                selection-background-color: rgba(0, 255, 0, 0.5);
            }
            QSpinBox:hover {
                background-color: #4a4a4a;
            }
            QSpinBox:disabled {
                background-color: #302f2f;
            }
        """
        )

        spin2_layout = QVBoxLayout()
        spin2_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        spin2_layout.setContentsMargins(0, 0, 0, 0)
        spin2_layout.setSpacing(0)
        spin2_layout.addWidget(spin_label_2)
        spin2_layout.addWidget(self.spin_box_2)

        spin_layout.addLayout(spin1_layout)
        spin_layout.addLayout(spin2_layout)
        spin_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        checkbox_layout = QVBoxLayout()
        self.checkbox = QCheckBox("Indexing")
        self.checkbox.setToolTip("Toggle to name songs using indexes.")
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet(
            """
            QCheckBox{
                padding: 9px 0px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 2px solid #45a049;
                border-radius: 8px;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
            }
        """
        )
        self.checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        raw_layout = QHBoxLayout()
        raw_label = QLabel("MP3 to RAW")
        raw_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.convert_button = QPushButton("Convert to RAW")
        self.convert_button.setFixedHeight(30)
        self.convert_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #595757;
                border-radius: 8px;
                color: white;
                padding: 5px 15px;
                background-color: #595757;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #302f2f;
            }
        """
        )
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        raw_layout.addWidget(raw_label)
        raw_layout.addWidget(self.convert_button)
        raw_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        checkbox_layout.addWidget(self.checkbox)
        checkbox_layout.setContentsMargins(0, 17, 0, 0)
        file_button_layout.setContentsMargins(0, 13, 0, 0)

        file_layout.addLayout(spin_layout)
        file_layout.addLayout(file_button_layout)
        file_layout.addLayout(checkbox_layout)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setFixedHeight(10)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Scrollable Label Grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(200)
        self.scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.growing_label = QLabel("")
        self.growing_label.setWordWrap(True)
        self.growing_label.setFixedWidth(350)
        self.growing_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
            }
        """
        )
        self.growing_label.adjustSize()
        self.growing_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.scroll_layout.addWidget(self.growing_label)

        scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(scroll_content)

        main_layout.addWidget(title_label)
        main_layout.addLayout(input_layout)
        main_layout.addSpacing(-10)
        main_layout.addLayout(file_layout)
        main_layout.addSpacing(-30)
        main_layout.addLayout(raw_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addSpacing(5)
        main_layout.addWidget(self.scroll_area)

        central_widget.setLayout(main_layout)

    def get_input_text(self):
        return self.input_field.text()

    def on_download_clicked(self):
        if self.spin_box_1.value() > self.spin_box_2.value():
            self.status_label.setText("Start/End is not possible.")
            return

        dir = self.folder_path
        url = self.get_input_text()

        self.download_button.setEnabled(False)
        self.file_button.setEnabled(False)
        self.input_field.setEnabled(False)
        self.spin_box_1.setEnabled(False)
        self.spin_box_2.setEnabled(False)
        self.checkbox.setEnabled(False)
        self.convert_button.setEnabled(False)

        if self.on_download:
            self.status_label.setText("Downloading...")

            self.on_download(
                url,
                dir,
                self.on_set_label,
                self.on_download_finished,
                self.on_track_downloaded,
                self.checkbox.isChecked(),
                self.spin_box_1.value(),
                self.spin_box_2.value(),
            )

    def on_set_label(self, label):
        self.status_label.setText(label)
        time.sleep(1)
        self.status_label.setText("")

    def start_conversion(self):
        self.download_button.setEnabled(False)
        self.file_button.setEnabled(False)
        self.input_field.setEnabled(False)
        self.spin_box_1.setEnabled(False)
        self.spin_box_2.setEnabled(False)
        self.checkbox.setEnabled(False)
        self.convert_button.setEnabled(False)

        if self.on_convert:
            self.status_label.setText("Converting...")

            self.on_convert(
                self.folder_path, self.on_set_label, self.on_download_finished
            )

    def on_download_finished(self):
        self.download_button.setEnabled(True)
        self.file_button.setEnabled(True)
        self.convert_button.setEnabled(True)
        self.input_field.setEnabled(True)
        self.spin_box_1.setEnabled(True)
        self.spin_box_2.setEnabled(True)
        self.checkbox.setEnabled(True)
        self.growing_label.setText("")

    def on_track_downloaded(self, track):
        current = self.growing_label.text()
        self.growing_label.setText(current + ("\n\n" if current else "") + track)
        self.growing_label.adjustSize()

    def select_file(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if self.folder_path:
            print(f"Selected folder: {self.folder_path}")
            self.status_label.setText(f"Selected folder: {self.folder_path}")
