#!/usr/bin/env python
# coding: utf-8

# user.py


import csv
import sys
import random
from datetime import datetime
from src.patient import Patient
from src.visit import Visit
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.ticker as ticker 
import tkinter as tk
from tkinter import Toplevel, messagebox
import pandas as pd
from src.data_handler import load_patient_data
from src.logger import log_usage




def authenticate_user(username, password, credentials_file):
    with open(credentials_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return row["role"].lower()
    return None


class User:
    def __init__(self, username, role, data_file, note_file):
        self.username = username
        self.role = role
        self.data_file = data_file
        self.note_file = note_file


    def start_session(self, patients):
        raise NotImplementedError("Subclass must implement session behavior")

    


class Nurse(User):
    def __init__(self, username, role, data_file, note_file):
        super().__init__(username, role, data_file, note_file)
        self.data_file = data_file
        self.note_file = note_file
        self.patients = load_patient_data(data_file)

    def start_session_ui(self, root):
        self.patients = load_patient_data(self.data_file)
        menu = tk.Toplevel(root)
        menu.title("Nurse Dashboard")

        tk.Label(menu, text="Nurse Actions").pack(pady=10)
        tk.Button(menu, text="Add Patient", command=lambda: self.add_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Remove Patient", command=lambda: self.remove_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="Retrieve Patient", command=lambda: self.retrieve_patient_ui(menu)).pack(pady=5)
        tk.Button(menu, text="View Note", command=lambda: self.view_note_ui(menu)).pack(pady=5)

    def add_patient_ui(self, root):
        win = tk.Toplevel(root)
        win.title("Add Patient")

        fields = ["Patient_ID", "Visit Date (YYYY-MM-DD)", "Visit Department", "Chief Complaint", 
                  "Note ID", "Note Type", "Age", "Race", "Gender", "Ethnicity", "Zip Code", "Insurance"]
        entries = {field: tk.Entry(win) for field in fields}

        for field, entry in entries.items():
            tk.Label(win, text=field).pack()
            entry.pack()


        def add():
            try:
                patient_id = int(entries["Patient_ID"].get())
                visit_time = entries["Visit Date (YYYY-MM-DD)"].get()
                formatted_date = datetime.strptime(visit_time, "%Y-%m-%d").strftime("%m/%d/%Y")
                visit_id = random.randint(100000, 999999)
                visit_department = entries["Visit Department"].get()
                chief_complaint = entries["Chief Complaint"].get()
                note_id = entries["Note ID"].get()
                note_type = entries["Note Type"].get()
                age = int(entries["Age"].get())
                race = entries["Race"].get()
                gender = entries["Gender"].get()
                ethnicity = entries["Ethnicity"].get()
                zip_code = entries["Zip Code"].get()
                insurance = entries["Insurance"].get()

                if patient_id not in self.patients:
                    self.patients[patient_id] = Patient(patient_id, race, gender, ethnicity, zip_code, insurance)

                visit = Visit(visit_id, patient_id, formatted_date, visit_department, chief_complaint, note_id, note_type, age)
                self.patients[patient_id].add_visit(visit)

                with open(self.data_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([patient_id, visit_id, formatted_date, visit_department, race, gender,
                                     ethnicity, age, zip_code, insurance, chief_complaint, note_id, note_type])
                messagebox.showinfo("Success", f"Visit added for Patient {patient_id}.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Add Visit", command=add).pack(pady=10)
        
        log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             action="Add Patient", status="Success")


    def remove_patient_ui(self, root):
        win = tk.Toplevel(root)
        win.title("Remove Patient")

        tk.Label(win, text="Enter Patient_ID to remove:").pack()
        entry = tk.Entry(win)
        entry.pack()

        def remove():
            try:
                patient_id = int(entry.get())
                if patient_id in self.patients:
                    del self.patients[patient_id]
                    self.remove_patient_from_file(patient_id)
                    messagebox.showinfo("Success", f"Patient {patient_id} removed.")
                    win.destroy()
                else:
                    messagebox.showwarning("Not Found", f"Patient {patient_id} not found.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Remove", command=remove).pack(pady=5)
        
        log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          action="Remove Patient", status="Success")


    def remove_patient_from_file(self, patient_id):
        lines = []
        with open(self.data_file, mode="r") as file:
            reader = csv.reader(file)
            lines = [row for row in reader if row[0] != str(patient_id)]

        with open(self.data_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lines)

    def retrieve_patient_ui(self, root):
        win = tk.Toplevel(root)
        win.title("Retrieve Patient")

        tk.Label(win, text="Enter Patient ID to retrieve:").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        def retrieve():
            try:
                pid = int(entry.get())  # Convert input to int
                print("Looking for patient ID:", pid)
                patient = self.patients.get(pid)
                if patient:
                    info = f"Patient ID: {patient.patient_id}\n" \
                           f"Race: {patient.race}\n" \
                           f"Gender: {patient.gender}\n" \
                           f"Ethnicity: {patient.ethnicity}\n" \
                           f"Zip Code: {patient.zip_code}\n" \
                           f"Insurance: {patient.insurance}\n" \
                           f"Number of Visits: {len(patient.visits)}"\

                    if patient.visits:
                        try:
                            recent_visit = max(patient.visits, key=lambda v: datetime.strptime(v.visit_time, "%m/%d/%Y"))
                            visit_info = f"\n\nMost Recent Visit:\n" \
                                              f"Visit ID: {recent_visit.visit_id}\n" \
                                              f"Visit Time: {recent_visit.visit_time}\n" \
                                              f"Department: {recent_visit.visit_department}\n"\
                                              f"Age at Visit: {recent_visit.age}"
                            info += visit_info
                        except Exception as e:
                            info += f"\n\n[Error reading visit time: {str(e)}]"


                    messagebox.showinfo("Patient Found", info)
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Retrieve Patient", status="Success")
                else:
                    messagebox.showerror("Not Found", f"No patient with ID {pid}.")
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Retrieve Patient", status="Failed")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric Patient ID.")
                log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          action="Retrieve Patient", status="Failed")

        tk.Button(win, text="Retrieve", command=retrieve).pack(pady=10)





    def view_note_ui(self, root):
        win = tk.Toplevel(root)
        win.title("View Note")

        tk.Label(win, text="Patient_ID").pack()
        patient_id_entry = tk.Entry(win)
        patient_id_entry.pack()

        tk.Label(win, text="Visit Date (YYYY-MM-DD)").pack()
        visit_date_entry = tk.Entry(win)
        visit_date_entry.pack()

        def view_note():
            patient_id = patient_id_entry.get().strip()
            visit_date_input = visit_date_entry.get().strip()
            note_id = None

            try:
               input_date = datetime.strptime(visit_date_input, "%Y-%m-%d").strftime("%m/%d/%Y")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                with open(self.data_file, newline='', encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row["Patient_ID"].strip() == patient_id:
                            csv_date = datetime.strptime(row["Visit_time"].strip(), "%m/%d/%Y").strftime("%m/%d/%Y")
                            if csv_date == input_date:
                                note_id = row.get("Note_ID", "").strip()
                                break

                if not note_id:
                    messagebox.showinfo("Not Found", "No matching visit found.")
                    return

            except FileNotFoundError:
                messagebox.showerror("Error", f"{self.data_file} not found.")
                return

            try:
                with open(self.note_file, newline='', encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row["Note_ID"].strip() == note_id:
                            note_text = row["Note_text"].strip()
                        
                            # Note display window
                            note_window = tk.Toplevel(win)
                            note_window.title("Note Text")
                            note_window.geometry("600x400")

                            frame = tk.Frame(note_window)
                            frame.pack(fill="both", expand=True)

                            scrollbar = tk.Scrollbar(frame)
                            scrollbar.pack(side="right", fill="y")

                            text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
                            text_area.insert(tk.END, note_text)
                            text_area.config(state=tk.DISABLED)
                            text_area.pack(side="left", fill="both", expand=True)

                            scrollbar.config(command=text_area.yview)
                            return

                messagebox.showinfo("Not Found", "Note text not found.")

            except FileNotFoundError:
                messagebox.showerror("Error", f"{self.note_file} not found.")

        tk.Button(win, text="View Note", command=view_note).pack(pady=5)
        
        log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          action="View Note", status="Success")


    
    def count_visits_ui(self, root):
        
        def count_visits():
            date_input = entry.get().strip()
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a date in YYYY-MM-DD format.")
                return

            count = 0
            for p in self.patients.values():
                for v in p.get_visits():
                    try:
                        visit_date = datetime.strptime(v.visit_time, "%m/%d/%Y").strftime("%Y-%m-%d")
                        if visit_date == date_input:
                            count += 1
                    except ValueError:
                        print(f"Invalid date format: {v.visit_time}")

            messagebox.showinfo("Visit Count", f"Total visits on {date_input}: {count}")

        # Create a popup window
        win = Toplevel(root)
        win.title("Count Visits by Date")

        tk.Label(win, text="Enter date (YYYY-MM-DD):").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        tk.Button(win, text="Count Visits", command=count_visits).pack(pady=10)
        
        log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          action="Count Visits", status="Success")


   



class Clinician(Nurse):
    pass  # Same actions as Nurse; can extend if needed



class Admin(User):
    def __init__(self, username, role, data_file, note_file):
        super().__init__(username, role, data_file, note_file)
        self.data_file = data_file
        self.patients = {}

    def start_session_ui(self, patients):
        def count_visits():
            date_input = entry.get().strip()
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a date in YYYY-MM-DD format.")
                return

            count = 0
            for p in patients.values():
                for v in p.get_visits():
                    try:
                        visit_date = datetime.strptime(v.visit_time, "%m/%d/%Y").strftime("%Y-%m-%d")
                        if visit_date == date_input:
                            count += 1
                    except ValueError:
                        print(f"Invalid date format: {v.visit_time}")

            messagebox.showinfo("Visit Count", f"Total visits on {date_input}: {count}")

        # Create a popup window
        win = Toplevel()
        win.title("Count Visits by Date")

        tk.Label(win, text="Enter date (YYYY-MM-DD):").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        tk.Button(win, text="Count Visits", command=count_visits).pack(pady=10)
        
        log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          action="Count Visits", status="Success")



class Management(User):
    def __init__(self, username, role, data_file, note_file):
        super().__init__(username, role, data_file, note_file)

    def generate_statistics_ui(self, patients):
        try:
            df = pd.read_csv(self.data_file)
            stat_win = Toplevel()
            stat_win.title("Patient Statistics")

            def show_temporal_trend():
                try:
                    df['Visit_time'] = pd.to_datetime(df['Visit_time'], errors='coerce')
                    visits_by_date = df['Visit_time'].dt.date.value_counts().sort_index()
                    visits_by_date.plot(kind='line', title="Visits Over Time")
                    plt.xlabel("Date")
                    plt.ylabel("Number of Visits")
                    plt.tight_layout()
                    plt.show()
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Temporal Trends", status="Success")
                except Exception as e:
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Temporal Trends", status="Failed")

            def show_insurance_distribution():
                try:
                    df['Insurance'].value_counts().plot(kind='bar', title="Insurance Types")
                    plt.xlabel("Insurance")
                    plt.ylabel("Count")
                    plt.tight_layout()
                    plt.show()
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Insurance Distribution", status="Success")
                except Exception as e:
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Insurance Distribution", status="Failed")

            def show_race_distribution():
                try:
                    df['Race'].value_counts().plot(kind='pie', title="Patient Race", autopct='%1.1f%%')
                    plt.ylabel("")
                    plt.tight_layout()
                    plt.show()
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Race Distribution", status="Success")
                except Exception as e:
                    log_usage(self.username, self.role, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              action="Race Distribution", status="Failed")

            tk.Button(stat_win, text="Temporal Trends", command=show_temporal_trend).pack(pady=5)
            tk.Button(stat_win, text="Insurance Trends", command=show_insurance_distribution).pack(pady=5)
            tk.Button(stat_win, text="Race Demographics", command=show_race_distribution).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statistics: {str(e)}")

            


