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
        self.db_connection = db_connection  # Store the database connection
        self.on_login = on_login
        self.setup_ui()

    def setup_ui(self):
        # Create the login frame
        login_frame = ttk.Frame(self, padding="20")
        login_frame.pack(expand=True)

        # Title
        title = ttk.Label(login_frame, text="Login", font=("TkDefaultFont", 20, "bold"))
        title.pack(pady=10)

        # Username
        username_label = ttk.Label(login_frame, text="Username:")
        username_label.pack(anchor="w")
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.pack(fill="x", pady=5)

        # Password
        password_label = ttk.Label(login_frame, text="Password:")
        password_label.pack(anchor="w")
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.pack(fill="x", pady=5)

        # Login Button
        login_button = ttk.Button(login_frame, text="Login", command=self.handle_login, style="primary.TButton")
        login_button.pack(pady=10)

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