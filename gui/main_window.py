from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.components.analysis import AnalysisView
from gui.components.data_view import DataView
from gui.components.upload_view import UploadView


class MainWindow(ttk.Frame):
    """
    Main application window that sets up the user interface based on the user's role.
    """

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
        """
        Sets up the UI components of the main window.
        """
        # Display welcome message
        self._display_welcome_message()

        # Create tabbed interface
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Add appropriate tabs based on the user's role
        self._add_tabs(notebook)

        # Add logout button
        self._add_logout_button()

    def _display_welcome_message(self):
        """
        Displays a welcome message with the user's information.
        """
        welcome_label = ttk.Label(
            self,
            text=f"Welcome, {self.user_info['username']} ({self.user_info['role'].capitalize()})",
            font=("TkDefaultFont", 16, "bold"),
            anchor="center"
        )
        welcome_label.pack(pady=10)

    def _add_tabs(self, notebook):
        """
        Adds tabs to the notebook based on the user's role.

        :param notebook: The ttk.Notebook widget where tabs are added.
        """
        if self.user_info["role"] in ["admin", "viewer"]:
            # Add data viewer tab
            data_view_tab = DataView(notebook, self.db_connection)
            notebook.add(data_view_tab, text="Data Viewer")

            # Add data analysis tab
            analysis_tab = AnalysisView(notebook, self.db_connection)
            notebook.add(analysis_tab, text="Data Analysis")

        if self.user_info["role"] == "admin":
            # Add data upload tab for admin users
            upload_tab = UploadView(notebook, self.db_connection)
            notebook.add(upload_tab, text="Upload Data")

    def _add_logout_button(self):
        """
        Adds a logout button at the bottom of the window.
        """
        logout_button = ttk.Button(
            self,
            text="Logout",
            command=self.logout,
            style="danger.TButton"
        )
        logout_button.pack(pady=10)

    def logout(self):
        """
        Handles the logout logic by destroying the main window and displaying a confirmation message.
        """
        self.destroy()
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")