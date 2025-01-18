import pandas as pd
from tkinter import filedialog, messagebox, ttk
from utils.validators import validate_date, validate_numeric

class UploadView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ttk.Label(self, text="Upload Dataset", font=("TkDefaultFont", 16, "bold"))
        title.pack(pady=10)

        # Upload button
        upload_button = ttk.Button(self, text="Upload CSV", command=self.upload_csv, style="primary.TButton")
        upload_button.pack(pady=20)

    def upload_csv(self):
        # Open file dialog
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        # Load the dataset
        try:
            data = pd.read_csv(file_path)
            print(f"Dataset loaded successfully with {len(data)} rows.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dataset: {e}")
            return

        # Validate and insert the dataset
        self.validate_and_insert_data(data)

    def validate_and_insert_data(self, data):
        required_columns = {
            "usmer", "medical_unit", "sex", "patient_type", "date_died",
            "intubed", "pneumonia", "age", "pregnant", "diabetes", "copd",
            "asthma", "inmsupr", "hipertension", "other_disease", "cardiovascular",
            "obesity", "renal_chronic", "tobacco", "classification_final", "icu"
        }

        # Check for required columns
        if not required_columns.issubset(data.columns):
            messagebox.showerror("Error", "The dataset is missing required columns.")
            return

        valid_records = 0
        for _, row in data.iterrows():
            # Validate individual fields
            if not validate_numeric(row["age"]) or not validate_numeric(row["icu"]):
                print(f"Skipping invalid row: {row.to_dict()}")
                continue
            if not validate_date(row["date_died"]):
                print(f"Skipping invalid date in row: {row.to_dict()}")
                continue

            # Prepare and execute the query
            query = """
                INSERT INTO Patients (
                    usmer, medical_unit, sex, patient_type, date_died, intubed, pneumonia,
                    age, pregnant, diabetes, copd, asthma, inmsupr, hipertension, other_disease,
                    cardiovascular, obesity, renal_chronic, tobacco, classification_final, icu
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            params = (
                row["usmer"], row["medical_unit"], row["sex"], row["patient_type"],
                row["date_died"], row["intubed"], row["pneumonia"], row["age"],
                row["pregnant"], row["diabetes"], row["copd"], row["asthma"],
                row["inmsupr"], row["hipertension"], row["other_disease"],
                row["cardiovascular"], row["obesity"], row["renal_chronic"],
                row["tobacco"], row["classification_final"], row["icu"]
            )

            if self.db_connection.execute_query(query, params):
                valid_records += 1

        messagebox.showinfo("Success", f"Uploaded {valid_records} valid records successfully.")
