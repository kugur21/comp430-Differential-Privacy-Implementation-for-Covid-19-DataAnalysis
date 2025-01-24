import csv
from datetime import datetime

from database.schema import CREATE_TABLES_QUERIES

def initialize_database(db_connection):
    """
    Initializes the database by creating necessary tables if they don't exist.
    :param db_connection: The database connection instance.
    """
    create_db_query = """CREATE DATABASE IF NOT EXISTS covid_data;"""
    db_connection.execute_query(create_db_query)
    use_db_query = """USE covid_data;"""
    db_connection.execute_query(use_db_query)
    for table_name, query in CREATE_TABLES_QUERIES.items():
        try:
            db_connection.execute_query(query)
            print(f"Table {table_name} created or already exists.")
        except Exception as e:
            print(f"Error creating table {table_name}: {e}")


def insert_data_from_csv(db_connection, csv_file_path, table_name):
    """
    Reads data from a CSV file and inserts it into the specified table if the data doesn't already exist.
    :param db_connection: The database connection instance.
    :param csv_file_path: Path to the CSV file.
    :param table_name: Name of the table to insert data into.
    """
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)

            if table_name == 'users':
                query = "SELECT * FROM Users"
                db_connection.execute_query(query)
                if not db_connection.fetchone():
                    for row in csv_reader:
                        columns = "username, password_hash, role, budget"
                        placeholders = "%s, %s, %s, %s"
                        values = (
                            row['username'],
                            row['hashed_password'],
                            row['role'],
                            row['budget'],
                        )
                        insert_query = f"INSERT INTO Users ({columns}) VALUES ({placeholders})"
                        db_connection.execute_query(insert_query, values)
            elif table_name == 'patients':
                query = "SELECT * FROM Patients"
                db_connection.execute_query(query)
                if not db_connection.fetchone():
                    for row in csv_reader:
                        if row['DATE_DIED'] == '9999-99-99':
                            row['DATE_DIED'] = None
                        else:
                            row['DATE_DIED'] = datetime.strptime(row['DATE_DIED'], '%d/%m/%Y').strftime('%Y-%m-%d')
                        columns = ", ".join(row.keys())
                        placeholders = ", ".join(["%s"] * len(row))
                        values = list(row.values())
                        insert_query = f"INSERT INTO Patients ({columns}) VALUES ({placeholders})"
                        db_connection.execute_query(insert_query, values)
    except Exception as e:
        print(f"Error processing CSV file {csv_file_path}: {e}")


def load_data(db_connection, accounts_csv_path, covid_data_csv_path):
    """
    Initializes the database by inserting data from CSV files if they don't already exist.
    :param db_connection: The database connection instance.
    """

    insert_data_from_csv(db_connection, accounts_csv_path, 'users')

    insert_data_from_csv(db_connection, covid_data_csv_path, 'patients')
