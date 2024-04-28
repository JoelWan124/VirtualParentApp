from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
import database

class LoginWindow(QWidget):
    login_success = pyqtSignal(int)
    register_request = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")
        
        login_button.clicked.connect(self.check_credentials)
        register_button.clicked.connect(self.register_request.emit)
        
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        
        self.setLayout(layout)

    def check_credentials(self):
        user_id = database.check_user_credentials(self.username.text(), self.password.text())
        if user_id:
            self.login_success.emit(user_id)  # Emit user_id upon successful login
        else:
            print("Login failed")
