import csv
import os
from datetime import datetime

# Ensure path is relative to project root, not src/
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # goes up one level from /src
DATA_DIR = os.path.join(BASE_DIR, "data")
USAGE_LOG_FILE = os.path.join(DATA_DIR, "usage_log.csv")

def log_usage(username, role, login_time, action="Unknown", status="Success"):
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data/ folder exists

    try:
        file_exists = os.path.exists(USAGE_LOG_FILE)
        with open(USAGE_LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Username", "Role", "Login_Time", "Action", "Status"])
            writer.writerow([username, role, login_time, action, status])

        # Confirm location
        print(f"[LOG] Entry saved to: {USAGE_LOG_FILE}")

    except Exception as e:
        print(f"[ERROR] Failed to log usage: {e}")




