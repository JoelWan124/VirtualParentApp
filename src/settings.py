from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        self.notifications_checkbox = QCheckBox("Enable Notifications", self)
        self.update_button = QPushButton("Update Settings", self)

        layout.addWidget(self.notifications_checkbox)
        layout.addWidget(self.update_button)
        self.setLayout(layout)
