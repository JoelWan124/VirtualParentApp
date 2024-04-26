from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import database

class ToothbrushingRoom(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id  # Store the user_id passed in
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.instructions_label = QLabel("Follow the steps to brush your teeth properly.")
        self.start_button = QPushButton("Start Toothbrushing")
        self.start_button.clicked.connect(self.start_toothbrushing)

        # If you want to display user-specific data, you can update the UI here
        # For example, show the user's current progress if you have that information.

        layout.addWidget(self.instructions_label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_toothbrushing(self):
        # This function would start the toothbrushing activity
        # Since we now have a user_id, we can log this activity as belonging to that user.
        print(f"Toothbrushing activity started for user_id: {self.user_id}")
        # You might want to have a method to check or update the user's progress here.
