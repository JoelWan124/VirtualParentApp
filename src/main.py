import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction
from dashboard import Dashboard
from login_window import LoginWindow
from registration_window import RegistrationWindow
from toothbrushing_room import ToothbrushingRoom
from achievements import AchievementsWindow
from settings import SettingsWindow
from history import HistoryWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user_id = None  # Initialize with no user
        self.setWindowTitle('Virtual Parent Application')
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.init_navbar()

    def init_ui(self):
        self.login_window = self.create_login_window()
        self.registration_window = self.create_registration_window()
        self.setCentralWidget(self.login_window)

    def init_navbar(self):
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

    def create_registration_window(self):
        registration_window = RegistrationWindow()
        registration_window.registration_success.connect(self.show_login)
        return registration_window

    def user_logged_in(self, user_id):
        self.current_user_id = user_id
        self.dashboard = Dashboard(user_id=user_id)  # Pass user_id to the dashboard
        self.show_dashboard()
        self.navbar.show()

    def show_login(self):
        self.current_user_id = None
        self.login_window = self.create_login_window()  # Recreate the login window
        self.setCentralWidget(self.login_window)
        self.navbar.hide()

    def show_dashboard(self):
        if not hasattr(self, 'dashboard') or self.dashboard.user_id != self.current_user_id:
            self.dashboard = Dashboard(user_id=self.current_user_id)  # Pass user_id to the dashboard
        self.setCentralWidget(self.dashboard)

    def show_registration(self):
        if not hasattr(self, 'registration_window'):
            self.registration_window = self.create_registration_window()
        self.setCentralWidget(self.registration_window)

    def show_achievements(self):
        if not hasattr(self, 'achievements_window') or self.achievements_window.user_id != self.current_user_id:
            self.achievements_window = AchievementsWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.achievements_window)

    def show_settings(self):
        if not hasattr(self, 'settings_window') or self.settings_window.user_id != self.current_user_id:
            self.settings_window = SettingsWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.settings_window)

    def show_history(self):
        if not hasattr(self, 'history_window') or self.history_window.user_id != self.current_user_id:
            self.history_window = HistoryWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.history_window)

    def show_toothbrushing_room(self):
        if not hasattr(self, 'toothbrushing_room') or self.toothbrushing_room.user_id != self.current_user_id:
            self.toothbrushing_room = ToothbrushingRoom(user_id=self.current_user_id)
        self.setCentralWidget(self.toothbrushing_room)

    def logout(self):
        self.current_user_id = None
        # Clear all user-specific windows
        self.dashboard = None
        self.achievements_window = None
        self.settings_window = None
        self.history_window = None
        self.toothbrushing_room = None
        self.show_login()

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
