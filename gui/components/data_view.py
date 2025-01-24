import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class DataView(ttk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.current_page = 1
        self.rows_per_page = 10
        self.total_rows = 0
        self.setup_ui()

    def setup_ui(self):
        title = ttk.Label(self, text="Data Viewer", font=("TkDefaultFont", 16, "bold"))
        title.pack(pady=10)

        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left", padx=5)
        self.search_field = ttk.Combobox(search_frame,
                                         values=["Age", "Sex", "Patient Type", "Medical Unit"],
                                         width=15)
        self.search_field.set("Age")
        self.search_field.pack(side="left", padx=5)

        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side="left", padx=5)

        ttk.Button(search_frame, text="Search",
                   command=self.perform_search,
                   style="primary.TButton").pack(side="left", padx=5)

        ttk.Button(search_frame, text="Reset",
                   command=self.load_data).pack(side="left")

        rows_per_page_frame = ttk.Frame(self)
        rows_per_page_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(rows_per_page_frame, text="Rows per page:").pack(side="left", padx=5)
        self.rows_per_page_entry = ttk.Entry(rows_per_page_frame, width=5)
        self.rows_per_page_entry.insert(0, "10")
        self.rows_per_page_entry.pack(side="left", padx=5)

        ttk.Button(rows_per_page_frame, text="Apply",
                   command=self.update_rows_per_page).pack(side="left", padx=5)

        self.columns = [
            "patient_id", "usmer", "medical_unit", "sex", "patient_type", "date_died",
            "intubed", "pneumonia", "age", "pregnant", "diabetes", "copd", "asthma",
            "inmsupr", "hipertension", "other_disease", "cardiovascular", "obesity",
            "renal_chronic", "tobacco", "classification_final", "icu"
        ]

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.table = ttk.Treeview(table_frame, columns=self.columns, show="headings", height=20)

        y_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)

        self.table.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        for col in self.columns:
            display_name = col.replace("_", " ").title()
            self.table.heading(col, text=display_name,
                               command=lambda c=col: self.sort_column(c))
            width = 70 if col in ["patient_id", "age", "usmer"] else 100
            self.table.column(col, anchor="center", width=width, minwidth=50)

        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(fill="x", padx=10, pady=5)

        self.previous_button = ttk.Button(pagination_frame, text="Previous", command=self.previous_page)
        self.previous_button.pack(side="left", padx=5)

        self.page_label = ttk.Label(pagination_frame, text=f"Page {self.current_page}")
        self.page_label.pack(side="left", padx=5)

        self.next_button = ttk.Button(pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="left", padx=5)

        self.load_data()

    def load_data(self, filters=None):
        try:
            for item in self.table.get_children():
                self.table.delete(item)

            offset = (self.current_page - 1) * self.rows_per_page

            query = """
                SELECT patient_id, usmer, medical_unit, sex, patient_type, date_died, intubed, pneumonia,
                       age, pregnant, diabetes, copd, asthma, inmsupr, hipertension, other_disease,
                       cardiovascular, obesity, renal_chronic, tobacco, classification_final, icu
                FROM Patients
            """

            if filters:
                query += f" WHERE {filters}"

            query += f" LIMIT {self.rows_per_page} OFFSET {offset}"

            self.db_connection.execute_query(query)
            rows = self.db_connection.cursor.fetchall()

            for row in rows:
                self.table.insert("", "end", values=tuple(row.values()))

            self.update_total_rows(filters)
            self.update_pagination_controls()
        except Exception as e:
            print(f"Error loading data: {e}")

    def update_total_rows(self, filters=None):
        try:
            query = "SELECT COUNT(*) AS total FROM Patients"
            if filters:
                query += f" WHERE {filters}"

            self.db_connection.execute_query(query)
            result = self.db_connection.cursor.fetchone()

            if result:
                self.total_rows = int(result["total"])
            else:
                self.total_rows = 0
        except Exception as e:
            print(f"Error updating total rows: {e}")
            self.total_rows = 0

    def update_pagination_controls(self):
        self.page_label.config(text=f"Page {self.current_page}")
        self.previous_button.config(state="normal" if self.current_page > 1 else "disabled")
        total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page
        self.next_button.config(state="normal" if self.current_page < total_pages else "disabled")

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_data()

    def perform_search(self):
        search_field = self.search_field.get().lower()
        search_term = self.search_entry.get()

        if search_term.isdigit():
            filters = f"{search_field} = {search_term}"
        else:
            filters = f"{search_field} LIKE '%{search_term}%'"

        self.current_page = 1
        self.load_data(filters)

    def update_rows_per_page(self):
        try:
            self.rows_per_page = int(self.rows_per_page_entry.get())
            self.current_page = 1
            self.load_data()
        except ValueError:
            ttk.Messagebox.show_error(title="Error", message="Please enter a valid number for rows per page.")

    def sort_column(self, column):
        rows = [(self.table.set(k, column), k) for k in self.table.get_children("")]
        rows.sort(key=lambda x: x[0])

        for index, (_, k) in enumerate(rows):
            self.table.move(k, "", index)

    def refresh_data(self):
        self.load_data()