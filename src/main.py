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
        self.dashboard = None
        self.achievements_window = None
        self.settings_window = None
        self.history_window = None
        self.toothbrushing_room = None
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
        self.show_dashboard()
        self.navbar.show()



#####Before Login (User)
    def show_login(self):
        self.current_user_id = None
        self.login_window = self.create_login_window()  # Recreate the login window
        self.setCentralWidget(self.login_window)
        self.navbar.hide()

    def show_registration(self):
        if not hasattr(self, 'registration_window'):
            self.registration_window = self.create_registration_window()
        self.setCentralWidget(self.registration_window)


#####After login (Member)
    def show_dashboard(self):
        # Create a new dashboard instance with the current user's ID.
        self.dashboard = Dashboard(user_id=self.current_user_id)
        # Set the new dashboard instance as the central widget.
        self.setCentralWidget(self.dashboard)



    def show_achievements(self):
        # Create a new instance of AchievementsWindow
        self.achievements_window = AchievementsWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.achievements_window)


    def show_settings(self):
        self.settings_window = SettingsWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.settings_window)

    def show_history(self):
        self.history_window = HistoryWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.history_window)

    def show_toothbrushing_room(self):
        self.toothbrushing_room = ToothbrushingRoom(user_id=self.current_user_id)
        self.setCentralWidget(self.toothbrushing_room)


    def logout(self):
        self.current_user_id = None
        # Dispose of user-specific windows
        self.dispose_user_windows()
        self.show_login()

    def dispose_user_windows(self):
        # Properly dispose of windows to free up resources
        if self.dashboard:
            self.dashboard.deleteLater()
        if self.achievements_window:
            self.achievements_window.deleteLater()
        if self.settings_window:
            self.settings_window.deleteLater()
        if self.history_window:
            self.history_window.deleteLater()
        if self.toothbrushing_room:
            self.toothbrushing_room.deleteLater()

        # Reset references to None
        self.dashboard = None
        self.achievements_window = None
        self.settings_window = None
        self.history_window = None
        self.toothbrushing_room = None

def main():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
