import ttkbootstrap as ttk
from tkinter import messagebox
import bcrypt

class LoginScreen(ttk.Frame):
    def __init__(self, parent, db_connection, on_login):
        """
        Initializes the login screen.
        :param parent: The parent Tkinter container.
        :param db_connection: The database connection instance.
        :param on_login: Callback function triggered on successful login.
        """
        super().__init__(parent)
        self.db_connection = db_connection
        self.on_login = on_login
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style(theme="superhero")

        self.configure(bootstyle="superhero")
        login_frame = ttk.Frame(self, padding="40 30 40 30", style="dark.TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ttk.Label(
            login_frame,
            text="Login",
            font=("Helvetica", 24, "bold"),
            bootstyle="inverse-light"
        )
        title.pack(pady=(0, 20))

        username_label = ttk.Label(
            login_frame,
            text="Username:",
            font=("Helvetica", 12),
            bootstyle="light"
        )
        username_label.pack(anchor="w", pady=(10, 0))

        self.username_entry = ttk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bootstyle="light"
        )
        self.username_entry.pack(fill="x", pady=5, ipady=5)

        password_label = ttk.Label(
            login_frame,
            text="Password:",
            font=("Helvetica", 12),
            bootstyle="light"
        )
        password_label.pack(anchor="w", pady=(10, 0))

        self.password_entry = ttk.Entry(
            login_frame,
            show="*",
            font=("Helvetica", 12),
            bootstyle="light"
        )
        self.password_entry.pack(fill="x", pady=5, ipady=5)

        login_button = ttk.Button(
            login_frame,
            text="Login",
            command=self.handle_login,
            style="success.TButton",
            width=20
        )
        login_button.pack(pady=20)

        footer_label = ttk.Label(
            login_frame,
            text="© COMP430 DATA PRIVACY PROJECT.",
            font=("Helvetica", 9),
            bootstyle="secondary"
        )
        footer_label.pack(side="bottom", pady=(20, 0))

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Both username and password are required.")
            return

        try:
            query = "SELECT username, password_hash, role, budget FROM Users WHERE username = %s"
            params = (username,)

            if self.db_connection.execute_query(query, params):
                user_data = self.db_connection.fetchone()

                if user_data:
                    if bcrypt.checkpw(password.encode("utf-8"), user_data["password_hash"].encode("utf-8")):
                        self.on_login({"username": user_data["username"], "role": user_data["role"], "budget": user_data["budget"]})
                    else:
                        messagebox.showerror("Login Failed", "Invalid password.")
                else:
                    messagebox.showerror("Login Failed", "Username not found.")
            else:
                messagebox.showerror("Error", "Failed to execute database query.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")