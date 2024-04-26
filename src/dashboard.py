from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from toothbrushing_room import ToothbrushingRoom

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.toothbrushing_room = ToothbrushingRoom()  # Ensure you import ToothbrushingRoom correctly
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setFixedSize(800, 600)

        # Layouts for the routines
        layout = QVBoxLayout()
        day_layout = QVBoxLayout()
        night_layout = QVBoxLayout()

        # Day routine
        day_label = QLabel("Day Routine")
        self.day_toothbrushing_button = QPushButton('Go to Toothbrushing Room')
        self.day_toothbrushing_button.clicked.connect(self.open_toothbrushing_room)
        day_layout.addWidget(day_label)
        day_layout.addWidget(self.day_toothbrushing_button)

        # Night routine
        night_label = QLabel("Night Routine")
        self.night_toothbrushing_button = QPushButton('Go to Toothbrushing Room')
        self.night_toothbrushing_button.clicked.connect(self.open_toothbrushing_room)
        night_layout.addWidget(night_label)
        night_layout.addWidget(self.night_toothbrushing_button)

        # Add day and night routines to the main layout
        layout.addLayout(day_layout)
        layout.addLayout(night_layout)
        self.setLayout(layout)

    def open_toothbrushing_room(self):
        self.toothbrushing_room.show()
