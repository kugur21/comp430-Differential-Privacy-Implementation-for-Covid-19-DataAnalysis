import pandas as pd
from database.connection import DatabaseConnection
from utils.validators import validate_date, validate_numeric

def load_dataset(file_path, db_connection):
    """
    Loads a CSV dataset into the Patients table in the database.

    :param file_path: Path to the CSV file.
    :param db_connection: DatabaseConnection instance.
    """
    try:
        # Load the dataset
        data = pd.read_csv(file_path)
        print(f"Dataset loaded successfully with {len(data)} rows.")

        # Required columns
        required_columns = {
            "usmer", "medical_unit", "sex", "patient_type", "date_died",
            "intubed", "pneumonia", "age", "pregnant", "diabetes", "copd",
            "asthma", "inmsupr", "hipertension", "other_disease", "cardiovascular",
            "obesity", "renal_chronic", "tobacco", "classification_final", "icu"
        }

        # Validate columns
        if not required_columns.issubset(data.columns):
            print("Dataset is missing required columns.")
            return

        # Validate and insert records
        valid_records = 0
        for _, row in data.iterrows():
            if not validate_numeric(row["age"]) or not validate_numeric(row["icu"]):
                print(f"Skipping invalid row: {row.to_dict()}")
                continue

            # Validate the date
            if not validate_date(row["date_died"]):
                print(f"Skipping invalid date in row: {row.to_dict()}")
                continue

            # Prepare the query and parameters
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

            # Execute the query
            if db_connection.execute_query(query, params):
                valid_records += 1

        print(f"Successfully inserted {valid_records} valid records into the database.")
    except Exception as e:
        print(f"An error occurred while processing the dataset: {e}")


if __name__ == "__main__":
    # Path to the dataset
    file_path = "/mnt/data/reducedCovidData (2).csv"

    # Initialize database connection
    db = DatabaseConnection()
    if db.connect():
        load_dataset(file_path, db)
        db.close()
    else:
        print("Failed to connect to the database.")
