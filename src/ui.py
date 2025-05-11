def authenticate(username, password):
    try:
        with open(CREDENTIALS_FILE, newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                print(f"Row read: {row}")  # Debugging line
                if len(row) != 4:
                    continue  # Skip malformed rows
                _, u, p, role = row
                if username == u and password == p:
                    print(f"Login successful for user: {u}")  # Debugging line
                    role = role.strip().lower()  # Strip any whitespace
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


