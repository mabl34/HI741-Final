import tkinter as tk
import csv
from tkinter import messagebox, simpledialog
from src.user import User, Nurse, Clinician, Admin, Management
from src.data_handler import load_patient_data
from src.logger import log_usage 
from datetime import datetime

# Path to credentials file (CSV with Username, Password, Role columns)
CREDENTIALS_FILE = "data/Credentials.csv"
PATIENT_DATA_FILE = "data/Patient_data.csv"
NOTE_DATA_FILE = "data/Notes.csv"


def authenticate(username, password):
    try:
        with open(CREDENTIALS_FILE, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 4:
                    continue  # Skip malformed rows
                _, u, p, role = row  # Ignore index column
                if username == u and password == p:
                    role = role.lower()
                    data_file = PATIENT_DATA_FILE
                    note_file = NOTE_DATA_FILE
                    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Create user object and log successful login
                    if role == "nurse":
                        user = Nurse(username, role, data_file, note_file)
                    elif role == "clinician":
                        user = Clinician(username, role, data_file, note_file)
                    elif role == "admin":
                        user = Admin(username, role, data_file, note_file)
                    elif role == "management":
                        user = Management(username, role, data_file, note_file)
                    else:
                        messagebox.showerror("Login Failed", "Invalid role.")
                        return None
                    
                    log_usage(username, role, login_time, action="Login", status="Success")
                    return user

        # Log failed login
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_usage(username, "Unknown", login_time, action="Login", status="Failed")
        messagebox.showerror("Login Failed", "Invalid username or password.")
        return None

    except FileNotFoundError:
        messagebox.showerror("Error", "Credentials file not found.")
        return None


        
        

        


def launch_ui():
    root = tk.Tk()
    root.title("Hospital Data System Login")
    root.geometry("300x200")

    tk.Label(root, text="Username").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        user = authenticate(username, password)
        if user:
            root.destroy()
            patients = load_patient_data(PATIENT_DATA_FILE)
            show_menu(user, patients)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)

    root.mainloop()

def show_menu(user, patients):
    menu = tk.Tk()
    menu.title(f"{user.__class__.__name__} Menu")
    menu.geometry("400x300")

    def wrap_and_return_to_menu(func):
        def wrapped():
            func(patients)
        return wrapped

    # Buttons for each role
    if isinstance(user, (Nurse, Clinician)):
        tk.Button(menu, text="Retrieve Patient", command=lambda: user.retrieve_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Add Patient", command=lambda: user.add_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Remove Patient", command=lambda: user.remove_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Count Visits", command=lambda: user.count_visits_ui(menu)).pack(pady=5)
        tk.Button(menu, text="View Note", command=lambda: user.view_note_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Exit", command=menu.destroy).pack(pady=5)


    if isinstance(user, (Admin)):
        tk.Button(menu, text="Count Visits", command=lambda: user.start_session_ui(patients)).pack(pady=10)
        tk.Button(menu, text="Exit", command=menu.destroy).pack(pady=10)
    
    elif isinstance(user, (Management)):
        tk.Button(menu, text="Generate Statistics", command=lambda: user.generate_statistics_ui(patients)).pack(pady=10)
        tk.Button(menu, text="Exit", command=menu.destroy).pack(pady=10)

    menu.mainloop()


