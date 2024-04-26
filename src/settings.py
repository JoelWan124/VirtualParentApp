# settings.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QTimeEdit
from PyQt5.QtCore import QTime, pyqtSignal

from database import get_user_settings, update_user_settings

class SettingsWindow(QWidget):
    history_requested = pyqtSignal()
    logout_requested = pyqtSignal()

    def __init__(self, user_id=None):  # Accept an optional user_id argument
        super().__init__()
        self.user_id = user_id  # Store the user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        self.notifications_checkbox = QCheckBox("Enable Notifications", self)
        layout.addWidget(self.notifications_checkbox)

        self.day_time_edit = QTimeEdit(self)
        self.day_time_edit.setTime(QTime(8, 0))
        self.day_time_edit.setDisplayFormat("hh:mm AP")
        layout.addWidget(QLabel("Day Routine Notification Time:"))
        layout.addWidget(self.day_time_edit)

        self.night_time_edit = QTimeEdit(self)
        self.night_time_edit.setTime(QTime(20, 0))
        self.night_time_edit.setDisplayFormat("hh:mm AP")
        layout.addWidget(QLabel("Night Routine Notification Time:"))
        layout.addWidget(self.night_time_edit)

        self.update_button = QPushButton("Update Settings", self)
        self.update_button.clicked.connect(self.update_settings)
        layout.addWidget(self.update_button)
        

        self.history_button = QPushButton("View History", self)
        self.history_button.clicked.connect(self.navigate_to_history)
        layout.addWidget(self.history_button)

        self.logout_button = QPushButton("Logout", self)
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def populate_settings(self):
        user_id = self.get_current_user_id()  # Implement this method
        settings = get_user_settings(user_id)
        if settings:
            notifications_enabled, day_time, night_time = settings
            self.notifications_checkbox.setChecked(notifications_enabled)
            self.day_time_edit.setTime(QTime.fromString(day_time, "HH:mm"))
            self.night_time_edit.setTime(QTime.fromString(night_time, "HH:mm"))

    def update_settings(self):
        user_id = self.get_current_user_id()  # Implement this method
        notifications_enabled = self.notifications_checkbox.isChecked()
        day_time = self.day_time_edit.time().toString("HH:mm")
        night_time = self.night_time_edit.time().toString("HH:mm")
        success = update_user_settings(user_id, notifications_enabled, day_time, night_time)
        if success:
            print("Settings updated successfully.")
        else:
            print("Failed to update settings.")

    def navigate_to_history(self):
        self.history_requested.emit()

    def logout(self):
        self.logout_requested.emit()

    def get_current_user_id(self):
        return self.user_id

