import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
import database


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
        # Check if the image exists using the correct relative path
        if os.path.exists(self.unlocked_image_path if self.unlocked else self.locked_image_path):
            pixmap = QPixmap(self.unlocked_image_path if self.unlocked else self.locked_image_path)
            self.badge_icon.setPixmap(pixmap.scaled(120, 120, transformMode=Qt.SmoothTransformation))
        else:
            print(f"Image not found: {self.unlocked_image_path if self.unlocked else self.locked_image_path}")


    def unlock(self):
        self.unlocked = True
        self.update_icon()

class AchievementsWindow(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.badges = []
        self.init_ui()
        if self.user_id is not None:
            self.load_achievements_for_user(self.user_id)

    def init_ui(self):
        self.setWindowTitle("Achievements")
        layout = QVBoxLayout()

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



    def load_achievements_for_user(self, user_id):
        # Connect to the database and check conditions for each badge
        conn = database.create_connection()
        if conn:
            try:
                # Badge 1: Long Way to Go - Completed the room at least once
                cursor = conn.cursor()
                cursor.execute("SELECT status FROM userRooms WHERE user_id = ? LIMIT 1", (user_id,))
                if cursor.fetchone():
                    self.badges[0].unlock()

                # Badge 2: BAHAHAHAHAHA - Completed the room with 3 stars for the first time
                cursor.execute("SELECT starEarned FROM userRooms WHERE user_id = ? AND starEarned = 3 LIMIT 1", (user_id,))
                if cursor.fetchone():
                    self.badges[1].unlock()

                # Badge 3: WoMp WOmp :( - Fail to complete the room
                cursor.execute("SELECT status FROM userRooms WHERE user_id = ? AND status = 0 LIMIT 1", (user_id,))
                if cursor.fetchone():
                    self.badges[2].unlock()

            except sqlite3.Error as e:
                print(f"An error occurred while retrieving achievements: {e}")
            finally:
                conn.close()

        # Checking the room completion status for a specific room
        room_completion_status = database.get_room_completion_status(user_id, "ToothbrushingRoom")
        if room_completion_status is not None and room_completion_status:
            self.badges[0].unlock()

    
        
