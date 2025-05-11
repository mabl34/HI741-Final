import csv
from datetime import datetime
import os

# Path to data/usage_log.csv relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # One level up from src/
DATA_DIR = os.path.join(BASE_DIR, "data")
USAGE_LOG_FILE = os.path.join(DATA_DIR, "usage_log.csv")

def log_usage(username, role, login_time, action="Unknown", status="Success"):
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_exists = os.path.isfile(USAGE_LOG_FILE)
    try:
        with open(USAGE_LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Username", "Role", "Login_Time", "Action", "Status"])
            writer.writerow([username, role, login_time, action, status])

        # Debug log to confirm logging worked
        print(f"[LOG] {username} ({role}) at {login_time} -> {action} [{status}]")

    except Exception as e:
        print(f"[ERROR] Failed to log usage: {e}")



