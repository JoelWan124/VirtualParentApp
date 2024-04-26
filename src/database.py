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
            user_id INTEGER NOT NULL,
            notifications_enabled BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
        try:
            cursor = conn.cursor()
            cursor.execute(create_user_table)
            cursor.execute(create_achievements_table)
            cursor.execute(create_settings_table)
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
            return True
        except sqlite3.IntegrityError:
            print("Username already exists.")
            return False
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

def check_user_credentials(username, password):
    """Check if a user's login credentials are valid, comparing hashed passwords."""
    conn = create_connection()
    if conn:
        try:
            sql = "SELECT password FROM users WHERE username = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result and result[0] == hash_password(password):
                return True
            return False
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    setup_database()
