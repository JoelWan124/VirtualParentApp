from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

class AchievementBadge(QWidget):
    def __init__(self, name, description, unlocked=False):
        super().__init__()
        self.name = name
        self.description = description
        self.unlocked = unlocked
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Badge icon setup
        self.badge_icon = QLabel()
        self.update_icon()
        layout.addWidget(self.badge_icon)

        # Description setup
        description_label = QLabel(self.description)
        layout.addWidget(description_label)

        self.setLayout(layout)

    def update_icon(self):
        if self.unlocked:
            pixmap = QPixmap('path_to_unlocked_image.png')  # Replace with your unlocked image path
        else:
            pixmap = QPixmap('path_to_locked_image.png')  # Replace with your locked image path
        self.badge_icon.setPixmap(pixmap.scaled(50, 50, transformMode=Qt.SmoothTransformation))

    def unlock(self):
        self.unlocked = True
        self.update_icon()

class AchievementsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Achievements")
        layout = QVBoxLayout()

        # Example achievements setup
        self.badges = [
            AchievementBadge("Long Way to Go", "Complete the room for the first time."),
            AchievementBadge("BAHAHAHAHAHA", "Complete the room with 3 stars for the first time."),
            AchievementBadge("WoMp WOmp :(", "Fail to complete the room."),
            AchievementBadge("2Days in a row", "Complete the room for 2 consecutive days."),
            AchievementBadge("MANIACAL", "Complete the room for 7 consecutive days.")
        ]

        for badge in self.badges:
            layout.addWidget(badge)

        self.setLayout(layout)

# Example to demonstrate the unlocking process, which you can trigger based on actual events
def simulate_unlocking_achievements(window):
    # Assuming this function is called when conditions are met
    window.badges[0].unlock()  # Unlock the first badge

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = AchievementsWindow()
    ex.show()
    simulate_unlocking_achievements(ex)  # Simulate an unlock for demonstration
    sys.exit(app.exec_())
