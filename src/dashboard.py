from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from toothbrushing_room import ToothbrushingRoom
import database  # Import your database module here

class Dashboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.toothbrushing_room = ToothbrushingRoom(user_id=self.user_id)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dashboard")
        self.setFixedSize(800, 600)

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

        # Update the button texts based on the room status
        self.update_room_status_buttons()

    def update_room_status_buttons(self):
        # Assuming that 'get_room_completion_status' returns True, False, or None
        status = database.get_room_completion_status(self.user_id, "Toothbrushing")
        button_text = "Toothbrushing Room - Completed" if status else "Toothbrushing Room - Incomplete"
        self.day_toothbrushing_button.setText(button_text)
        self.night_toothbrushing_button.setText(button_text)

    def open_toothbrushing_room(self):
        # Open the toothbrushing room window, passing in the user ID if needed
        self.toothbrushing_room.show()

# You would use this Dashboard class somewhere in your application like this:
# user_id = ... # Determine the logged-in user's ID
# dashboard = Dashboard(user_id=user_id)
