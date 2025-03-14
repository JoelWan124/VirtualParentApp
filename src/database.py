import sqlite3
import hashlib

DATABASE_NAME = "virtual_parent.db"

#hihihiihihi
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
    new_user_id = None
    if conn:
        try:
            sql = "INSERT INTO users (username, password) VALUES (?, ?)"
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            cursor.execute(sql, (username, hashed_password))
            conn.commit()
            new_user_id = cursor.lastrowid
            print(f"User '{username}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    return new_user_id

def register_user(username, password):
    """Register a new user and create default entries in all relevant tables."""
    user_id = add_new_user(username, password)
    if user_id:
        create_default_settings_for_user(user_id)
        initialize_achievements_for_user(user_id)
        initialize_activity_history_for_user(user_id)
        initialize_routines_for_user(user_id)
        return user_id
    return None

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
            sql = """
            UPDATE settings
            SET notifications_enabled = ?, dayRoutineReminder = ?, nightRoutineReminder = ?
            WHERE user_id = ?
            """
            cursor = conn.cursor()
            notifications_value = 1 if notifications_enabled else 0
            # Execute the update statement
            cursor.execute(sql, (notifications_value, day_time, night_time, user_id))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"No settings found for user_id {user_id}. Creating new settings row.")
                create_default_settings_for_user(user_id, notifications_value, day_time, night_time)
            else:
                print(f"Updated settings for user_id {user_id}")
            return True
        except sqlite3.Error as e:
            print(f"An error occurred while updating settings: {e}")
            return False
        finally:
            conn.close()


def create_default_settings_for_user(user_id, notifications_enabled=True, day_time='08:00', night_time='20:00'):
    """Create default settings for a user."""
    conn = create_connection()
    assert conn, "Failed to connect to the database."
    if conn:
        try:
            sql = """
            INSERT INTO settings (user_id, notifications_enabled, dayRoutineReminder, nightRoutineReminder)
            VALUES (?, ?, ?, ?)
            """
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, int(notifications_enabled), day_time, night_time))
            conn.commit()
            assert cursor.rowcount == 1, "Failed to insert default settings."
            print(f"Created default settings for user_id {user_id}")
        except sqlite3.Error as e:
            print(f"An error occurred while creating default settings: {e}")
        finally:
            conn.close()



def initialize_achievements_for_user(user_id):
    """Initialize default achievements for the user."""
    conn = create_connection()
    assert conn, "Failed to connect to the database."
    if conn:
        try:
            achievements = [("First Login",), ("First Activity",), ("First Week",)]
            cursor = conn.cursor()
            cursor.executemany(
                "INSERT INTO achievements (user_id, achievement) VALUES (?, ?)",
                [(user_id, achievement) for achievement in achievements]
            )
            conn.commit()
            cursor.execute("SELECT COUNT(*) FROM achievements WHERE user_id = ?", (user_id,))
            count = cursor.fetchone()[0]
            assert count > 0, "No achievements initialized for user."
            print(f"Initialized default achievements for user_id {user_id}")
        except sqlite3.Error as e:
            print(f"An error occurred while initializing achievements: {e}")
        finally:
            conn.close()



def initialize_activity_history_for_user(user_id):
    """Initialize the activity history for the user."""
    conn = create_connection()
    assert conn, "Failed to connect to the database."
    if conn:
        try:
            cursor = conn.cursor()
            # Insert a default entry into activityHistories
            cursor.execute(
                "INSERT INTO activityHistories (user_id, date, activitiesCompleted) VALUES (?, ?, ?)",
                (user_id, "2024-01-01", "Registered")
            )
            conn.commit()
            assert cursor.rowcount == 1, "Failed to insert activity history."
            print(f"Initialized activity history for user_id {user_id}")
        except sqlite3.Error as e:
            print(f"An error occurred while initializing activity history: {e}")
        finally:
            conn.close()


def initialize_routines_for_user(user_id):
    """Initialize default routines for the user."""
    conn = create_connection()
    assert conn, "Failed to connect to the database."
    if conn:
        try:
            cursor = conn.cursor()
            # Insert a default entry into routines
            cursor.execute(
                "INSERT INTO routines (user_id, routineType, startTime, endTime) VALUES (?, ?, ?, ?)",
                (user_id, "day", "08:00", "09:00")
            )
            conn.commit()
            assert cursor.rowcount == 1, "Failed to insert routines."
            print(f"Initialized default routines for user_id {user_id}")
        except sqlite3.Error as e:
            print(f"An error occurred while initializing routines: {e}")
        finally:
            conn.close()




def print_user_day_time(user_id):
    """Print the day routine notification time for a user."""
    settings = get_user_settings(user_id)
    if settings:
        print(f"Day routine notification time for user_id {user_id} is: {settings[1]}")
    else:
        print(f"No settings found for user_id {user_id}.")


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
            sql = "SELECT notifications_enabled, dayRoutineReminder, nightRoutineReminder FROM settings WHERE user_id = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            print(f"Fetched settings for user_id {user_id}: {result}")
            return result
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()
    else:
        print("Failed to create database connection.")
        return None
    


def get_notification_times_from_db(user_id):
    """Retrieve the notification times and enabled status for a user."""
    conn = create_connection()
    if conn:
        try:
            sql = """
            SELECT notifications_enabled, dayRoutineReminder, nightRoutineReminder
            FROM settings
            WHERE user_id = ?
            """
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if result:
                notifications_enabled, day_time, night_time = result
                return {
                    "enabled": notifications_enabled,
                    "day_time": day_time,
                    "night_time": night_time
                }
            else:
                return None
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            conn.close()

def get_room_id_by_name(room_name):
    """Fetch the room_id from the database based on the roomName."""
    conn = create_connection()
    room_id = None
    if conn:
        try:
            sql = "SELECT room_id FROM rooms WHERE roomName = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (room_name,))
            result = cursor.fetchone()
            if result:
                room_id = result[0]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return room_id

def complete_room_for_user(user_id, room_id, stars_earned=3, status=True):
    """Mark a room as completed for a user."""
    conn = create_connection()
    if conn:
        try:
            # First, check if the userRoom entry exists
            sql_check = "SELECT userRoom_id FROM userRooms WHERE user_id = ? AND room_id = ?"
            cursor = conn.cursor()
            cursor.execute(sql_check, (user_id, room_id))
            result = cursor.fetchone()

            if result is None:
                # Insert a new entry if it doesn't exist
                sql_insert = """INSERT INTO userRooms (user_id, room_id, starEarned, status)
                                VALUES (?, ?, ?, ?)"""
                cursor.execute(sql_insert, (user_id, room_id, stars_earned, status))
            else:
                # Update the existing entry
                sql_update = """UPDATE userRooms
                                SET starEarned = ?, status = ?
                                WHERE user_id = ? AND room_id = ?"""
                cursor.execute(sql_update, (stars_earned, status, user_id, room_id))

            conn.commit()
            print(f"Room completion updated successfully for user_id {user_id} and room_id {room_id}.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            
def insert_test_user_room(user_id, room_id, stars_earned, status):
    """Insert a test entry into the userRooms table."""
    conn = create_connection()
    if conn:
        try:
            sql = """
            INSERT INTO userRooms (user_id, room_id, starEarned, status)
            VALUES (?, ?, ?, ?)
            """
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, room_id, stars_earned, status))
            conn.commit()
            print("Test entry added to userRooms table.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

def fetch_and_print_user_rooms(user_id):
    """Fetch and print all entries for a user from the userRooms table."""
    conn = create_connection()
    if conn:
        try:
            sql = "SELECT * FROM userRooms WHERE user_id = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    setup_database()

    # Run the test
    test_user_id = 8
    test_room_id = 1
    insert_test_user_room(test_user_id, test_room_id, 3, True)
    fetch_and_print_user_rooms(test_user_id)

