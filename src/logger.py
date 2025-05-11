import csv
from datetime import datetime
import os

USAGE_LOG_FILE = os.path.join(os.path.dirname(__file__), "usage_log.csv")

def log_usage(username, role, login_time, action="Unknown", status="Success"):
    file_exists = os.path.isfile(USAGE_LOG_FILE)
    try:
        with open(USAGE_LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Username", "Role", "Login_Time", "Action", "Status"])
            writer.writerow([username, role, login_time, action, status])
        
        # ✅ Debug print to terminal
        #print(f"[LOG] {username} ({role}) at {login_time} -> {action} [{status}]")

    except Exception as e:
        print(f"[ERROR] Failed to log usage: {e}")


