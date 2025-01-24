import sys
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.components.analysis import AnalysisView
from gui.components.data_view import DataView
from gui.components.dynamicAnalysis import DynamicAnalysisView
from gui.components.upload_view import UploadView
from gui.components.welcome import WelcomeTab

class MainWindow(ttk.Frame):
    """
    Main application window that sets up the user interface based on the user's role.
    """

    def __init__(self, parent, db_connection, user_info):
        """
        Initializes the main application window.

        :param parent: The parent Tkinter container.
        :param db_connection: The database connection instance.
        :param user_info: Dictionary containing user information (e.g., user_id, username, role, budget).
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

        # Display privacy budget
        self._display_privacy_budget()

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

    def _display_privacy_budget(self):
        """
        Displays the privacy budget in the top-right corner.
        """
        self.privacy_budget_label = ttk.Label(
            self,
            text=f"Privacy Budget: {self.user_info['budget']} ε",
            font=("TkDefaultFont", 12),
            anchor="e"
        )
        self.privacy_budget_label.pack(side="top", anchor="ne", padx=10, pady=10)

    def _add_tabs(self, notebook):
        """
        Adds tabs to the notebook based on the user's role.

        :param notebook: The ttk.Notebook widget where tabs are added.
        """
        if self.user_info["role"] in ["admin", "viewer"]:
            # Add welcome tab
            welcome_tab = WelcomeTab(notebook)
            notebook.add(welcome_tab, text="Welcome")

            # Add data analysis tab
            analysis_tab = AnalysisView(notebook, self, self.db_connection)
            notebook.add(analysis_tab, text="Data Analysis")

            # Add dynamic analysis tab
            dynamic_analysis_tab = DynamicAnalysisView(notebook, self, self.db_connection)
            notebook.add(dynamic_analysis_tab, text="Dynamic Analysis")

        if self.user_info["role"] == "admin":
            # Add data upload tab for admin users
            upload_tab = UploadView(notebook, self.db_connection)
            notebook.add(upload_tab, text="Upload Data")

            # Add data viewer tab
            data_view_tab = DataView(notebook, self.db_connection)
            notebook.add(data_view_tab, text="Data Viewer")

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

    def update_privacy_budget(self, epsilon):
        """
        Updates the user's privacy budget in the database and the UI.

        :param epsilon: The privacy epsilon value.
        """
        try:
            # Update the budget in the database
            new_budget = self.user_info["budget"] - epsilon
            query = "UPDATE Users SET budget = %s WHERE username = %s"
            self.db_connection.execute_query(query, (new_budget, self.user_info["username"]))

            # Update the budget in the user_info dictionary
            self.user_info["budget"] = new_budget

            # Update the budget label in the UI
            self.privacy_budget_label.config(text=f"Privacy Budget: {new_budget} ε")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update privacy budget: {e}")

    def logout(self):
        """
        Handles the logout logic by destroying the main window.
        """
        self.destroy()
        sys.exit(0)

