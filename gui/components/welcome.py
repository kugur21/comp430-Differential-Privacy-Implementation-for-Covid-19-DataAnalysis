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

        self.configure(bootstyle="dark")

        welcome_label = ttk.Label(
            self,
            text="Welcome to the Differential Privacy Implementation Project!",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=20)

        description_label = ttk.Label(
            self,
            text=(
                "This application is designed to demonstrate the implementation of differential privacy "
                "techniques on COVID-19 datasets. Differential privacy is a system for publicly sharing "
                "information about a dataset by describing the patterns of groups within the dataset "
                "while withholding information about individuals in the dataset. This application "
                "provides tools for secure data upload, detailed data visualization, and privacy-preserving "
                "data analysis. By using this application, you can explore how differential privacy "
                "can be applied to real-world data while ensuring the privacy of individuals."
            ),
            wraplength=800,
            justify="center",
            font=("Helvetica", 14),
            bootstyle="light"
        )
        description_label.pack(pady=15)


        tabs_label = ttk.Label(
            self,
            text="Here is what each tab does in detail:",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        )
        tabs_label.pack(pady=(20, 10))

        tabs_description = (
            "Data Analysis Tab: The Data Analysis tab provides a privacy-preserving framework for various analyses on medical data, leveraging differential privacy mechanisms such as Gaussian, Laplace, Exponential, and Report Noisy Max to ensure data confidentiality. This section supports multiple analyses, including age distribution, ICU statistics, disease correlation, gender-based ICU analysis, recovery and mortality rates, and high-risk survivor identification, among others. It dynamically generates visualizations, such as bar charts, pie charts, and time series plots, with enhanced aesthetics. The UI includes a control panel for selecting analyses, adjusting privacy budgets (ε), and displaying progress, results, and visualizations in an interactive and user-friendly layout. The privacy-preserving computations integrate database queries and noise injection, ensuring robust differential privacy compliance for sensitive medical datasets.\n\n"
            "Dynamic Analysis Tab: The Dynamic Analysis tab supports various analyses, including age and patient type analysis, disease and classification correlation, gender and tobacco impact, death counts over a date range, and ICU and comorbidity trends. This section leverages differential privacy mechanisms to protect sensitive data during analyses, ensuring compliance with privacy standards. Users can dynamically input parameters such as age ranges, medical conditions, and date ranges through prompts, and adjust the privacy budget (ε) using a slider. It features a responsive UI with sections for analysis selection, results, and graphical visualizations, which are rendered using Matplotlib with modern aesthetics and integrated into the application. The modular design makes it versatile for handling various data queries while maintaining user-friendly interaction and a focus on data security.\n\n"
        )
        tabs_text = ttk.Label(
            self,
            text=tabs_description,
            justify="left",
            wraplength=800,
            font=("Helvetica", 14),
            bootstyle="light"
        )
        tabs_text.pack(pady=10)

        footer_label = ttk.Label(
            self,
            text=(
                "Thank you for using this application! We hope it provides valuable insights "
                "into how differential privacy can be applied to real-world datasets. "
            ),
            wraplength=800,
            justify="center",
            font=("Helvetica", 14, "italic"),
            bootstyle="primary"
        )
        footer_label.pack(pady=30)