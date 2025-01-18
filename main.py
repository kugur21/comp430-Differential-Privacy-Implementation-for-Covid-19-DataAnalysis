#!/usr/bin/env python3

import tkinter as tk
from ttkbootstrap import Style
from gui.login import LoginScreen
from gui.main_window import MainWindow
from database.connection import DatabaseConnection
from utils.security import hash_password

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = Style("cosmo")  # Apply a ttkbootstrap theme
        self.title("Privacy-Preserving COVID-19 Data Analysis")
        self.geometry("800x600")

        # Database connection
        self.db = DatabaseConnection()
        if not self.db.connect():
            print("Failed to connect to the database. Exiting.")
            self.destroy()
            return

        # Initialize the app with the login screen
        self.current_frame = None
        self.show_login_screen()

    def show_login_screen(self):
        """Displays the login screen."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginScreen(self, self.db, self.on_login_success)
        self.current_frame.pack(fill="both", expand=True)

    def show_main_window(self, user_info):
        """Displays the main application window."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainWindow(self, self.db, user_info)
        self.current_frame.pack(fill="both", expand=True)

    def on_login_success(self, user_info):
        """Handles successful login and transitions to the main window."""
        self.show_main_window(user_info)

    def on_close(self):
        """Handles application cleanup on close."""
        if self.db:
            self.db.close()
        self.destroy()

def setup_default_admin(db):
    """
    Creates a default admin user if no users exist in the database.
    """
    query = "SELECT COUNT(*) AS user_count FROM Users"
    db.execute_query(query)
    result = db.cursor.fetchone()
    user_count = result["user_count"]  # Access the dictionary key

    if user_count == 0:
        username = "admin"
        password = "admin123"
        hashed_password = hash_password(password)

        insert_query = """
            INSERT INTO Users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """
        db.execute_query(insert_query, (username, hashed_password, "admin"))
        print(f"Default admin user created:\nUsername: {username}\nPassword: {password}")

if __name__ == "__main__":
    # Initialize the application
    app = Application()

    # Create default admin if necessary
    setup_default_admin(app.db)

    # Handle cleanup on close
    app.protocol("WM_DELETE_WINDOW", app.on_close)

    # Run the application
    app.mainloop()
