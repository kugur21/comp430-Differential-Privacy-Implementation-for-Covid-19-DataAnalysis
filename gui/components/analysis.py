import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from privacy.differential_privacy import apply_differential_privacy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class AnalysisView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent, padding="20")
        self.db_connection = db_connection
        self.current_canvas = None
        self.epsilon = 1.0  # Default privacy budget

        # Configure grid weights for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Set theme style
        self.style = ttk.Style()
        self.style.theme_use('superhero')  # Modern tema seçimi
        self.setup_ui()

    def setup_ui(self):
        # Header Section
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        title = ttk.Label(
            header_frame,
            text="Data Analysis",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-primary"
        )
        title.pack(pady=(0, 10))

        # Analysis Selection
        self.analysis_options = [
            "Age Distribution",
            "ICU Statistics",
            "Disease Correlation",
            "Gender-Based ICU Analysis",
            "Medical Unit Analysis",
            "Time Series Analysis",
            "COVID Trends",
            "Disease Priority Analysis",
            "Disease Weighted Selection",
            "Recovery Rate Analysis",
            "Mortality Rate by Age Group",
            "Most Affected Age",
            "High Risk Survivor"
        ]
        self.analysis_var = ttk.StringVar(value=self.analysis_options[0])

        # Control Panel
        control_frame = ttk.Frame(self)
        control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # Add epsilon slider
        epsilon_frame = ttk.Frame(control_frame)
        epsilon_frame.pack(pady=(0, 10))

        epsilon_label = ttk.Label(
            epsilon_frame,
            text="Privacy Budget (ε):",
            font=("Helvetica", 10)
        )
        epsilon_label.pack(side="left", padx=(0, 10))

        # We use an IntVar to ensure integer steps from 1 to 10
        self.epsilon_var = ttk.IntVar(value=1)

        # Configure the slider for integer values from 1 to 10
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

        # This label will display the numeric value of ε
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

        run_button = ttk.Button(
            control_frame,
            text="Run Analysis",
            command=self.run_analysis,
            bootstyle="primary-outline",
            width=20
        )
        run_button.pack(pady=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            bootstyle="primary",
            length=200
        )
        self.progress.pack(pady=(0, 10))
        self.progress.pack_forget()

        # Main Content Area
        content_frame = ttk.Frame(self)
        content_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)  # Increase weight for the visualization area

        # Results Panel
        results_frame = ttk.LabelFrame(
            content_frame,
            text="Analysis Results",
            padding="10",
            bootstyle="primary"
        )
        results_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        self.result_text = ScrolledText(
            results_frame,
            height=20,
            width=40,  # Reduce the width of the analysis result text box
            wrap="word",
            font=("Helvetica", 14),  # Increase the font size of the analysis result text
            autohide=True
        )
        self.result_text.pack(fill="both", expand=True)

        # Graph Panel
        graph_frame = ttk.LabelFrame(
            content_frame,
            text="Visualization",
            padding="10",
            bootstyle="primary"
        )
        graph_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self.graph_frame = ttk.Frame(graph_frame, width=800, height=400)  # Increase the width of the visualization area
        self.graph_frame.pack(fill="both", expand=True)

        # Status Bar
        self.status_label = ttk.Label(
            self,
            text="Ready",
            font=("Helvetica", 10),
            bootstyle="secondary"
        )
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    def _update_epsilon_label(self, event=None):
        """Callback to update the epsilon label whenever the slider moves."""
        self.epsilon_value_label.config(text=str(self.epsilon_var.get()))

    def run_analysis(self):
        self.progress.pack()
        self.progress.start()
        self.status_label.configure(text="Running analysis...")

        self.result_text.delete(1.0, "end")
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        try:
            selected_analysis = self.analysis_var.get()
            # Get the current epsilon value from the slider (integer from 1 to 10)
            self.epsilon = float(self.epsilon_var.get())

            if selected_analysis == "Age Distribution":
                result = self.perform_age_group_distribution()
            elif selected_analysis == "ICU Statistics":
                result = self.perform_icu_statistics()
            elif selected_analysis == "Disease Correlation":
                result = self.perform_disease_correlation()
            elif selected_analysis == "Gender-Based ICU Analysis":
                result = self.perform_gender_based_analysis()
            elif selected_analysis == "Medical Unit Analysis":
                result = self.perform_regional_analysis()
            elif selected_analysis == "Time Series Analysis":
                result = self.perform_time_series_analysis()
            elif selected_analysis == "COVID Trends":
                result = self.perform_covid_trends()
            elif selected_analysis == "Disease Priority Analysis":
                result = self.perform_disease_priority_analysis()
            elif selected_analysis == "Disease Weighted Selection":
                result = self.perform_top_death_dates_exponential()
            elif selected_analysis == "Recovery Rate Analysis":
                result = self.perform_recovery_rate_analysis()
            elif selected_analysis == "Mortality Rate by Age Group":
                result = self.perform_mortality_rate_by_age_group()
            elif selected_analysis == "Most Affected Age":
                result = self.perform_most_affected_age_group()
            elif selected_analysis == "High Risk Survivor":
                result = self.perform_high_risk_survivors()
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

        finally:
            self.progress.stop()
            self.progress.pack_forget()

    def display_graph(self, fig):
        plt.style.use('ggplot')  # Modern grafik stili
        fig.patch.set_facecolor(self.style.colors.bg)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.config(width=600, height=400)
        canvas_widget.pack(fill="both", expand=True)

        fig.tight_layout()
        canvas.draw()
        self.current_canvas = canvas

    def perform_age_group_distribution(self):
        """
        Fetches age distribution data from the database, applies differential privacy,
        and visualizes the results.
        """
        # SQL query to group patients by age groups
        query = """
        SELECT 
            FLOOR(age / 10) * 10 AS age_group, 
            COUNT(*) AS count
        FROM Patients
        WHERE age IS NOT NULL  -- Exclude missing age values
        GROUP BY FLOOR(age / 10) * 10
        ORDER BY age_group;
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No age distribution data available."

        # Convert query results into a dictionary: {age_group: count}
        age_groups = {f"{row['age_group']}-{row['age_group'] + 9}": float(row['count'])
                      for row in results}

        # Apply differential privacy to each age group count
        dp_results = {
            group: apply_differential_privacy(
                [count],
                mechanism="Gaussian",
                epsilon=self.epsilon,
                sensitivity=1
            )[0]
            for group, count in age_groups.items()
        }

        # Plot the results
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(dp_results)))
        ax.bar(dp_results.keys(), dp_results.values(), color=colors, edgecolor='black')

        # Set titles and labels with improved font sizes
        ax.set_title(f"Age Distribution (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_xlabel("Age Groups", fontsize=12, color='white')
        ax.set_ylabel("Noisy Count", fontsize=12, color='white')

        # Improve grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', color='white')

        # Set the color of the tick labels
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Display the graph
        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Age Distribution Results:\n"
        for age_group, count in dp_results.items():
            result_str += f"{age_group}: {count:.2f}\n"
        return result_str

    def perform_icu_statistics(self):
        # Query to get detailed ICU statistics
        query = """
        SELECT 
            COUNT(*) AS total_icu_patients,
            AVG(age) AS avg_age,
            SUM(CASE WHEN sex = 1 THEN 1 ELSE 0 END) AS male_count,
            SUM(CASE WHEN sex = 2 THEN 1 ELSE 0 END) AS female_count,
            SUM(CASE WHEN diabetes = 1 THEN 1 ELSE 0 END) AS diabetes_count,
            SUM(CASE WHEN hipertension = 1 THEN 1 ELSE 0 END) AS hipertension_count,
            SUM(CASE WHEN obesity = 1 THEN 1 ELSE 0 END) AS obesity_count
        FROM Patients
        WHERE icu = 1;
        """
        self.db_connection.execute_query(query)
        result = self.db_connection.cursor.fetchone()

        if not result:
            return "No ICU data available."

        # Extract results
        total_icu_patients = float(result['total_icu_patients'])
        avg_age = float(result['avg_age'])
        male_count = float(result['male_count'])
        female_count = float(result['female_count'])
        diabetes_count = float(result['diabetes_count'])
        hipertension_count = float(result['hipertension_count'])
        obesity_count = float(result['obesity_count'])

        # Apply differential privacy to all counts
        dp_total_icu_patients = \
        apply_differential_privacy([total_icu_patients], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_avg_age = apply_differential_privacy([avg_age], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_male_count = apply_differential_privacy([male_count], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_female_count = apply_differential_privacy([female_count], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_diabetes_count = apply_differential_privacy([diabetes_count], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_hipertension_count = \
        apply_differential_privacy([hipertension_count], mechanism="Laplace", epsilon=self.epsilon)[0]
        dp_obesity_count = apply_differential_privacy([obesity_count], mechanism="Laplace", epsilon=self.epsilon)[0]

        # Prepare data for visualization
        gender_labels = ['Male', 'Female']
        gender_counts = [dp_male_count, dp_female_count]

        disease_labels = ['Diabetes', 'Hypertension', 'Obesity']
        disease_counts = [dp_diabetes_count, dp_hipertension_count, dp_obesity_count]

        # Create subplots for gender and disease distribution
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot gender distribution
        colors_gender = plt.cm.viridis(np.linspace(0, 1, len(gender_labels)))
        ax1.pie(gender_counts, labels=gender_labels, autopct="%1.1f%%", startangle=90, colors=colors_gender,
                textprops={'color': 'white'})
        ax1.set_title(f"Gender Distribution in ICU (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')

        # Plot disease distribution
        colors_disease = plt.cm.viridis(np.linspace(0, 1, len(disease_labels)))
        ax2.bar(disease_labels, disease_counts, color=colors_disease, edgecolor='black')
        ax2.set_title(f"Disease Distribution in ICU (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax2.set_ylabel("Noisy Count", fontsize=12, color='white')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')

        # Set the background color of the plots
        ax1.set_facecolor('#2e2e2e')
        ax2.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Display the graph
        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = (
            f"ICU Statistics (ε={self.epsilon:.2f}):\n"
            f"Total ICU Patients: {dp_total_icu_patients:.2f}\n"
            f"Average Age: {dp_avg_age:.2f}\n"
            f"Male Patients: {dp_male_count:.2f}\n"
            f"Female Patients: {dp_female_count:.2f}\n"
            f"Patients with Diabetes: {dp_diabetes_count:.2f}\n"
            f"Patients with Hypertension: {dp_hipertension_count:.2f}\n"
            f"Patients with Obesity: {dp_obesity_count:.2f}\n"
        )
        return result_str

    def perform_disease_correlation(self):
        query = """
        SELECT COUNT(*) AS count, diabetes, hipertension 
        FROM Patients 
        WHERE diabetes IN (1, 2) AND hipertension IN (1, 2)  
        GROUP BY diabetes, hipertension
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for disease correlation."

        dp_results = {
            f"Diabetes: {row['diabetes']}, Hypertension: {row['hipertension']}":
                apply_differential_privacy([row['count']], mechanism="Laplace", epsilon=self.epsilon)[0]
            for row in results
        }

        # Adjust figure size to fit the frame
        fig, ax = plt.subplots(figsize=(6, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        wedges, texts, autotexts = ax.pie(
            dp_results.values(),
            labels=dp_results.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.viridis(np.linspace(0, 1, len(dp_results))),
            textprops={'fontsize': 10, 'color': 'white'}  # Smaller text size
        )
        ax.set_title(f"Disease Correlation (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent text overlap
        plt.tight_layout()

        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Disease Correlation Results:\n"
        for condition, count in dp_results.items():
            result_str += f"{condition}: {count:.2f}\n"
        return result_str

    def perform_gender_based_analysis(self):
        """
        Fetches gender-based patient and ICU statistics from the database,
        applies differential privacy, and visualizes the results.
        """
        # SQL query to get total patients and ICU patients by gender
        query = """
        SELECT 
            sex AS gender,
            COUNT(*) AS total,
            SUM(CASE WHEN icu = 1 THEN 1 ELSE 0 END) AS icu_count
        FROM Patients
        WHERE sex IN (1, 2)  -- Filter out missing values (e.g., 97, 99)
        GROUP BY sex;
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No gender-based data available."

        # Convert query results into a dictionary: {gender: {"total": count, "icu_count": count}}
        genders = {
            row["gender"]: {
                "total": float(row["total"]),
                "icu_count": float(row["icu_count"])
            }
            for row in results
        }

        # Apply differential privacy to all values
        dp_genders = {
            k: {
                "total": apply_differential_privacy(
                    [v["total"]],
                    mechanism="Gaussian",
                    epsilon=self.epsilon,
                    sensitivity=1
                )[0],
                "icu_count": apply_differential_privacy(
                    [v["icu_count"]],
                    mechanism="Gaussian",
                    epsilon=self.epsilon,
                    sensitivity=1
                )[0]
            }
            for k, v in genders.items()
        }

        # Prepare data for visualization
        labels = [f"Gender {k}" for k in dp_genders.keys()]
        total_values = [v["total"] for v in dp_genders.values()]
        icu_values = [v["icu_count"] for v in dp_genders.values()]

        # Create pie charts with adjusted figure size
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        colors = plt.cm.viridis(np.linspace(0, 1, len(dp_genders)))

        ax1.pie(total_values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'color': 'white'})
        ax1.set_title(f"Total Patients by Gender (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')

        ax2.pie(icu_values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'color': 'white'})
        ax2.set_title(f"ICU Patients by Gender (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')

        # Set the background color of the plot
        ax1.set_facecolor('#2e2e2e')
        ax2.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent text overlap
        plt.tight_layout()

        # Display the graph
        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Gender-Based Analysis Results:\n"
        for gender, data in dp_genders.items():
            result_str += f"Gender {gender} - Total: {data['total']:.2f}, ICU: {data['icu_count']:.2f}\n"
        return result_str

    def perform_regional_analysis(self):
        query = "SELECT usmer, COUNT(*) AS count FROM Patients GROUP BY usmer"
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for regional analysis."

        # Map usmer values to their corresponding medical unit levels
        usmer_mapping = {
            1: "First Level",
            2: "Second Level",
            3: "Third Level"
        }

        # Apply differential privacy to the counts
        dp_results = {
            usmer_mapping[row['usmer']]:
                apply_differential_privacy([row['count']], mechanism="Laplace", epsilon=self.epsilon)[0]
            for row in results
        }

        # Create the plot with a smaller size
        fig, ax = plt.subplots(figsize=(6, 4))  # Smaller figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Prepare data for pie chart
        labels = list(dp_results.keys())
        sizes = list(dp_results.values())
        colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))  # Modern renk paleti

        # Plot the pie chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',  # Yüzde değerlerini göster
            startangle=90,  # Başlangıç açısı
            colors=colors,
            textprops={'fontsize': 10, 'color': 'white'}  # Yazı boyutu ve rengi
        )

        # Set titles with improved font sizes
        ax.set_title(f"Medical Unit Level Distribution (ε={self.epsilon:.2f})", fontsize=12, pad=10, color='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Display the graph
        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Medical Unit Level Distribution Results:\n"
        for region, count in dp_results.items():
            result_str += f"{region}: {count:.2f}\n"
        return result_str
    def perform_time_series_analysis(self):
        query = """
        SELECT date_died, COUNT(*) AS deaths 
        FROM Patients 
        WHERE date_died IS NOT NULL 
        GROUP BY date_died 
        ORDER BY date_died
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for time series analysis."

        dp_results = {
            row['date_died']:
                apply_differential_privacy([row['deaths']], mechanism="Gaussian", epsilon=self.epsilon)[0]
            for row in results
        }

        dates = list(dp_results.keys())
        values = list(dp_results.values())

        fig, ax = plt.subplots(figsize=(10, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data without markers and with a solid line
        ax.plot(dates, values, linestyle='-', color='#3498db', linewidth=2)

        # Set titles and labels with improved font sizes
        ax.set_title(f"Time Series Analysis (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_xlabel("Date", fontsize=12, color='white')
        ax.set_ylabel("Noisy Death Count", fontsize=12, color='white')

        # Improve grid lines
        ax.grid(True, linestyle='--', alpha=0.7)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', color='white')

        # Set the color of the tick labels
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Time Series Analysis Results:\n"
        for date, count in dp_results.items():
            result_str += f"{date}: {count:.2f}\n"
        return result_str

    def perform_covid_trends(self):
        try:
            query = """
            SELECT DATE_FORMAT(created_at, '%Y-%u') AS week, COUNT(*) AS weekly_cases 
            FROM Patients 
            WHERE classification_final = 1 
            GROUP BY week
            ORDER BY week;
            """
            # Execute query and check if successful
            if not self.db_connection.execute_query(query):
                return "Error executing database query"

            # Fetch results and check if there's data
            results = self.db_connection.cursor.fetchall()
            if not results:
                return "No COVID trend data available"

            # Process the data
            dp_results = {}
            for row in results:
                if row and 'week' in row and 'weekly_cases' in row:
                    week = row['week']
                    cases = row['weekly_cases']
                    if week and cases is not None:  # Ensure we have valid data
                        dp_results[week] = apply_differential_privacy(
                            [cases],
                            mechanism="Gaussian",
                            epsilon=self.epsilon
                        )[0]

            if not dp_results:
                return "No valid data points found for analysis"

            weeks = list(dp_results.keys())
            cases = list(dp_results.values())

            fig, ax = plt.subplots(figsize=(10, 5))  # Adjust figure size
            plt.style.use('ggplot') 

            # Plot the data with a modern color palette
            if len(weeks) > 1:
                ax.plot(
                    weeks,
                    cases,
                    marker='o',
                    linestyle='-',
                    color='#2ecc71',
                    linewidth=2,
                    markersize=8,
                    label="Weekly Cases"
                )
            else:
                # For single data point, use scatter and annotate for visibility
                ax.scatter(
                    weeks,
                    cases,
                    color='#2ecc71',
                    s=150,  # Increase the dot size for better visibility
                  
                )
                ax.annotate(f"{cases[0]:.2f}",
                            (weeks[0], cases[0]),
                            textcoords="offset points",
                            xytext=(0, 10),
                            ha='center',
                            color='white',
                            fontweight='bold')

            # Set titles and labels with improved font sizes and colors
            ax.set_title(f"COVID Trends Over Time (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
            ax.set_xlabel("Weeks", fontsize=12, color='white')
            ax.set_ylabel("Noisy Cases", fontsize=12, color='white')

            # Improve grid lines
            ax.grid(True, linestyle='--', alpha=0.7)

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right', color='white')

            # Set the color of the tick labels
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            # Set the background color of the plot
            ax.set_facecolor('#2e2e2e')
            fig.patch.set_facecolor('#2e2e2e')

            # Add a legend for clarity
            ax.legend(loc='upper left', fontsize=10, facecolor='#2e2e2e')

            # Adjust layout to prevent overlap
            plt.tight_layout()

            self.display_graph(fig)

            # Return processed data with summary
            result_str = "COVID Trends Analysis Results:\n"
            for week, case in dp_results.items():
                result_str += f"Week {week}: {case:.2f}\n"
            return result_str

        except Exception as e:
            return f"Error analyzing COVID trends: {str(e)}"

    def perform_disease_priority_analysis(self):
        """
        'ReportNoisyMax' mekanizmasını örnekleyen bir analiz.
        Bazı hastalıkların (diabetes, hipertension, obesity, tobacco)
        sayımlarını (count) çekip, en yüksek gürültülü skora sahip
        hastalığı bulur.
        """
        query = """
        SELECT
            SUM(CASE WHEN diabetes=1 THEN 1 ELSE 0 END) AS diabetes_count,
            SUM(CASE WHEN hipertension=1 THEN 1 ELSE 0 END) AS hipertension_count,
            SUM(CASE WHEN obesity=1 THEN 1 ELSE 0 END) AS obesity_count,
            SUM(CASE WHEN tobacco=1 THEN 1 ELSE 0 END) AS tobacco_count
        FROM Patients
        """
        self.db_connection.execute_query(query)
        row = self.db_connection.cursor.fetchone()
        if not row:
            return "No data available."

        # Veritabanından gelen 'decimal.Decimal' türlerini float'a çeviriyoruz:
        data = [
            float(row['diabetes_count']),
            float(row['hipertension_count']),
            float(row['obesity_count']),
            float(row['tobacco_count'])
        ]
        labels = ["Diabetes", "Hypertension", "Obesity", "Tobacco"]

        # 'ReportNoisyMax' mekanizması sadece EN BÜYÜK değerin indeksini döndürür
        idx = apply_differential_privacy(
            data,
            mechanism="ReportNoisyMax",
            epsilon=self.epsilon,
            sensitivity=1  # sayım sorgusu için
        )

        chosen_label = labels[idx]
        chosen_count = data[idx]

        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
        bars = ax.bar(labels, data, color=colors, edgecolor='black')

        # Set titles and labels with improved font sizes
        ax.set_title(f"Disease Priority Analysis (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_ylabel("Count", fontsize=12, color='white')

        # Improve grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Set the color of the tick labels
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Seçilen kategoriyi kırmızıya boyayarak vurgulayalım
        bars[idx].set_color('#e74c3c')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        self.display_graph(fig)

        return f"NoisyMax chose '{chosen_label}' (raw count = {chosen_count:.2f})."

    def perform_top_death_dates_exponential(self):
        """
        En çok kişinin öldüğü 10 tarihi bulur, Exponential mekanizmasıyla
        hangi tarihin 'seçilmiş' olduğunu rastgele belirler.
        X ekseninde sayısal değerler gizlenir (ölçek görünmez).
        """

        # 1) En çok ölüm (count) yaşanan 10 tarihi sorguluyoruz
        query = """
        SELECT 
            date_died, 
            COUNT(*) AS died_count
        FROM Patients
        WHERE date_died IS NOT NULL
        GROUP BY date_died
        ORDER BY died_count DESC
        LIMIT 10
        """
        self.db_connection.execute_query(query)
        rows = self.db_connection.cursor.fetchall()

        if not rows:
            return "No data available for top death dates."

        # 2) Verileri hazırlama
        date_labels = []
        died_counts = []

        for row in rows:
            date_str = str(row["date_died"]) if row["date_died"] else "Unknown"
            count_val = float(row["died_count"]) if row["died_count"] else 0.0

            date_labels.append(date_str)
            died_counts.append(count_val)

        if all(count == 0 for count in died_counts):
            return "All 10 dates have 0 deaths? No valid data to run Exponential."

        # 3) Exponential mekanizması
        chosen_date = apply_differential_privacy(
            data=date_labels,
            mechanism="Exponential",
            epsilon=self.epsilon,
            utility=died_counts,
            sensitivity=1
        )

        # 4) Yatay bar chart oluşturma
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(date_labels)))
        bars = ax.barh(date_labels, died_counts, color=colors, edgecolor='black')

        # Set titles and labels with improved font sizes
        ax.set_title(f"Top 10 Death Dates (Exponential) (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_ylabel("Date Died", fontsize=12, color='white')

        # --- SAYISAL EKSENİ GİZLEME ---
        ax.set_xlabel("")  # x ekseni etiketini boş yap
        ax.set_xticklabels([])  # x ekseni üzerindeki yazıları gizle
        ax.set_xticks([])  # x ekseni üzerindeki çizgileri kaldır

        # Çizgiler (grid) de istenmiyorsa:
        # ax.grid(False)  # tüm ızgarayı kapatabilir
        # veya sadece x ekseni gridini kapatmak için:
        ax.grid(axis='y', linestyle='--', alpha=0.3)  # sadece yatay çizgiler kalsın

        # Seçilen tarihi kırmızıya boyayalım
        for i, lbl in enumerate(date_labels):
            if lbl == chosen_date:
                bars[i].set_color('#e74c3c')
                # Dilerseniz açıklama da koyabilirsiniz:
                ax.annotate(
                    "Selected",
                    xy=(died_counts[i], i),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center',
                    color='white',
                    fontweight='bold'
                )

        # Set the color of the tick labels
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        self.display_graph(fig)

        # 5) Metinsel çıktı
        return (
            f"Exponential mechanism chose date '{chosen_date}' among the top 10 death dates.\n"
            "Note: X-axis numeric scale is hidden."
        )

    def perform_recovery_rate_analysis(self):
        query = """
        SELECT 
            COUNT(*) AS total_cases,
            SUM(CASE WHEN date_died IS NULL THEN 1 ELSE 0 END) AS recovered_cases
        FROM Patients;
        """
        self.db_connection.execute_query(query)
        result = self.db_connection.cursor.fetchone()

        if not result:
            return "No data available for recovery analysis."

        total_cases = float(result['total_cases'])
        recovered_cases = float(result['recovered_cases'])

        print(f"SQL Query - Total Cases: {total_cases}, Recovered Cases: {recovered_cases}")

        if total_cases == 0:
            return "Total cases is zero, cannot calculate recovery rate."

        noise_total = np.random.normal(0, 50)  #higher noise to test impact
        noise_recovered = np.random.normal(0, 50)

        dp_total_cases = max(apply_differential_privacy([total_cases], mechanism="Gaussian", epsilon=self.epsilon, sensitivity=1)[0] + noise_total, 0)
        dp_recovered_cases = max(apply_differential_privacy([recovered_cases], mechanism="Gaussian", epsilon=self.epsilon, sensitivity=1)[0] + noise_recovered, 0)

        print(f"DP - Total Cases: {dp_total_cases}, Recovered Cases: {dp_recovered_cases}")

        #noise might lead to zero values
        if dp_total_cases < 1:
            print("DP total cases after noise is too low, setting to 1 to avoid division by zero.")
            dp_total_cases = 1

        # Calculation of Recovery Rate
        recovery_rate = (dp_recovered_cases / dp_total_cases) * 100
        print(f"Calculated Recovery Rate: {recovery_rate:.2f}%")
        values = [dp_recovered_cases, dp_total_cases - dp_recovered_cases]
        labels = ['Recovered', 'Not Recovered']

        plt.clf()
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(labels)))
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors, textprops={'color': 'white'})

        # Set titles and labels with improved font sizes
        ax.set_title(f"Recovery Rate (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        self.display_graph(fig)

        return f"Recovery Rate (ε={self.epsilon:.2f}): {recovery_rate:.2f}%"

    def perform_mortality_rate_by_age_group(self):
        query = """
            SELECT FLOOR(age / 10) * 10 AS age_group, 
                COUNT(*) AS total_cases,
                SUM(CASE WHEN date_died IS NOT NULL THEN 1 ELSE 0 END) AS deaths
            FROM Patients
            GROUP BY age_group
            ORDER BY age_group;
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for mortality rate analysis."

        # decimal to float for numerical operations
        age_groups = {f"{row['age_group']}-{row['age_group'] + 9}": float(row['total_cases']) for row in results}
        deaths = {f"{row['age_group']}-{row['age_group'] + 9}": float(row['deaths']) for row in results}

        dp_total_cases = {
            group: apply_differential_privacy([count], mechanism="Gaussian", epsilon=self.epsilon, sensitivity=1)[0]
            for group, count in age_groups.items()
        }

        dp_deaths = {
            group: apply_differential_privacy([count], mechanism="Laplace", epsilon=self.epsilon, sensitivity=1)[0]
            for group, count in deaths.items()
        }

        # computation of mortality rates safely
        mortality_rates = {
            group: (dp_deaths[group] / dp_total_cases[group] * 100) if dp_total_cases[group] > 0 else 0
            for group in age_groups
        }

        # Clear previous plot before drawing a new one
        plt.clf()

        # Create a new figure with a modern style
        fig, ax = plt.subplots(figsize=(8, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(mortality_rates)))
        ax.bar(mortality_rates.keys(), mortality_rates.values(), color=colors, edgecolor='black')

        # Set titles and labels with improved font sizes
        ax.set_title(f"Mortality Rate by Age Group (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_xlabel("Age Group", fontsize=12, color='white')
        ax.set_ylabel("Mortality Rate (%)", fontsize=12, color='white')

        # Improve grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', color='white')

        # Set the color of the tick labels
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        # Display the graph
        self.display_graph(fig)

        # Return the differentially private results in a readable format
        result_str = "Mortality Rate by Age Group Results:\n"
        for age_group, rate in mortality_rates.items():
            result_str += f"{age_group}: {rate:.2f}%\n"
        return result_str

    def perform_most_affected_age_group(self):
        query = """
            SELECT FLOOR(age / 10) * 10 AS age_group, 
                COUNT(*) AS total_cases
            FROM Patients
            WHERE date_died IS NOT NULL
            GROUP BY age_group
            ORDER BY age_group
        """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No data available for mortality analysis."

        # Convert data to appropriate types
        age_groups = {str(row["age_group"]) + "-" + str(row["age_group"] + 9): float(row["total_cases"]) for row in results}

        # Apply Report Noisy Max to find the most affected age group
        most_affected_group_index = apply_differential_privacy(
            data=list(age_groups.values()),
            mechanism="ReportNoisyMax",
            epsilon=self.epsilon,
            sensitivity=1
        )

        most_affected_group = list(age_groups.keys())[most_affected_group_index]

        # Prepare visualization data
        age_labels = list(age_groups.keys())
        affected_counts = list(age_groups.values())

        # Create the horizontal bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.barh(age_labels, affected_counts, color='#3498db', edgecolor='black')

        ax.set_title(f"Most Affected Age Groups (ε={self.epsilon:.2f})", fontsize=14, pad=15, fontweight='bold')
        ax.set_ylabel("Age Groups", fontsize=12)
        
        # Hide X-axis labels for a cleaner look
        ax.set_xlabel("")
        ax.set_xticklabels([])
        ax.set_xticks([])

        # Add grid lines for readability
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        # Highlight the most affected age group in red
        for i, lbl in enumerate(age_labels):
            if lbl == most_affected_group:
                bars[i].set_color('#e74c3c')
                ax.annotate(
                    "Selected",
                    xy=(affected_counts[i], i),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center',
                    color='white',
                    fontweight='bold'
                )

        self.display_graph(fig)

        return f"The most affected age group is {most_affected_group} years."





    def perform_high_risk_survivors(self):
        query = """
            SELECT patient_id, age, diabetes, obesity, hipertension, intubed, icu
            FROM Patients
            WHERE (diabetes + obesity + hipertension) >= 2
            AND (intubed = 1 OR icu = 1)
            AND date_died IS NULL;
        """


        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        if not results:
            return "No high-risk survivor data available."

        ages = [row["age"] for row in results]

        dp_survivors_count = apply_differential_privacy(
            [len(results)],
            mechanism="Laplace",
            epsilon=self.epsilon,
            sensitivity=1)[0]


        selected_age = apply_differential_privacy(
            data=ages,
            mechanism="Exponential",
            epsilon=self.epsilon,
            utility=ages,
            sensitivity=1)

        age_groups = {f"{age//10*10}-{age//10*10+9}": 0 for age in ages}
        for age in ages:
            age_group = f"{age//10*10}-{age//10*10+9}"
            age_groups[age_group] += 1

        group_labels = list(age_groups.keys())
        survivor_counts = list(age_groups.values())


        fig, ax = plt.subplots(figsize=(8, 5))  # Adjusted figure size
        plt.style.use('ggplot')  # Use seaborn style for better aesthetics

        # Plot the data with a modern color palette
        colors = plt.cm.viridis(np.linspace(0, 1, len(group_labels)))
        bars = ax.barh(group_labels, survivor_counts, color=colors, edgecolor='black')

        # Set titles and labels with improved font sizes
        ax.set_title(f"High-Risk Survivors by Age Group (ε={self.epsilon:.2f})", fontsize=14, pad=15, color='white')
        ax.set_ylabel("Age Groups", fontsize=12, color='white')

        # --- SAYISAL EKSENİ GİZLEME ---
        ax.set_xlabel("")  # x ekseni etiketini boş yap
        ax.set_xticklabels([])  # x ekseni üzerindeki yazıları gizle
        ax.set_xticks([])  # x ekseni üzerindeki çizgileri kaldır

        # Çizgiler (grid) de istenmiyorsa:
        # ax.grid(False)  # tüm ızgarayı kapatabilir
        # veya sadece x ekseni gridini kapatmak için:
        ax.grid(axis='y', linestyle='--', alpha=0.3)  # sadece yatay çizgiler kalsın

        # highlight most affected age group
        most_affected_group = f"{selected_age//10*10}-{selected_age//10*10+9}"
        for i, lbl in enumerate(group_labels):
            if lbl == most_affected_group:
                bars[i].set_color('#e74c3c')
                ax.annotate(
                    "Selected",
                    xy=(survivor_counts[i], i),
                    xytext=(5, 0),
                    textcoords="offset points",
                    va='center',
                    color='white',
                    fontweight='bold'
                )

        # Set the color of the tick labels
        ax.tick_params(axis='y', colors='white')

        # Set the background color of the plot
        ax.set_facecolor('#2e2e2e')
        fig.patch.set_facecolor('#2e2e2e')

        # Adjust layout to prevent overlap
        plt.tight_layout()

        self.display_graph(fig)

        return {
            "Total High-Risk Survivors (DP)": dp_survivors_count,
            "DP Selected Age Group": most_affected_group
        }