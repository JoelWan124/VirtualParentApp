# history.py
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView

class HistoryWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()
        self.populate_history()

    def init_ui(self):
        self.setWindowTitle("History")
        self.layout = QVBoxLayout()

        self.history_label = QLabel("Completed Rooms", self)
        self.layout.addWidget(self.history_label)

        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Date", "Room Name", "Stars Earned"])
        self.layout.addWidget(self.history_table)

        self.setLayout(self.layout)

    def populate_history(self):
        history_data = self.get_user_history_from_database()
        self.history_table.setRowCount(len(history_data))

        for row, (date, room_name, stars_earned) in enumerate(history_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(date))
            self.history_table.setItem(row, 1, QTableWidgetItem(room_name))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(stars_earned)))

        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_user_history_from_database(self):
        # Simulated test data
        simulated_history = [
            ("2024-04-25", "Toothbrushing(Day)", 3),
            ("2024-04-25", "Toothbrushing(Night)", 2),
            ("2024-04-24", "Energy Saving", 1),
            ("2024-04-23", "Healthy Eating", 3),
            ("2024-04-22", "Mindfulness", 2),
        ]
        return simulated_history

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    history_window = HistoryWindow(user_id=1)
    history_window.show()
    sys.exit(app.exec_())
