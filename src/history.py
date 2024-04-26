# history.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView

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
        # Placeholder function - replace with actual database call
        return [("2024-04-26", "Toothbrushing", 3), ("2024-04-25", "Toothbrushing", 2)]
