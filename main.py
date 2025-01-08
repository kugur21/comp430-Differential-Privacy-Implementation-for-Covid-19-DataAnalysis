import mysql.connector
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ksu12345",
    auth_plugin='mysql_native_password'
)
db_cursor = db_connection.cursor(buffered=True)

# Helper Function: Populate Table from CSV with Date Conversion
def populate_table(file_path, insert_query):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[4]:  # 'date_died' sütununun CSV dosyasındaki indexi 4
                try:
                    row[4] = pd.to_datetime(row[4], format='%d/%m/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    row[4] = None  # Geçersiz tarihleri NULL olarak kaydet
            db_cursor.execute(insert_query, row)
    db_connection.commit()

# Initialize Database
db_cursor.execute("DROP DATABASE IF EXISTS covid_data")
db_cursor.execute("CREATE DATABASE IF NOT EXISTS covid_data")
db_cursor.execute("USE covid_data")

# Create Tables
db_cursor.execute("""
    CREATE TABLE Patients (
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
        icu INT
    )
""")

# Insert Data into the Patients Table
csv_file_path = "reducedCovidData.csv"
insert_query = """
    INSERT INTO Patients (
        usmer, medical_unit, sex, patient_type, date_died, intubed, pneumonia, age,
        pregnant, diabetes, copd, asthma, inmsupr, hipertension, other_disease,
        cardiovascular, obesity, renal_chronic, tobacco, classification_final, icu
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
populate_table(csv_file_path, insert_query)

# Tkinter Arayüzü
root = Tk()
root.title("Privacy-Preserving Data Analysis")
root.geometry("1200x800")

# Veri Tablosu
columns = [
    "patient_id", "usmer", "medical_unit", "sex", "patient_type", "age", "icu",
    "intubed", "pneumonia", "pregnant", "diabetes"
]
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.pack(fill=BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)


# Başlangıçta Tüm Verileri Konsola Yazdır
def print_all_columns_and_data():
    # Sütun adlarını alma
    db_cursor.execute("SHOW COLUMNS FROM Patients")
    columns = [column[0] for column in db_cursor.fetchall()]
    print("Columns:", columns)

    # Tüm verileri alma
    db_cursor.execute("SELECT * FROM Patients")
    rows = db_cursor.fetchall()
    print("Data:")
    for row in rows:
        print(row)


# Kodun başlangıcında tüm verileri ve sütunları yazdır
print_all_columns_and_data()


# Veri Gösterme Fonksiyonu
def display_data():
    for i in tree.get_children():
        tree.delete(i)
    db_cursor.execute(f"SELECT {', '.join(columns)} FROM Patients")
    rows = db_cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Gaussian Noise Tüm Verilere Uygula
# Gaussian Noise Tüm Verilere Uygula
def apply_gaussian_noise():
    # Veriyi çekiyoruz
    db_cursor.execute("SELECT pneumonia FROM Patients")
    rows = db_cursor.fetchall()
    pneumonia_values = [row[0] for row in rows]

    # Gaussian Noise ekliyoruz
    epsilon = 1.0
    scale = 1 / epsilon
    noisy_pneumonia = [value + np.random.normal(0, scale) for value in pneumonia_values]

    # Noisy sonuçları göstermek için yeni pencere oluşturuyoruz
    noisy_window = Toplevel(root)
    noisy_window.title("Noisy Pneumonia Values")
    noisy_window.geometry("800x600")
    noisy_tree = ttk.Treeview(noisy_window, columns=("Original Pneumonia", "Noisy Pneumonia"), show="headings")
    noisy_tree.pack(fill=BOTH, expand=True)
    noisy_tree.heading("Original Pneumonia", text="Original Pneumonia")
    noisy_tree.heading("Noisy Pneumonia", text="Noisy Pneumonia")

    for original, noisy in zip(pneumonia_values, noisy_pneumonia):
        noisy_tree.insert("", "end", values=(original, round(noisy, 2)))

    # Pasta grafiği Tkinter içinde gösterme
    def show_pie_chart():
        pneumonia_counts = pd.Series(pneumonia_values).value_counts().nlargest(10)

        # Matplotlib Figure oluştur
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.pie(pneumonia_counts, labels=pneumonia_counts.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Top Pneumonia Status Distribution")

        # Figure'ı Tkinter içine göm
        chart_window = Toplevel(noisy_window)
        chart_window.title("Pneumonia Distribution Pie Chart")
        chart_window.geometry("700x700")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    Button(noisy_window, text="Show Top Pneumonia Status (Pie Chart)", command=show_pie_chart).pack(pady=10)

# Report Noisy Max
def report_noisy_max_date_died():
    # Query to group deaths by date and count occurrences
    db_cursor.execute("SELECT date_died, COUNT(*) FROM Patients WHERE date_died IS NOT NULL GROUP BY date_died")
    rows = db_cursor.fetchall()

    # Extract dates and counts
    dates = [row[0].strftime('%Y-%m-%d') for row in rows]
    counts = [row[1] for row in rows]

    # Apply Laplace noise
    epsilon = 1.0
    noisy_counts = [count + np.random.laplace(0, 1 / epsilon) for count in counts]

    # Create a new window to display results
    max_window = Toplevel(root)
    max_window.title("Report Noisy Max Result (Date Died)")
    max_window.geometry("800x600")

    # Treeview to display noisy results
    noisy_tree = ttk.Treeview(max_window, columns=("Date Died", "Original Count", "Noisy Count"), show="headings")
    noisy_tree.pack(fill=BOTH, expand=True)
    noisy_tree.heading("Date Died", text="Date Died")
    noisy_tree.heading("Original Count", text="Original Count")
    noisy_tree.heading("Noisy Count", text="Noisy Count")

    for date, original, noisy in zip(dates, counts, noisy_counts):
        noisy_tree.insert("", "end", values=(date, original, round(noisy, 2)))

    # Plot a bar chart of the top 10 dates with the most deaths
    def show_bar_chart():
        top_dates = pd.DataFrame({"Date Died": dates, "Count": counts}).nlargest(10, "Count")

        # Matplotlib Figure
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.bar(top_dates["Date Died"], top_dates["Count"], color="skyblue")
        ax.set_title("Top 10 Dates with Most Deaths")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)

        # Embed the chart in a new window
        chart_window = Toplevel(max_window)
        chart_window.title("Top 10 Death Dates (Bar Chart)")
        chart_window.geometry("900x600")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    Button(max_window, text="Show Top 10 Dates (Bar Chart)", command=show_bar_chart).pack(pady=10)

    # Display the noisy maximum
    max_date = dates[np.argmax(noisy_counts)]
    Label(max_window, text=f"Most Frequent Death Date (Noisy): {max_date}", font=("Arial", 14)).pack(pady=10)

# Exponential Mechanism
def exponential_mechanism_patient_type():
    # Query to group patient types and count occurrences
    db_cursor.execute("SELECT patient_type, COUNT(*) FROM Patients GROUP BY patient_type")
    rows = db_cursor.fetchall()

    # Extract patient types and counts
    patient_types = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    # Assign utility scores (normalized counts as an example)
    total_count = sum(counts)
    utility_scores = [count / total_count for count in counts]

    # Calculate probabilities using exponential mechanism
    epsilon = 1.0
    probabilities = np.exp([utility * epsilon for utility in utility_scores])
    probabilities /= probabilities.sum()  # Normalize to make probabilities sum to 1

    # Select a patient type based on probabilities
    chosen_patient_type = np.random.choice(patient_types, p=probabilities)

    # Create a new window to display results
    exp_window = Toplevel(root)
    exp_window.title("Exponential Mechanism Result (Patient Type)")
    exp_window.geometry("800x600")

    # Treeview to display results
    exp_tree = ttk.Treeview(exp_window, columns=("Patient Type", "Count", "Utility Score", "Probability"), show="headings")
    exp_tree.pack(fill=BOTH, expand=True)
    exp_tree.heading("Patient Type", text="Patient Type")
    exp_tree.heading("Count", text="Count")
    exp_tree.heading("Utility Score", text="Utility Score")
    exp_tree.heading("Probability", text="Probability")

    for patient_type, count, utility, prob in zip(patient_types, counts, utility_scores, probabilities):
        exp_tree.insert("", "end", values=(patient_type, count, round(utility, 4), round(prob, 4)))

    # Display the selected patient type
    Label(exp_window, text=f"Selected Patient Type (Differentially Private): {chosen_patient_type}", font=("Arial", 14)).pack(pady=10)

    # Button to display pie chart
    def show_pie_chart():
        # Create a dataframe for plotting
        df = pd.DataFrame({"Patient Type": patient_types, "Count": counts})
        df_sorted = df.sort_values(by="Count", ascending=False)

        # Create a pie chart
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.pie(
            df_sorted["Count"],
            labels=df_sorted["Patient Type"],
            autopct="%1.1f%%",
            startangle=140,
        )
        ax.set_title("Patient Type Distribution")

        # Embed the chart in a new window
        chart_window = Toplevel(exp_window)
        chart_window.title("Patient Type Pie Chart")
        chart_window.geometry("700x700")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Add button to the window
    Button(exp_window, text="Show Patient Type Pie Chart", command=show_pie_chart).pack(pady=10)

# Düğmeler
button_frame = Frame(root)
button_frame.pack(fill=X, pady=10)

show_data_button = Button(button_frame, text="Show All Data", command=display_data)
show_data_button.pack(side=LEFT, padx=10)

apply_noise_button = Button(button_frame, text="Apply Gaussian Noise (Pneumonia)", command=apply_gaussian_noise)
apply_noise_button.pack(side=LEFT, padx=10)

noisy_max_date_button = Button(button_frame, text="Report Noisy Max (Date Died)", command=report_noisy_max_date_died)
noisy_max_date_button.pack(side=LEFT, padx=10)


exp_mechanism_patient_type_button = Button(button_frame, text="Exponential Mechanism (Patient Type)", command=exponential_mechanism_patient_type)
exp_mechanism_patient_type_button.pack(side=LEFT, padx=10)


# Tkinter Döngüsü
root.mainloop()

# Close the connection
db_cursor.close()
db_connection.close()
