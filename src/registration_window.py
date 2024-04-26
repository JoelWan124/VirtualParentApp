from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
import database

class RegistrationWindow(QWidget):
    registration_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Choose a username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Choose a password")
        self.password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton("Register")
        
        register_button.clicked.connect(self.register_user)
        
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(register_button)
        
        self.setLayout(layout)

    def register_user(self):
        if database.add_new_user(self.username.text(), self.password.text()):
            self.registration_success.emit()
        else:
            # Handle registration failure (e.g., username already exists)
            print("Registration failed")

