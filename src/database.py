import sqlite3
import hashlib

DATABASE_NAME = "virtual_parent.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        print(e)
    return conn

def setup_database():
    """Create tables in the database if they do not exist."""
    conn = create_connection()
    if conn:
        create_user_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
        create_achievements_table = """
        CREATE TABLE IF NOT EXISTS achievements (
            user_id INTEGER NOT NULL,
            achievement TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        create_settings_table = """
        CREATE TABLE IF NOT EXISTS settings (
            setting_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            notifications_enabled BOOLEAN NOT NULL DEFAULT 1,
            dayRoutineReminder TEXT DEFAULT '08:00', 
            nightRoutineReminder TEXT DEFAULT '20:00',
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        create_routine_table = """
        CREATE TABLE IF NOT EXISTS routines (
            routine_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            routineType TEXT CHECK(routineType IN ('day','Night')),
            startTime TEXT,
            endTime TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """

        create_room_table = """
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY,
            roomName TEXT,
            routineType TEXT
        );
        """

        create_userRoom_table = """
        CREATE TABLE IF NOT EXISTS userRooms (
            userRoom_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            room_id INTEGER,
            starEarned INTEGER,
            completionDate TEXT,
            status BOOLEAN,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (room_id) REFERENCES rooms (room_id)
        );
        """

        create_activityHistory_table = """
        CREATE TABLE IF NOT EXISTS activityHistories (
            history_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            date TEXT,
            activitiesCompleted TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """


        try:
            cursor = conn.cursor()
            cursor.execute(create_user_table)
            cursor.execute(create_achievements_table)
            cursor.execute(create_settings_table)
            cursor.execute(create_routine_table)
            cursor.execute(create_room_table)
            cursor.execute(create_userRoom_table)
            cursor.execute(create_activityHistory_table)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def hash_password(password):
    """Return the SHA-256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_new_user(username, password):
    """Add a new user to the database with hashed password."""
    conn = create_connection()
    if conn:
        try:
            sql = "INSERT INTO users (username, password) VALUES (?, ?)"
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute(sql, (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
            return False
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        else:
            print(f"User '{username}' added successfully.")
            return True
        finally:
            conn.close()


def check_user_credentials(username, password):
    """Check if a user's login credentials are valid, comparing hashed passwords, and return user ID or False."""
    conn = create_connection()
    if conn:
        try:
            sql = "SELECT id, password FROM users WHERE username = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result and result[1] == hash_password(password):
                return result[0]  # Return the user ID
            return False  # Return False if password does not match
        except sqlite3.Error as e:
            print(e)
            return False  # Return False if an error occurs
        finally:
            conn.close()

def update_user_settings(user_id, notifications_enabled, day_time, night_time):
    """Update the settings for a user."""
    conn = create_connection()
    if conn:
        try:
            sql = """UPDATE settings SET notifications_enabled = ?, dayRoutineReminder = ?, nightRoutineReminder = ?
                     WHERE user_id = ?"""
            cursor = conn.cursor()
            cursor.execute(sql, (notifications_enabled, day_time, night_time, user_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

def get_room_completion_status(user_id, room_name):
    """Get the completion status of a room for a given user."""
    conn = create_connection()
    if conn:
        try:
            sql = """SELECT status FROM userRooms 
                     JOIN rooms ON userRooms.room_id = rooms.room_id 
                     WHERE user_id = ? AND roomName = ?"""
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, room_name))
            result = cursor.fetchone()
            conn.close()  # Close the connection after executing the query
            if result is not None:
                return result[0]  # Return the status if found
            else:
                return None  # Return None if there is no such entry
        except sqlite3.Error as e:
            print(e)
            return None  # Return None if an error occurs
    else:
        print("Failed to create database connection.")
        return None


def get_user_settings(user_id):
    """Retrieve the settings for a user."""
    conn = create_connection()
    if conn:
        try:
            sql = "SELECT notifications_enabled, day_notification_time, night_notification_time FROM settings WHERE user_id = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()


if __name__ == "__main__":
    setup_database()
