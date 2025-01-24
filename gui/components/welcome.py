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
        # Arka plan rengini karanlık tema ile uyumlu yap
        self.configure(bootstyle="dark")  # Karanlık tema

        # Welcome Message (Mavi renkli başlık)
        welcome_label = ttk.Label(
            self,
            text="Welcome to the Differential Privacy Implementation Project!",
            font=("Helvetica", 20, "bold"),  # Daha büyük font boyutu
            bootstyle="primary"  # Mavi renk
        )
        welcome_label.pack(pady=20)  # Daha fazla padding

        # Project Description
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
            wraplength=800,  # Daha geniş bir alana yay
            justify="center",  # Metni ortala
            font=("Helvetica", 14),  # Daha büyük font boyutu
            bootstyle="light"  # Beyaz yazı
        )
        description_label.pack(pady=15)  # Daha fazla padding

        # Tab Explanation (Mavi renkli başlık)
        tabs_label = ttk.Label(
            self,
            text="Here is what each tab does in detail:",
            font=("Helvetica", 16, "bold"),  # Daha büyük font boyutu
            bootstyle="primary"  # Mavi renk
        )
        tabs_label.pack(pady=(20, 10))  # Daha fazla padding

        # Tabs Description
        tabs_description = (
            "- **Upload Tab**: This tab allows you to securely upload your datasets for analysis. "
            "The data is encrypted during the upload process to ensure privacy and security. "
            "You can upload CSV or Excel files containing COVID-19 data, and the application "
            "will process them for further analysis.\n\n"
            "- **Data View Tab**: In this tab, you can explore and visualize the uploaded dataset. "
            "The application provides various visualization tools, such as bar charts, pie charts, "
            "and time series plots, to help you understand the data better. You can also filter "
            "and sort the data based on different criteria.\n\n"
            "- **Analysis Tab**: This tab is dedicated to performing privacy-preserving data analysis. "
            "You can apply differential privacy techniques to the dataset and generate insights "
            "while ensuring that individual data points remain private. The analysis includes "
            "statistical summaries, trend analysis, and more."
        )
        tabs_text = ttk.Label(
            self,
            text=tabs_description,
            justify="left",
            wraplength=800,  # Daha geniş bir alana yay
            font=("Helvetica", 14),  # Daha büyük font boyutu
            bootstyle="light"  # Beyaz yazı
        )
        tabs_text.pack(pady=10)

        # Footer (Mavi renkli teşekkür mesajı)
        footer_label = ttk.Label(
            self,
            text=(
                "Thank you for using this application! We hope it provides valuable insights "
                "into how differential privacy can be applied to real-world datasets. "
                "If you have any questions or feedback, please feel free to contact us."
            ),
            wraplength=800,  # Daha geniş bir alana yay
            justify="center",  # Metni ortala
            font=("Helvetica", 14, "italic"),  # Daha büyük font boyutu
            bootstyle="primary"  # Mavi renk
        )
        footer_label.pack(pady=30)  # Daha fazla padding