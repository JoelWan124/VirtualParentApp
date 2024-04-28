import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from services import send_notification
from database import get_room_id_by_name, complete_room_for_user

class ToothbrushingRoom(QWidget):
    completion_signal = pyqtSignal()

    def __init__(self, user_id=None, room_name="Toothbrushing"):
        super().__init__()
        self.user_id = user_id
        self.room_id = get_room_id_by_name(room_name)
        self.current_step = 0
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.steps = [
            "Show the toothbrush with toothpaste on it.",
            "Brush the upper and lower left side of the teeth back and forth 5 times.",
            "Brush the upper and lower right side of the teeth back and forth 5 times.",
            "Brush the front part of the teeth gently in small circles 5 times.",
            "Brush the chewing surfaces of the teeth for 20 seconds.",
            "Spit out excess toothpaste and rinse the mouth with water.",
        ]
        self.images = [
            "../resources/images/badges/locked.png",
            "../resources/images/badges/locked.png",
            "../resources/images/badges/locked.png",
            "../resources/images/badges/locked.png",
            "../resources/images/badges/locked.png",
            "../resources/images/badges/locked.png",
        ]
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        instructions_layout = QVBoxLayout()
        for i, step in enumerate(self.steps):
            instructions_layout.addWidget(QLabel(f"{i+1}. {step}"))

        self.start_button = QPushButton("Start Toothbrushing")
        self.start_button.clicked.connect(self.on_start)
        instructions_layout.addWidget(self.start_button)

        camera_layout = QVBoxLayout()
        self.camera_label = QLabel()
        camera_layout.addWidget(self.camera_label)

        main_layout.addLayout(instructions_layout)
        main_layout.addLayout(camera_layout)

        self.setLayout(main_layout)


    def on_start(self):
        self.start_button.setDisabled(True)
        self.start_camera()
        self.show_next_step()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            qt_image = self.convert_cv_qt(frame)
            self.camera_label.setPixmap(qt_image)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def show_next_step(self):
        if self.current_step < len(self.steps):
            pixmap = QPixmap(self.images[self.current_step]).scaled(640, 480, Qt.KeepAspectRatio)
            self.show_prompt(self.steps[self.current_step], pixmap)
        else:
            self.completion_signal.emit()

    def show_prompt(self, text, pixmap):
        msg = QMessageBox(self)
        msg.setWindowTitle(f"Step {self.current_step + 1}")
        msg.setText(text)
        msg.setIconPixmap(pixmap)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.on_prompt_close)
        msg.exec_()

    def on_prompt_close(self, i):
        self.current_step += 1
        self.show_next_step()

    def room_completed(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Room Completed")
        msg.setText("3 stars earned! You have completed the room, Congratulations!!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.on_finish)
        msg.exec_()

    def on_finish(self, i):
        # Use the room_id fetched during initialization
        if self.room_id is not None:
            complete_room_for_user(self.user_id, self.room_id)
        else:
            print("Error: Room ID could not be found.")


    def closeEvent(self, event):
        self.timer.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()
        
        msg = QMessageBox()
        msg.setWindowTitle("Room Completed")
        msg.setText("Congratulations!! You have completed the room, 3 stars earned!")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        # Send notification when the room is closed
        send_notification(
            title='Toothbrushing Session Ended',
            message='Your toothbrushing session has just ended.'
        )

        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tb_room = ToothbrushingRoom(user_id=1)
    tb_room.show()
    sys.exit(app.exec_())
