import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class DataView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        # Title
        title = ttk.Label(self, text="Data Viewer", font=("TkDefaultFont", 16, "bold"))
        title.pack(pady=10)

        # Search bar
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=5)
        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Search", command=self.perform_search, style="primary.TButton").pack(side="left")

        # Data table
        self.table = ttk.Treeview(self, columns=("ID", "Age", "ICU", "Pneumonia"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Age", text="Age")
        self.table.heading("ICU", text="ICU")
        self.table.heading("Pneumonia", text="Pneumonia")
        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self, filters=None):
        # Query the database and populate the table
        query = "SELECT patient_id, age, icu, pneumonia FROM Patients"
        if filters:
            query += f" WHERE {filters}"
        self.db_connection.execute_query(query)
        for row in self.db_connection.cursor.fetchall():
            self.table.insert("", "end", values=(row['patient_id'], row['age'], row['icu'], row['pneumonia']))

    def perform_search(self):
        search_term = self.search_entry.get()
        filters = f"age = {search_term}" if search_term.isdigit() else None
        self.table.delete(*self.table.get_children())
        self.load_data(filters)

    def refresh_data(self):
        # Clear existing rows in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch the latest data from the database
        query = """
            SELECT patient_id, usmer, medical_unit, sex, patient_type,
                   pneumonia, age, diabetes, icu
            FROM Patients
            LIMIT 1000
        """
        self.master.db_connection.execute_query(query)
        rows = self.master.db_connection.cursor.fetchall()

        # Insert the fetched data into the Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)
