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
tree = ttk.Treeview(root, columns=("patient_id", "usmer", "medical_unit", "sex", "age", "icu"), show="headings")
tree.pack(fill=BOTH, expand=True)

for col in ["patient_id", "usmer", "medical_unit", "sex", "age", "icu"]:
    tree.heading(col, text=col)

# Veri Gösterme Fonksiyonu
def display_data():
    for i in tree.get_children():
        tree.delete(i)
    db_cursor.execute("SELECT patient_id, usmer, medical_unit, sex, age, icu FROM Patients")
    rows = db_cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Gaussian Noise Tüm Verilere Uygula
# Gaussian Noise Tüm Verilere Uygula
def apply_gaussian_noise():
    db_cursor.execute("SELECT age FROM Patients")
    rows = db_cursor.fetchall()
    ages = [row[0] for row in rows]

    epsilon = 1.0
    scale = 1 / epsilon
    noisy_ages = [age + np.random.normal(0, scale) for age in ages]

    noisy_window = Toplevel(root)
    noisy_window.title("Noisy Ages")
    noisy_window.geometry("800x600")  # Sekme boyutunu artırıyoruz
    noisy_tree = ttk.Treeview(noisy_window, columns=("Original Age", "Noisy Age"), show="headings")
    noisy_tree.pack(fill=BOTH, expand=True)
    noisy_tree.heading("Original Age", text="Original Age")
    noisy_tree.heading("Noisy Age", text="Noisy Age")

    for original, noisy in zip(ages, noisy_ages):
        noisy_tree.insert("", "end", values=(original, round(noisy, 2)))

    # Pasta grafiği Tkinter içinde gösterme
    def show_pie_chart():
        age_counts = pd.Series(ages).value_counts().nlargest(10)

        # Matplotlib Figure oluştur
        fig = Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Top 10 Most Frequent Ages")

        # Figure'ı Tkinter içine göm
        chart_window = Toplevel(noisy_window)
        chart_window.title("Age Distribution Pie Chart")
        chart_window.geometry("700x700")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    Button(noisy_window, text="Show Top 10 Ages (Pie Chart)", command=show_pie_chart).pack(pady=10)
# Report Noisy Max
def report_noisy_max():
    db_cursor.execute("SELECT sex, COUNT(*) FROM Patients GROUP BY sex")
    rows = db_cursor.fetchall()

    epsilon = 1.0
    noisy_counts = [count + np.random.laplace(0, 1 / epsilon) for _, count in rows]
    categories = [row[0] for row in rows]

    max_category = categories[np.argmax(noisy_counts)]

    max_window = Toplevel(root)
    max_window.title("Report Noisy Max Result")
    max_window.geometry("400x200")  # Sekme boyutunu artırıyoruz
    Label(max_window, text=f"Most Frequent Category (Noisy): {max_category}", font=("Arial", 14)).pack(pady=20)

# Exponential Mechanism
def exponential_mechanism():
    utility_scores = [("Yes", 0.8), ("No", 0.6), ("Maybe", 0.7)]
    epsilon = 1.0

    probabilities = np.exp([score * epsilon / 2 for _, score in utility_scores])
    probabilities /= probabilities.sum()

    chosen_option = np.random.choice([item for item, _ in utility_scores], p=probabilities)

    exp_window = Toplevel(root)
    exp_window.title("Exponential Mechanism Result")
    exp_window.geometry("400x200")  # Sekme boyutunu artırıyoruz
    Label(exp_window, text=f"Selected Option: {chosen_option}", font=("Arial", 14)).pack(pady=20)

# Düğmeler
button_frame = Frame(root)
button_frame.pack(fill=X, pady=10)

show_data_button = Button(button_frame, text="Show All Data", command=display_data)
show_data_button.pack(side=LEFT, padx=10)

apply_noise_button = Button(button_frame, text="Apply Gaussian Noise (AGE)", command=apply_gaussian_noise)
apply_noise_button.pack(side=LEFT, padx=10)

noisy_max_button = Button(button_frame, text="Report Noisy Max (Sex)", command=report_noisy_max)
noisy_max_button.pack(side=LEFT, padx=10)

exp_mechanism_button = Button(button_frame, text="Exponential Mechanism", command=exponential_mechanism)
exp_mechanism_button.pack(side=LEFT, padx=10)

# Tkinter Döngüsü
root.mainloop()

# Close the connection
db_cursor.close()
db_connection.close()
