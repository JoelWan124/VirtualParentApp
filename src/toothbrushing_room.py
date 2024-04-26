from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class ToothbrushingRoom(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.instructions_label = QLabel("Follow the steps to brush your teeth properly.")
        self.start_button = QPushButton("Start Toothbrushing")
        self.start_button.clicked.connect(self.start_toothbrushing)

        layout.addWidget(self.instructions_label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_toothbrushing(self):
        # This function would start the toothbrushing activity
        print("Toothbrushing activity started")

# This class would be imported and instantiated in the Dashboard.py
