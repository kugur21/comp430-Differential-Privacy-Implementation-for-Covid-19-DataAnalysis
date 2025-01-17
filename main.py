# config.py
import os
from dotenv import load_dotenv
# main.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
# database/connection.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import numpy as np
from typing import List, Union, Tuple
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import List, Dict, Any
# gui/login.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import bcrypt
import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from typing import Dict, Any



load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Sultan9988'),
    'database': os.getenv('DB_NAME', 'covid_data')
}




class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False


# database/schema.py
CREATE_TABLES_QUERIES = {
    'users': """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('admin', 'viewer') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    'patients': """
        CREATE TABLE IF NOT EXISTS Patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            usmer INT,
            medical_unit INT,
            sex INT,
            patient_type INT,
            date_died DATE,
            intubed INT,
            pneumonia INT,
            age INT,
            pregnant INT,
            diabetes INT,
            copd INT,
            asthma INT,
            inmsupr INT,
            hipertension INT,
            other_disease INT,
            cardiovascular INT,
            obesity INT,
            renal_chronic INT,
            tobacco INT,
            classification_final INT,
            icu INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}

# privacy/differential_privacy.py



class DifferentialPrivacy:
    def __init__(self, epsilon: float = 1.0):
        self.epsilon = epsilon

    def add_gaussian_noise(self, data: List[float], sensitivity: float = 1.0) -> List[float]:
        """Add Gaussian noise to numeric data."""
        scale = sensitivity / self.epsilon
        noise = np.random.normal(0, scale, len(data))
        return [d + n for d, n in zip(data, noise)]

    def add_laplace_noise(self, data: List[float], sensitivity: float = 1.0) -> List[float]:
        """Add Laplace noise to count queries."""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, len(data))
        return [d + n for d, n in zip(data, noise)]

    def exponential_mechanism(
            self,
            data: List[Union[str, int]],
            utility_scores: List[float]
    ) -> Tuple[Union[str, int], List[float]]:
        """Apply exponential mechanism to categorical data."""
        utility_scores = np.array(utility_scores)
        probabilities = np.exp(utility_scores * self.epsilon / 2)
        probabilities /= probabilities.sum()
        chosen_idx = np.random.choice(len(data), p=probabilities)
        return data[chosen_idx], probabilities.tolist()


# visualization/charts.py


class ChartManager:
    @staticmethod
    def create_bar_chart(
            data: Dict[str, List[float]],
            title: str,
            xlabel: str,
            ylabel: str
    ) -> Figure:
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.bar(data['labels'], data['values'])
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        return fig

    @staticmethod
    def create_pie_chart(
            data: Dict[str, List[float]],
            title: str
    ) -> Figure:
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        ax.pie(data['values'], labels=data['labels'], autopct='%1.1f%%')
        ax.set_title(title)
        return fig

    @staticmethod
    def embed_chart(parent: tk.Widget, figure: Figure) -> FigureCanvasTkAgg:
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        return canvas




class LoginScreen(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.setup_ui()

    def setup_ui(self):
        # Login form
        login_frame = ttk.Frame(self, padding="20")
        login_frame.pack(expand=True)

        # Title
        title_label = ttk.Label(
            login_frame,
            text="COVID-19 Data Analysis Login",
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.pack(pady=20)

        # Username
        username_frame = ttk.Frame(login_frame)
        username_frame.pack(fill="x", pady=5)
        ttk.Label(username_frame, text="Username:").pack(side="left")
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(side="right", padx=5)

        # Password
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill="x", pady=5)
        ttk.Label(password_frame, text="Password:").pack(side="left")
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side="right", padx=5)

        # Login button
        ttk.Button(
            login_frame,
            text="Login",
            command=self.handle_login,
            style="primary.TButton"
        ).pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # In practice, you would verify against database
        self.callback(username, password)


# gui/main_window.py


class MainWindow(ttk.Frame):
    def __init__(self, parent, db_connection, dp_manager):
        super().__init__(parent)
        self.db_connection = db_connection
        self.dp_manager = dp_manager
        self.setup_ui()

    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Add tabs
        self.data_tab = self.create_data_tab()
        self.analysis_tab = self.create_analysis_tab()
        self.upload_tab = self.create_upload_tab()

        self.notebook.add(self.data_tab, text="Data View")
        self.notebook.add(self.analysis_tab, text="Analysis")
        self.notebook.add(self.upload_tab, text="Data Upload")

    def create_data_tab(self):
        tab = ttk.Frame(self.notebook)

        # Toolbar
        toolbar = ttk.Frame(tab)
        toolbar.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            toolbar,
            text="Refresh Data",
            command=self.refresh_data,
            style="primary.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Export to CSV",
            command=self.export_data,
            style="info.TButton"
        ).pack(side="left", padx=5)

        # Treeview for data display
        columns = [
            "patient_id", "age", "sex", "patient_type",
            "pneumonia", "diabetes", "icu"
        ]

        self.tree = ttk.Treeview(
            tab,
            columns=columns,
            show="headings",
            selectmode="extended"
        )

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)

        # Scrollbars
        y_scroll = ttk.Scrollbar(
            tab,
            orient="vertical",
            command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            tab,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        # Pack everything
        self.tree.pack(fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")

        return tab

    def create_analysis_tab(self):
        tab = ttk.Frame(self.notebook)

        # Controls frame
        controls = ttk.LabelFrame(tab, text="Analysis Controls", padding=10)
        controls.pack(fill="x", padx=5, pady=5)

        # Analysis type selection
        ttk.Label(controls, text="Analysis Type:").pack(side="left", padx=5)
        self.analysis_var = tk.StringVar(value="age_distribution")

        analysis_options = [
            ("Age Distribution", "age_distribution"),
            ("Patient Type Distribution", "patient_type_dist"),
            ("ICU Statistics", "icu_stats")
        ]

        for text, value in analysis_options:
            ttk.Radiobutton(
                controls,
                text=text,
                value=value,
                variable=self.analysis_var
            ).pack(side="left", padx=5)

        # DP controls
        dp_frame = ttk.LabelFrame(tab, text="Privacy Controls", padding=10)
        dp_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(dp_frame, text="Epsilon:").pack(side="left", padx=5)
        self.epsilon_var = tk.DoubleVar(value=1.0)
        epsilon_entry = ttk.Entry(
            dp_frame,
            textvariable=self.epsilon_var,
            width=10
        )
        epsilon_entry.pack(side="left", padx=5)

        ttk.Button(
            dp_frame,
            text="Apply Analysis",
            command=self.run_analysis,
            style="primary.TButton"
        ).pack(side="left", padx=5)

        # Results frame
        self.results_frame = ttk.Frame(tab)
        self.results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        return tab

    def create_upload_tab(self):
        tab = ttk.Frame(self.notebook)

        # Upload frame
        upload_frame = ttk.LabelFrame(tab, text="Upload Data", padding=10)
        upload_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            upload_frame,
            text="Select CSV File",
            command=self.select_file,
            style="info.TButton"
        ).pack(side="left", padx=5)

        self.filename_var = tk.StringVar()
        ttk.Label(
            upload_frame,
            textvariable=self.filename_var
        ).pack(side="left", padx=5)

        # Validation frame
        validation_frame = ttk.LabelFrame(tab, text="Validation Results", padding=10)
        validation_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.validation_text = tk.Text(validation_frame, height=10)
        self.validation_text.pack(fill="both", expand=True)

        return tab

    def refresh_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch new data from database
        query = """
            SELECT patient_id, age, sex, patient_type, 
                   pneumonia, diabetes, icu 
            FROM Patients 
            LIMIT 1000
        """
        self.db_connection.execute_query(query)
        rows = self.db_connection.cursor.fetchall()

        # Insert into treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def export_data(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            # Get selected items or all if none selected
            selected_items = self.tree.selection()
            if not selected_items:
                selected_items = self.tree.get_children()

            # Prepare data for export
            data = []
            for item in selected_items:
                data.append(self.tree.item(item)['values'])

            # Create DataFrame and export
            columns = [self.tree.heading(col)['text'] for col in self.tree.cget('columns')]
            df = pd.DataFrame(data, columns=columns)
            df.to_csv(filename, index=False)

    def run_analysis(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        analysis_type = self.analysis_var.get()
        epsilon = self.epsilon_var.get()

        # Perform analysis based on type
        if analysis_type == "age_distribution":
            self.analyze_age_distribution(epsilon)
        elif analysis_type == "patient_type_dist":
            self.analyze_patient_type_distribution(epsilon)
        elif analysis_type == "icu_stats":
            self.analyze_icu_statistics(epsilon)


    # Continuing main_window.py methods
    def select_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            self.filename_var.set(filename)
            self.validate_csv(filename)

    def validate_csv(self, filename):
        self.validation_text.delete('1.0', tk.END)
        try:
            df = pd.read_csv(filename)
            required_columns = [
                'usmer', 'medical_unit', 'sex', 'patient_type', 'date_died',
                'intubed', 'pneumonia', 'age', 'pregnant', 'diabetes'
            ]

            # Check columns
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                self.validation_text.insert(tk.END,
                                            f"Error: Missing required columns: {', '.join(missing_cols)}\n")
                return False

            # Check data types
            type_errors = []
            numeric_cols = ['age', 'patient_type', 'intubed', 'pneumonia']
            for col in numeric_cols:
                if not pd.to_numeric(df[col], errors='coerce').notna().all():
                    type_errors.append(col)

            if type_errors:
                self.validation_text.insert(tk.END,
                                            f"Error: Non-numeric values in columns: {', '.join(type_errors)}\n")
                return False

            # Validation passed
            self.validation_text.insert(tk.END, "Validation passed. Ready to upload.\n")
            ttk.Button(
                self.validation_text.master,
                text="Upload to Database",
                command=lambda: self.upload_csv(filename),
                style="success.TButton"
            ).pack(pady=10)
            return True

        except Exception as e:
            self.validation_text.insert(tk.END, f"Error reading CSV file: {str(e)}\n")
            return False

    def upload_csv(self, filename):
        try:
            df = pd.read_csv(filename)

            # Convert dates to MySQL format
            df['date_died'] = pd.to_datetime(df['date_died']).dt.strftime('%Y-%m-%d')

            # Prepare insert query
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            query = f"INSERT INTO Patients ({columns}) VALUES ({placeholders})"

            # Insert data in batches
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i + batch_size].values.tolist()
                self.db_connection.cursor.executemany(query, batch)

            self.db_connection.connection.commit()
            self.validation_text.insert(tk.END, "Data uploaded successfully!\n")
            self.refresh_data()

        except Exception as e:
            self.validation_text.insert(tk.END, f"Error uploading data: {str(e)}\n")

    def analyze_age_distribution(self, epsilon):
        # Fetch age data
        query = "SELECT age FROM Patients WHERE age IS NOT NULL"
        self.db_connection.execute_query(query)
        ages = [row[0] for row in self.db_connection.cursor.fetchall()]

        # Add differential privacy
        dp_ages = self.dp_manager.add_gaussian_noise(ages, sensitivity=1.0)

        # Create age groups
        bins = list(range(0, 101, 10))
        orig_hist, _ = np.histogram(ages, bins=bins)
        dp_hist, _ = np.histogram(dp_ages, bins=bins)

        # Create comparison charts
        fig = Figure(figsize=(12, 6))

        # Original distribution
        ax1 = fig.add_subplot(121)
        ax1.hist(ages, bins=bins, alpha=0.7)
        ax1.set_title("Original Age Distribution")
        ax1.set_xlabel("Age")
        ax1.set_ylabel("Count")

        # DP distribution
        ax2 = fig.add_subplot(122)
        ax2.hist(dp_ages, bins=bins, alpha=0.7, color='orange')
        ax2.set_title("Privacy-Preserved Age Distribution")
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Count")

        fig.tight_layout()

        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def analyze_patient_type_distribution(self, epsilon):
        # Fetch patient type data
        query = """
                SELECT patient_type, COUNT(*) as count 
                FROM Patients 
                GROUP BY patient_type
            """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        types, counts = zip(*results)

        # Apply exponential mechanism for selecting representative types
        chosen_type, probabilities = self.dp_manager.exponential_mechanism(
            list(types),
            [count / sum(counts) for count in counts]
        )

        # Create visualization
        fig = Figure(figsize=(12, 6))

        # Pie chart of original distribution
        ax1 = fig.add_subplot(121)
        ax1.pie(counts, labels=[f"Type {t}" for t in types], autopct='%1.1f%%')
        ax1.set_title("Original Patient Type Distribution")

        # Bar chart of selection probabilities
        ax2 = fig.add_subplot(122)
        ax2.bar([f"Type {t}" for t in types], probabilities)
        ax2.set_title("DP Selection Probabilities")
        ax2.set_xlabel("Patient Type")
        ax2.set_ylabel("Probability")
        ax2.tick_params(axis='x', rotation=45)

        fig.tight_layout()

        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def analyze_icu_statistics(self, epsilon):
        # Fetch ICU data
        query = """
                SELECT icu, COUNT(*) as count 
                FROM Patients 
                WHERE icu IS NOT NULL 
                GROUP BY icu
            """
        self.db_connection.execute_query(query)
        results = self.db_connection.cursor.fetchall()

        icu_status, counts = zip(*results)

        # Add Laplace noise to counts
        noisy_counts = self.dp_manager.add_laplace_noise(list(counts))

        # Create visualization
        fig = Figure(figsize=(12, 6))

        # Bar chart comparison
        ax = fig.add_subplot(111)
        x = np.arange(len(icu_status))
        width = 0.35

        ax.bar(x - width / 2, counts, width, label='Original')
        ax.bar(x + width / 2, noisy_counts, width, label='Privacy-Preserved')

        ax.set_xticks(x)
        ax.set_xticklabels(['Not in ICU', 'In ICU'])
        ax.set_ylabel('Count')
        ax.set_title('ICU Statistics: Original vs Privacy-Preserved')
        ax.legend()

        fig.tight_layout()

        # Embed chart
        canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


class Application:
    def __init__(self):
        # Initialize main window
        self.root = ttk.Window(
            title="COVID-19 Data Analysis",
            themename="litera",
            size=(1200, 800)
        )
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize database connection
        self.db = DatabaseConnection()
        if not self.db.connect():
            self.show_error("Database Connection Error",
                            "Could not connect to the database.")
            return

        # Initialize differential privacy manager
        self.dp_manager = DifferentialPrivacy()

        # Start with login screen
        self.show_login()

    def show_login(self):
        self.clear_window()
        self.login_screen = LoginScreen(self.root, self.handle_login)
        self.login_screen.pack(fill=tk.BOTH, expand=True)

    def handle_login(self, username, password):
        # TODO: Implement actual authentication
        # For now, just proceed to main window
        self.show_main_window()

    def show_main_window(self):
        self.clear_window()
        self.main_window = MainWindow(
            self.root,
            self.db,
            self.dp_manager
        )
        self.main_window.pack(fill=tk.BOTH, expand=True)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_error(self, title, message):
        tk.messagebox.showerror(title, message)

    def on_closing(self):
        if self.db:
            self.db.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()