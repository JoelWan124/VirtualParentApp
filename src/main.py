import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction
from dashboard import Dashboard
from login_window import LoginWindow
from registration_window import RegistrationWindow
from toothbrushing_room import ToothbrushingRoom
from achievements import AchievementsWindow
from settings import SettingsWindow
from history import HistoryWindow
from PyQt5.QtCore import QThread
from services import start_notification_scheduler


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
        # Set up the user-specific windows here with the current_user_id
        self.dashboard = Dashboard(user_id=self.current_user_id)
        self.settings_window = SettingsWindow(user_id=self.current_user_id)
        self.settings_window.logout_requested.connect(self.logout)
        self.show_dashboard()
        self.navbar.show()

        # Start the notification scheduler in a new thread
        self.notification_thread = QThread()
        self.notification_thread.started.connect(lambda: start_notification_scheduler(self.current_user_id))
        self.notification_thread.start()




#####Before Login (User)
    def show_login(self):
        self.current_user_id = None
        self.login_window = self.create_login_window()
        self.setCentralWidget(self.login_window)
        self.navbar.hide()

    def show_registration(self):
        if not hasattr(self, 'registration_window'):
            self.registration_window = self.create_registration_window()
        self.setCentralWidget(self.registration_window)


#####After login (Member)
    def show_dashboard(self):
        self.dashboard = Dashboard(user_id=self.current_user_id)
        self.setCentralWidget(self.dashboard)



    def show_achievements(self):
        self.achievements_window = AchievementsWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.achievements_window)


    def show_settings(self):
        self.settings_window = SettingsWindow(user_id=self.current_user_id)
        self.settings_window.logout_requested.connect(self.logout)
        self.setCentralWidget(self.settings_window)


    def show_history(self):
        self.history_window = HistoryWindow(user_id=self.current_user_id)
        self.setCentralWidget(self.history_window)

    def show_toothbrushing_room(self):
        self.toothbrushing_room = ToothbrushingRoom(user_id=self.current_user_id)
        self.setCentralWidget(self.toothbrushing_room)



    def logout(self):
        print("Logging out...")  # Debug print to confirm logout is called
        
        # Clear the central widget
        current_central_widget = self.takeCentralWidget()
        if current_central_widget is not None:
            current_central_widget.deleteLater()

         # Stop the notification scheduler
        if hasattr(self, 'notification_thread'):
            self.notification_thread.quit()
            self.notification_thread.wait()

        # Reset the user ID and any user-specific state
        self.current_user_id = None
        self.dispose_user_windows()
        self.show_login()

    def dispose_user_windows(self):
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
