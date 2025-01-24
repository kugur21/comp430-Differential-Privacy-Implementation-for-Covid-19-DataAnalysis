import tkinter as tk
from ttkbootstrap import Style
from gui.login import LoginScreen
from gui.main_window import MainWindow
from database.connection import DatabaseConnection
from database.initializer import initialize_database, load_data

#project
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = Style("cosmo")  # Apply a ttkbootstrap theme
        self.title("Privacy-Preserving COVID-19 Data Analysis")
        self.geometry("1400x1200")

        # Database connection
        self.db = DatabaseConnection()
        if not self.db.connect():
            print("Failed to connect to the database. Exiting.")
            self.destroy()
            return

        # Initialize the database schema
        self.initialize_database()

        self.load_account_and_covid_data()

        # Initialize the app with the login screen
        self.current_frame = None
        self.show_login_screen()

    def initialize_database(self):
        """
        Initializes the database schema by creating tables if they don't exist.
        """
        try:
            initialize_database(self.db)
            print("Database schema initialized successfully.")
        except Exception as e:
            print(f"Error initializing database schema: {e}")
            self.destroy()


    def load_account_and_covid_data(self):
        """
        Loads the patient dataset into the database.
        """
        try:
            covid_data_csv_path = "reducedCovidData.csv"
            accounts_csv_path = "accounts.csv"
            load_data(self.db, accounts_csv_path, covid_data_csv_path)

        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.destroy()

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


if __name__ == "__main__":
    # Initialize the application
    app = Application()

    # Handle cleanup on close
    app.protocol("WM_DELETE_WINDOW", app.on_close)

    # Run the application
    app.mainloop()