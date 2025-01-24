from tkinter import ttk, messagebox, filedialog
import pandas as pd


class UploadView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        disclaimer_frame = ttk.LabelFrame(self, text="Data Format Requirements", padding=10)
        disclaimer_frame.pack(fill="x", padx=10, pady=10)

        disclaimer_text = (
            "Ensure the uploaded CSV file has the following columns:\n"
            "USMER, MEDICAL_UNIT, SEX, PATIENT_TYPE, DATE_DIED, INTUBED, PNEUMONIA, AGE, PREGNANT, DIABETES, "
            "COPD, ASTHMA, INMSUPR, HIPERTENSION, OTHER_DISEASE, CARDIOVASCULAR, OBESITY, RENAL_CHRONIC, "
            "TOBACCO, CLASIFFICATION_FINAL, ICU\n\n"
            "Column names are case-insensitive but must match exactly. Missing or invalid data will cause errors."
        )

        disclaimer_label = ttk.Label(
            disclaimer_frame, text=disclaimer_text, wraplength=600, justify="left"
        )
        disclaimer_label.pack(padx=10, pady=5)

        upload_frame = ttk.LabelFrame(self, text="Upload CSV", padding=10)
        upload_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            upload_frame, text="Select CSV File", command=self.upload_csv
        ).pack(side="left", padx=10, pady=5)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select CSV File", filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        try:
            data = pd.read_csv(file_path)
            print(f"Dataset loaded successfully with {len(data)} rows.")

            if self.validate_and_insert_data(data):
                messagebox.showinfo("Success", f"Data uploaded successfully with {len(data)} rows.")
                print(f"Data uploaded successfully with {len(data)} rows.")

                if hasattr(self.master, 'data_view') and hasattr(self.master.data_view, 'refresh_data'):
                    self.master.data_view.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload data: {str(e)}")
            print(f"Error: {str(e)}")

    def validate_and_insert_data(self, data):
        required_columns = [
            'USMER', 'MEDICAL_UNIT', 'SEX', 'PATIENT_TYPE', 'DATE_DIED', 'INTUBED',
            'PNEUMONIA', 'AGE', 'PREGNANT', 'DIABETES', 'COPD', 'ASTHMA', 'INMSUPR',
            'HIPERTENSION', 'OTHER_DISEASE', 'CARDIOVASCULAR', 'OBESITY', 'RENAL_CHRONIC',
            'TOBACCO', 'CLASIFFICATION_FINAL', 'ICU'
        ]

        data.columns = data.columns.str.upper()

        missing_columns = set(required_columns) - set(data.columns)
        if missing_columns:
            messagebox.showerror("Validation Error", f"Missing columns: {', '.join(missing_columns)}")
            print(f"Validation Error: Missing columns: {', '.join(missing_columns)}")
            return False

        if 'DATE_DIED' in data.columns:
            try:
                data['DATE_DIED'] = pd.to_datetime(
                    data['DATE_DIED'], format='%d/%m/%Y', errors='coerce'
                ).dt.strftime('%Y-%m-%d')
            except Exception as e:
                messagebox.showerror("Date Conversion Error", f"Failed to convert dates: {str(e)}")
                print(f"Date Conversion Error: {str(e)}")
                return False

        try:
            query = """
                INSERT INTO Patients (
                    usmer, medical_unit, sex, patient_type, date_died, intubed,
                    pneumonia, age, pregnant, diabetes, copd, asthma, inmsupr,
                    hipertension, other_disease, cardiovascular, obesity, renal_chronic,
                    tobacco, classification_final, icu
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for _, row in data.iterrows():
                self.db_connection.execute_query(query, tuple(row[col] for col in required_columns))

            return True
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to insert data: {str(e)}")
            print(f"Database Error: {str(e)}")
            return False
