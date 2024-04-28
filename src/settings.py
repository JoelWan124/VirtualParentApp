from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QTimeEdit, QHBoxLayout
from PyQt5.QtCore import QTime, pyqtSignal
from database import get_user_settings, update_user_settings
from history import HistoryWindow

class SettingsWindow(QWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.history = HistoryWindow(user_id=self.user_id)
        self.init_ui()
        self.populate_settings()

    def init_ui(self):
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        self.notifications_checkbox = QCheckBox("Enable Notifications", self)
        layout.addWidget(self.notifications_checkbox)

        # Create horizontal layouts for the time edits and labels
        day_layout = QHBoxLayout()
        self.day_time_edit = QTimeEdit(self)
        self.day_time_edit.setDisplayFormat("HH:mm")
        day_layout.addWidget(QLabel("Day Routine Notification Time:"))
        day_layout.addWidget(self.day_time_edit)
        self.day_time_display = QLabel("Latest time: Not set")
        day_layout.addWidget(self.day_time_display)
        layout.addLayout(day_layout)

        night_layout = QHBoxLayout()
        self.night_time_edit = QTimeEdit(self)
        self.night_time_edit.setDisplayFormat("HH:mm")
        night_layout.addWidget(QLabel("Night Routine Notification Time:"))
        night_layout.addWidget(self.night_time_edit)
        self.night_time_display = QLabel("Latest time: Not set")
        night_layout.addWidget(self.night_time_display)
        layout.addLayout(night_layout)

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
        if self.user_id:
            settings = get_user_settings(self.user_id)
            if settings:
                notifications_enabled, day_time, night_time = settings
                self.notifications_checkbox.setChecked(notifications_enabled == 1)
                self.day_time_edit.setTime(QTime.fromString(day_time, "HH:mm"))
                self.night_time_edit.setTime(QTime.fromString(night_time, "HH:mm"))
                self.day_time_display.setText(f"Latest time: {day_time}")
                self.night_time_display.setText(f"Latest time: {night_time}")
            else:
                # Set default values if settings are None
                self.notifications_checkbox.setChecked(True)
                self.day_time_edit.setTime(QTime(8, 0))
                self.night_time_edit.setTime(QTime(20, 0))

    #Update
    def update_settings(self):
        user_id = self.get_current_user_id()
        notifications_enabled = self.notifications_checkbox.isChecked()
        day_time = self.day_time_edit.time().toString("HH:mm")
        night_time = self.night_time_edit.time().toString("HH:mm")
        success = update_user_settings(user_id, notifications_enabled, day_time, night_time)
        if success:
            print("Settings updated successfully.")
            QMessageBox.information(self, "Update Success", "Settings updated successfully.")
        else:
            print("Failed to update settings.")
            QMessageBox.critical(self, "Update Failed", "Failed to update settings.")



    def navigate_to_history(self):
        self.history.show()

    def logout(self):
        self.logout_requested.emit()

    def get_current_user_id(self):
        return self.user_id

