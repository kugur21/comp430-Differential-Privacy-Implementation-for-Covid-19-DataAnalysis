import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class WelcomeTab(ttk.Frame):
    """
    A tab that introduces the project and explains the purpose of other tabs.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the UI elements for the welcome tab.
        """
        # Welcome Message
        welcome_label = ttk.Label(
            self,
            text="Welcome to the Differential Privacy Implementation Project!",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=10)

        # Project Description
        description_label = ttk.Label(
            self,
            text=(
                "This application demonstrates the implementation of differential privacy "
                "techniques on COVID-19 data. It provides tools for data analysis, visualization, "
                "and secure data upload."
            ),
            wraplength=600,
            justify="left"
        )
        description_label.pack(pady=10)

        # Tab Explanation
        tabs_label = ttk.Label(
            self,
            text="Here is what each tab does:",
            font=("Helvetica", 12, "bold")
        )
        tabs_label.pack(pady=10)

        # Tabs Description
        tabs_description = (
            "- Upload: Securely upload datasets for analysis.\n"
            "- Data View: Explore and visualize the dataset.\n"
            "- Analysis: Perform privacy-preserving data analysis."
        )
        tabs_text = ttk.Label(
            self,
            text=tabs_description,
            justify="left",
            wraplength=600
        )
        tabs_text.pack(pady=10)

        # Footer
        footer_label = ttk.Label(
            self,
            text="Thank you for using this application!",
            font=("Helvetica", 10, "italic")
        )
        footer_label.pack(pady=20)