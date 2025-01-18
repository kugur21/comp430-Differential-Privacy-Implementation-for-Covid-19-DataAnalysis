from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.components.data_view import DataView
from gui.components.analysis import AnalysisView
from gui.components.upload_view import UploadView

class MainWindow(ttk.Frame):
    def __init__(self, parent, db_connection, user_info):
        """
        Initializes the main application window.
        :param parent: The parent Tkinter container.
        :param db_connection: The database connection instance.
        :param user_info: Dictionary containing user information (e.g., user_id, username, role).
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.user_info = user_info
        self.setup_ui()

    def setup_ui(self):
        # Welcome message
        welcome_label = ttk.Label(
            self,
            text=f"Welcome, {self.user_info['username']} ({self.user_info['role'].capitalize()})",
            font=("TkDefaultFont", 16, "bold"),
            anchor="center"
        )
        welcome_label.pack(pady=10)

        # Create Notebook (tabbed interface)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs based on role
        if self.user_info["role"] in ["admin", "viewer"]:
            data_view_tab = DataView(notebook, self.db_connection)
            notebook.add(data_view_tab, text="Data Viewer")

            analysis_tab = AnalysisView(notebook, self.db_connection)
            notebook.add(analysis_tab, text="Data Analysis")

        if self.user_info["role"] == "admin":
            upload_tab = UploadView(notebook, self.db_connection)
            notebook.add(upload_tab, text="Upload Data")

        # Logout Button
        logout_button = ttk.Button(self, text="Logout", command=self.logout, style="danger.TButton")
        logout_button.pack(pady=10)

    def logout(self):
        # Handle logout logic
        self.destroy()
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
