#!/usr/bin/env python
# coding: utf-8

# cli.py

import argparse
import sys
from datetime import datetime
from src.data_handler import load_patient_data
from src.user import User, Nurse, Clinician, Admin, Management
from src.user import authenticate_user

def main():
    parser = argparse.ArgumentParser(description="Healthcare CLI Application")
    parser.add_argument("-username", required=True, help="Username for login")
    parser.add_argument("-password", required=True, help="Password for login")

    # Set default values for credentials and data file
    parser.add_argument(
        "-credentials", default="PA3_credentials.csv",
        help="Path to credentials CSV file (default: PA3_credentials.csv)"
    )
    parser.add_argument(
        "-data", default="PA3_data.csv",
        help="Path to patient data file (default: PA3_data.csv)"
    )
    
    parser.add_argument(
        "-note", default="PA3_Notes.csv",
        help="Path to patient note file (default: PA3_Notes.csv)"
    )


    args = parser.parse_args()

    
    

    # Authenticate user
    role = authenticate_user(args.username, args.password, args.credentials)
    if not role:
        print("Authentication failed. Check your username or password.")
        sys.exit(1)

    # Load patient data
    patients = load_patient_data(args.data)

    # Initialize correct user role
    user_class = {
        "nurse": Nurse,
        "clinician": Clinician,
        "admin": Admin,
        "management": Management
    }.get(role, None)

    if user_class is None:
        print(f"Unknown role: {role}")
        sys.exit(1)

    print(f"Welcome, {args.username}! Role: {role.capitalize()}")

    # Create an instance of the user with their role
    user_instance = user_class(args.username, role, args.data, args.note)  # Pass role instead of password

    user_instance.start_session(patients)


if __name__ == "__main__":
    main()





