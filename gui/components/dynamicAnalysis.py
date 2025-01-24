import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from privacy.differential_privacy import apply_differential_privacy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import simpledialog  # Import simpledialog from tkinter

class DynamicAnalysisView(ttk.Frame):
    def __init__(self, parent, mainWindow, db_connection):
        super().__init__(parent, padding="20")
        self.mainWindow = mainWindow
        self.db_connection = db_connection
        self.current_canvas = None
        self.epsilon = 1.0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.style = ttk.Style()
        self.setup_ui()

    def setup_ui(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        title = ttk.Label(
            header_frame,
            text="Dynamic Analysis",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=(0, 10))

        self.analysis_options = [
            "Age and Patient Type Analysis",
            "Disease and Classification Analysis",
            "Gender and Tobacco Analysis",
            "Death Count Analysis",
            "ICU and Comorbidity Analysis"
        ]
        self.analysis_var = ttk.StringVar(value=self.analysis_options[0])

        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))

        epsilon_frame = ttk.Frame(control_frame)
        epsilon_frame.pack(pady=(0, 10))

        epsilon_label = ttk.Label(
            epsilon_frame,
            text="Privacy Budget (ε):",
            font=("Helvetica", 10)
        )
        epsilon_label.pack(side="left", padx=(0, 10))

        self.epsilon_var = ttk.IntVar(value=1)
        epsilon_slider = ttk.Scale(
            epsilon_frame,
            from_=1,
            to=10,
            orient='horizontal',
            variable=self.epsilon_var,
            command=self._update_epsilon_label,
            bootstyle="primary"
        )
        epsilon_slider.pack(side="left")

        self.epsilon_value_label = ttk.Label(
            epsilon_frame,
            text=str(self.epsilon_var.get()),
            font=("Helvetica", 10)
        )
        self.epsilon_value_label.pack(side="left", padx=(10, 0))

        analysis_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.analysis_var,
            values=self.analysis_options,
            width=30,
            font=("Helvetica", 12),
            bootstyle="primary"
        )
        analysis_dropdown.pack(pady=(0, 10))

        self.input_frame = ttk.Frame(control_frame)
        self.input_frame.pack(pady=(0, 10))

        run_button = ttk.Button(
            control_frame,
            text="Run Analysis",
            command=self.run_analysis,
            bootstyle="primary-outline",
            width=20
        )
        run_button.pack(pady=(0, 10))


        results_frame = ttk.LabelFrame(
            self,
            text="Analysis Results",
            padding="10",
            bootstyle="primary"
        )
        results_frame.grid(row=1, column=1, padx=(10, 0), sticky="nsew")

        results_frame.grid_propagate(False)
        results_frame.config(width=300, height=200)

        self.result_text = ttk.ScrolledText(
            results_frame,
            height=8,
            width=40,
            wrap="word",
            font=("Helvetica", 11),
        )
        self.result_text.pack(fill="both", expand=True)


        graph_frame = ttk.LabelFrame(
            self,
            text="Visualization",
            padding="10",
            bootstyle="primary"
        )
        graph_frame.grid(row=2, column=0, columnspan=2, padx=(10, 0), sticky="nsew")

        graph_frame.grid_propagate(False)
        graph_frame.config(width=700, height=500)

        self.graph_frame = ttk.Frame(graph_frame)
        self.graph_frame.pack(fill="both", expand=True)

        self.status_label = ttk.Label(
            self,
            text="Ready",
            font=("Helvetica", 10),
            bootstyle="secondary"
        )
        self.status_label.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    def _update_epsilon_label(self, event=None):
        """Callback to update the epsilon label whenever the slider moves."""
        self.epsilon_value_label.config(text=str(self.epsilon_var.get()))

    def run_analysis(self):
        self.epsilon = float(self.epsilon_var.get())
        selected_analysis = self.analysis_var.get()

        self.result_text.delete(1.0, "end")
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        try:
            if selected_analysis == "Age and Patient Type Analysis":
                result = self.perform_age_patient_type_analysis()
            elif selected_analysis == "Disease and Classification Analysis":
                result = self.perform_disease_classification_analysis()
            elif selected_analysis == "Gender and Tobacco Analysis":
                result = self.perform_gender_tobacco_analysis()
            elif selected_analysis == "Death Count Analysis":
                result = self.perform_death_count_analysis()
            elif selected_analysis == "ICU and Comorbidity Analysis":
                result = self.perform_icu_comorbidity_analysis()
            else:
                result = "Invalid Analysis Selected"

            self.result_text.insert("end", str(result))
            self.status_label.configure(
                text=f"Analysis completed successfully (ε={self.epsilon:.2f})",
                bootstyle="success"
            )

        except Exception as e:
            self.result_text.insert("end", f"Error: {str(e)}")
            self.status_label.configure(
                text="Error occurred during analysis",
                bootstyle="danger"
            )


    def perform_age_patient_type_analysis(self):
        """Query: Age and Patient Type Analysis"""
        min_age = self.get_input("Enter minimum age:", int)
        max_age = self.get_input("Enter maximum age:", int)
        patient_type = self.get_input("Enter patient type (1 for home, 2 for hospitalization):", int)

        if not self.mainWindow.update_privacy_budget(self.epsilon):
            return "Privacy budget exceeded. Please reduce the epsilon value."

        query = f"""
        SELECT 
            COUNT(*) AS Patient_Count
        FROM Patients
        WHERE AGE BETWEEN {min_age} AND {max_age}
          AND PATIENT_TYPE = {patient_type};
        """
        self.db_connection.execute_query(query)
        result = self.db_connection.cursor.fetchone()

        if not result:
            return "No data available for the given criteria."

        dp_result = apply_differential_privacy(
            self.db_connection,
            [result["Patient_Count"]],
            mechanism="Laplace",
            epsilon=self.epsilon,
            query=query
        )[0]

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.bar(
            [f"Age {min_age}-{max_age}"],
            [dp_result],
            color='#3498db',
            edgecolor='black'
        )
        ax.set_title(f"Patient Count (ε={self.epsilon:.2f})", fontsize=12, pad=10)
        ax.set_xlabel("Age Group", fontsize=10)
        ax.set_ylabel("Noisy Patient Count", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.display_graph(fig)

        return f"Patient Count (ε={self.epsilon:.2f}): {dp_result}"

    def perform_disease_classification_analysis(self):
        """Query: Disease and Classification Analysis"""
        diabetes = self.get_input("Enter diabetes status (1 for yes, 2 for no):", int)
        obesity = self.get_input("Enter obesity status (1 for yes, 2 for no):", int)
        cardio = self.get_input("Enter cardiovascular status (1 for yes, 2 for no):", int)
        if not self.mainWindow.update_privacy_budget(self.epsilon):
            return "Privacy budget exceeded. Please reduce the epsilon value."

        query = f"""
        SELECT 
            CASE 
                WHEN classification_final BETWEEN 1 AND 3 THEN classification_final
                ELSE 4  -- Group all classifications >= 4 as "Non-COVID"
            END AS classification_group,
            COUNT(*) AS Patient_Count
        FROM Patients
        WHERE (DIABETES = {diabetes} OR OBESITY = {obesity} OR CARDIOVASCULAR = {cardio})
        GROUP BY classification_group
        ORDER BY classification_group;
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for the given criteria."

        dp_results = {
            row["classification_group"]: apply_differential_privacy(
                self.db_connection,
                [row["Patient_Count"]],
                mechanism="Laplace",
                epsilon=self.epsilon,
                query=query
            )[0]
            for row in results
        }

        fig, ax = plt.subplots(figsize=(6, 4))

        classification_labels = {
            1: "COVID Level 1",
            2: "COVID Level 2",
            3: "COVID Level 3",
            4: "Non-COVID"
        }

        classifications = list(dp_results.keys())
        noisy_counts = list(dp_results.values())

        x_labels = [classification_labels[cls] for cls in classifications]

        ax.bar(
            x_labels,
            noisy_counts,
            color='#3498db',
            edgecolor='black'
        )

        diabetes_status = "Yes" if diabetes == 1 else "No"
        obesity_status = "Yes" if obesity == 1 else "No"
        cardio_status = "Yes" if cardio == 1 else "No"

        title = (
            f"Disease and Classification Analysis (ε={self.epsilon:.2f})\n"
            f"Diabetes: {diabetes_status}, Obesity: {obesity_status}, Cardiovascular: {cardio_status}"
        )
        ax.set_title(title, fontsize=12, pad=10)

        ax.set_xlabel("Classification", fontsize=10)
        ax.set_ylabel("Noisy Patient Count", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.display_graph(fig)

        return dp_results

    def perform_gender_tobacco_analysis(self):
        """Query: Gender and Tobacco Analysis"""
        sex = self.get_input("Enter gender (1 for female, 2 for male):", int)
        tobacco = self.get_input("Enter tobacco status (1 for yes, 2 for no):", int)

        if not self.mainWindow.update_privacy_budget(self.epsilon):
            return "Privacy budget exceeded. Please reduce the epsilon value."

        query = f"""
        SELECT 
            SEX,
            COUNT(*) AS Total_Patients,
            SUM(CASE WHEN ICU = 1 THEN 1 ELSE 0 END) AS ICU_Admissions,
            (SUM(CASE WHEN ICU = 1 THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) AS ICU_Rate
        FROM Patients
        WHERE SEX = {sex}
          AND TOBACCO = {tobacco}
        GROUP BY SEX;
        """
        self.db_connection.execute_query(query)
        result = self.db_connection.cursor.fetchone()

        if not result:
            return "No data available for the given criteria."

        total_patients = float(result["Total_Patients"])
        icu_admissions = float(result["ICU_Admissions"])
        icu_rate = float(result["ICU_Rate"])

        dp_total = apply_differential_privacy(
            self.db_connection,
            [total_patients],
            mechanism="Laplace",
            epsilon=self.epsilon,
            query=query
        )[0]
        dp_icu = apply_differential_privacy(
            self.db_connection,
            [icu_admissions],
            mechanism="Laplace",
            epsilon=self.epsilon,
            query=query
        )[0]

        fig, ax = plt.subplots(figsize=(4, 4))
        categories = ["Total Patients", "ICU Admissions"]
        values = [dp_total, dp_icu]

        ax.bar(
            categories,
            values,
            color=['#3498db', '#e74c3c'],
            edgecolor='black'
        )
        ax.set_title(f"Gender and Tobacco Analysis (ε={self.epsilon:.2f})", fontsize=12, pad=10)
        ax.set_xlabel("Category", fontsize=10)
        ax.set_ylabel("Noisy Count", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.display_graph(fig)

        return {
            "Total Patients (DP)": dp_total,
            "ICU Admissions (DP)": dp_icu,
            "ICU Rate": icu_rate
        }

    def perform_death_count_analysis(self):
        """Query: Death Count Analysis"""
        start_date = self.get_input("Enter start date (YYYY-MM-DD):", str)
        end_date = self.get_input("Enter end date (YYYY-MM-DD):", str)

        if not self.mainWindow.update_privacy_budget(self.epsilon):
            return "Privacy budget exceeded. Please reduce the epsilon value."

        query = f"""
        SELECT 
            COUNT(*) AS Deaths
        FROM Patients
        WHERE DATE_DIED BETWEEN '{start_date}' AND '{end_date}';
        """
        self.db_connection.execute_query(query)
        result = self.db_connection.cursor.fetchone()

        if not result:
            return "No data available for the given criteria."

        dp_result = apply_differential_privacy(
            self.db_connection,
            [result["Deaths"]],
            mechanism="Laplace",
            epsilon=self.epsilon,
            query=query
        )[0]

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 4))

        ax.bar(["Deaths"], [dp_result], color='#3498db', edgecolor='black')

        ax.set_title(
            f"Death Count (ε={self.epsilon:.2f})\nDate Range: {start_date} to {end_date}",
            fontsize=12,
            pad=10
        )
        ax.set_ylabel("Noisy Death Count", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.display_graph(fig)

        return f"Death Count (ε={self.epsilon:.2f}) for Date Range: {start_date} to {end_date}: {dp_result}"

    def perform_icu_comorbidity_analysis(self):
        """Query: ICU and Comorbidity Analysis"""
        pneumonia = self.get_input("Enter pneumonia status (1 for yes, 2 for no):", int)
        immunosuppressed = self.get_input("Enter immunosuppressed status (1 for yes, 2 for no):", int)
        renal_chronic = self.get_input("Enter chronic renal status (1 for yes, 2 for no):", int)

        if not self.mainWindow.update_privacy_budget(self.epsilon):
            return "Privacy budget exceeded. Please reduce the epsilon value."

        query = f"""
        SELECT 
            ICU,
            COUNT(*) AS Patient_Count
        FROM Patients
        WHERE PNEUMONIA = {pneumonia}
          AND INMSUPR = {immunosuppressed}
          AND RENAL_CHRONIC = {renal_chronic}
          AND ICU NOT IN (97, 99)  
        GROUP BY ICU;
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for the given criteria."

        dp_results = {
            "ICU Admitted" if row["ICU"] == 1 else "Not Admitted to ICU": apply_differential_privacy(
                self.db_connection,
                [row["Patient_Count"]],
                mechanism="Laplace",
                epsilon=self.epsilon,
                query=query
            )[0]
            for row in results
        }

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 4))

        icu_categories = list(dp_results.keys())
        noisy_counts = list(dp_results.values())

        ax.bar(
            icu_categories,
            noisy_counts,
            color='#3498db',
            edgecolor='black'
        )
        ax.set_title(f"ICU and Comorbidity Analysis (ε={self.epsilon:.2f})", fontsize=12, pad=10)
        ax.set_xlabel("ICU Category", fontsize=10)
        ax.set_ylabel("Noisy Patient Count", fontsize=10)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.display_graph(fig)

        return dp_results

    def get_input(self, prompt, input_type):
        return input_type(simpledialog.askstring("Input", prompt))

    def display_graph(self, fig):
        """Displays a matplotlib graph in the graph frame with modern styling."""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        plt.style.use('ggplot')
        fig.patch.set_facecolor('#2e2e2e')

        for ax in fig.axes:
            ax.set_facecolor('#2e2e2e')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()