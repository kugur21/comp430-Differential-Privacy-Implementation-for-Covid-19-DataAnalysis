import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from privacy.differential_privacy import apply_differential_privacy

class AnalysisView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ttk.Label(self, text="Data Analysis", font=("TkDefaultFont", 16, "bold"))
        title.pack(pady=10)

        # Dropdown for analysis selection
        self.analysis_options = ["Age Distribution", "ICU Statistics"]
        self.analysis_var = ttk.StringVar(value=self.analysis_options[0])
        analysis_dropdown = ttk.Combobox(self, textvariable=self.analysis_var, values=self.analysis_options)
        analysis_dropdown.pack(pady=5)

        # Button to run analysis
        run_button = ttk.Button(self, text="Run Analysis", command=self.run_analysis, style="primary.TButton")
        run_button.pack(pady=10)

        # Results display area
        self.result_text = ttk.Text(self, height=15, width=50)
        self.result_text.pack(pady=10)

    def run_analysis(self):
        selected_analysis = self.analysis_var.get()
        self.result_text.delete(1.0, "end")

        # Perform the analysis and apply differential privacy
        if selected_analysis == "Age Distribution":
            result = self.perform_age_distribution()
        elif selected_analysis == "ICU Statistics":
            result = self.perform_icu_statistics()
        else:
            result = "Invalid Analysis Selected"

        self.result_text.insert("end", result)

    def perform_age_distribution(self):
        # Query the database for patient ages and apply Gaussian noise
        query = "SELECT age FROM Patients WHERE age IS NOT NULL"
        self.db_connection.execute_query(query)
        ages = [row['age'] for row in self.db_connection.cursor.fetchall()]
        return apply_differential_privacy(ages, mechanism="Gaussian", epsilon=1.0)

    def perform_icu_statistics(self):
        # Query the database for ICU counts and apply Laplace noise
        query = "SELECT COUNT(*) AS icu_count FROM Patients WHERE icu = 1"
        self.db_connection.execute_query(query)
        icu_count = self.db_connection.cursor.fetchone()['icu_count']
        return apply_differential_privacy([icu_count], mechanism="Laplace", epsilon=1.0)
