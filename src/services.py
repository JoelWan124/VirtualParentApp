import schedule
import time
from threading import Thread
from plyer import notification
from database import get_notification_times_from_db
from threading import Thread

def send_notification(title, message):
    print(f"Sending notification: {title} - {message}")
    notification.notify(
        title=title,
        message=message,
        app_name='Virtual Parent App',
        timeout=10,
    )

def schedule_notifications(user_id): #
    send_notification('Immediate Test', 'If you see this, notifications are working!')
    settings = get_notification_times_from_db(user_id)
    if settings and settings["enabled"]:
        # Convert the boolean to Python's True/False
        notifications_enabled = settings["enabled"] == 1

        if notifications_enabled:
            #Debug Line below
            #schedule.every(10).seconds.do(send_notification, title='Test', message='This is a test notification BAHAHAHAHHAHAHAHAHAHAHAHAHAHA!')

            print(f"Scheduling day notification for {settings['day_time']}")
            print(f"Scheduling night notification for {settings['night_time']}")

            # Schedule day notification
            schedule.every().day.at(settings["day_time"]).do(
                send_notification, 
                title='Day Routine', 
                message='Time for your day hygiene routine!'
            )

            # Schedule night notification
            schedule.every().day.at(settings["night_time"]).do(
                send_notification, 
                title='Night Routine', 
                message='Time for your night hygiene routine!'
            )

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_notification_scheduler(user_id): #
    schedule_notifications(user_id) #
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

def closeEvent(self, event):
    self.timer.stop()
    if self.cap and self.cap.isOpened():
        self.cap.release()

    # Send notification when the room is closed
    send_notification(
        title='Toothbrushing Session Ended',
        message='Your toothbrushing session has just ended.'
    )


if __name__ == "__main__":
    # Testing 
    start_notification_scheduler(user_id=1) #
    input("Press Enter to exit...\n")
