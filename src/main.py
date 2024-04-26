import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction
from dashboard import Dashboard
from login_window import LoginWindow
from registration_window import RegistrationWindow
from toothbrushing_room import ToothbrushingRoom
from achievements import AchievementsWindow
from settings import SettingsWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Virtual Parent Application')
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()
        self.init_navbar()

    def init_ui(self):
        # Start with login window
        self.login_window = self.create_login_window()
        self.setCentralWidget(self.login_window)
        self.navbar_visible = False  # Track visibility of the navbar

    def init_navbar(self):
        # Initialize the navigation bar but keep it hidden initially
        self.navbar = QToolBar("Navigation")
        self.addToolBar(self.navbar)
        self.navbar.hide()  # Initially hide the navbar

        dashboard_action = QAction('Dashboard', self)
        dashboard_action.triggered.connect(self.show_dashboard)
        self.navbar.addAction(dashboard_action)

        achievements_action = QAction('Achievements', self)
        achievements_action.triggered.connect(self.show_achievements)
        self.navbar.addAction(achievements_action)

        settings_action = QAction('Settings', self)
        settings_action.triggered.connect(self.show_settings)
        self.navbar.addAction(settings_action)

    def create_login_window(self):
        login_window = LoginWindow()
        login_window.login_success.connect(self.user_logged_in)
        login_window.register_request.connect(self.show_registration)
        return login_window

    def user_logged_in(self):
        self.show_dashboard()
        self.show_navbar()

    def show_navbar(self):
        self.navbar.show()
        self.navbar_visible = True

    def hide_navbar(self):
        self.navbar.hide()
        self.navbar_visible = False

    def show_dashboard(self):
        self.dashboard = Dashboard()  # Create a new instance each time
        self.setCentralWidget(self.dashboard)
        if self.navbar_visible:
            self.show_navbar()

    def show_registration(self):
        self.registration_window = RegistrationWindow()  # Create a new instance each time
        self.setCentralWidget(self.registration_window)
        self.hide_navbar()

    def show_toothbrushing_room(self):
        self.toothbrushing_room = ToothbrushingRoom()  # Create a new instance each time
        self.setCentralWidget(self.toothbrushing_room)

    def show_achievements(self):
        self.achievements_window = AchievementsWindow()  # Create a new instance each time
        self.setCentralWidget(self.achievements_window)

    def show_settings(self):
        self.settings_window = SettingsWindow()  # Create a new instance each time
        self.setCentralWidget(self.settings_window)

def main():
    app = QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
