import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt


class AchievementBadge(QWidget):
    def __init__(self, name, description, unlocked=False, locked_image_path='path_to_locked_image.png', unlocked_image_path='path_to_unlocked_image.png'):
        super().__init__()
        self.name = name
        self.description = description
        self.unlocked = unlocked
        self.locked_image_path = locked_image_path
        self.unlocked_image_path = unlocked_image_path
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
        pixmap = QPixmap(self.unlocked_image_path if self.unlocked else self.locked_image_path)
        self.badge_icon.setPixmap(pixmap.scaled(120, 120, transformMode=Qt.SmoothTransformation))

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
            AchievementBadge(
                "Long Way to Go", 
                "Complete the room for the first time.", 
                False, 
                '../resources/images/badges/locked.png', 
                '../resources/images/badges/unlocked1.png'
            ),
            AchievementBadge(
                "BAHAHAHAHAHA", 
                "Complete the room with 3 stars for the first time.", 
                False, 
                '../resources/images/badges/locked.png', 
                '../resources/images/badges/unlocked2.png'
            ),
            AchievementBadge(
                "WoMp WOmp :(", 
                "Fail to complete the room.", 
                False, 
                '../resources/images/badges/locked.png', 
                '../resources/images/badges/unlocked3.png'
            ),
            AchievementBadge(
                "2Days in a row", 
                "Complete the room for 2 consecutive days.", 
                False, 
                '../resources/images/badges/locked.png', 
                '../resources/images/badges/unlocked4.png'
            ),
            AchievementBadge(
                "MANIACAL", 
                "Complete the room for 7 consecutive days.", 
                False, 
                '../resources/images/badges/locked.png', 
                '../resources/images/badges/unlocked5.png'
            )
        ]

        for badge in self.badges:
            layout.addWidget(badge)

        self.setLayout(layout)

# Example to demonstrate the unlocking process, which you can trigger based on actual events
#Triggered by the toothbrushing activities
def simulate_unlocking_achievements(window):
    # Assuming this function is called when conditions are met
    window.badges[0].unlock()  # Unlock the first badge

if __name__ == "__main__":
    # Check if the image file exists before starting the application
    image_path = '../resources/images/badges/locked.png'
    if not os.path.isfile(image_path):
        print(f"Image file not found: {image_path}")
    else:
        print(f"Image file exists: {image_path}")
    import sys
    app = QApplication(sys.argv)
    ex = AchievementsWindow()
    ex.show()
    simulate_unlocking_achievements(ex)  # Simulate an unlock for demonstration
    sys.exit(app.exec_())
