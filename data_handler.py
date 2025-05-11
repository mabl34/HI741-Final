#!/usr/bin/env python
# coding: utf-8

# Access data and class definitions
# Define function which loads patient data and returns patients

import csv
from patient import Patient
from visit import Visit


def load_patient_data(data_file):
    patients = {}

    with open(data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                # Handle the Patient Information
                patient_id = int(row["Patient_ID"])

                # If this is the first time encountering this patient_id, create a Patient object
                if patient_id not in patients:
                    patients[patient_id] = Patient(
                        patient_id=patient_id,
                        race=row["Race"],
                        gender=row["Gender"],
                        ethnicity=row["Ethnicity"],
                        zip_code=row["Zip_code"],
                        insurance=row["Insurance"]
                    )

                # Handle the Visit Information
                try:
                    visit_id = int(row["Visit_ID"])
                except ValueError:
                    print(f"Warning: Invalid Visit_ID '{row['Visit_ID']}' for Patient {patient_id}. Skipping this visit.")
                    continue

                visit = Visit(
                    visit_id=visit_id,
                    patient_id=patient_id,
                    age=row["Age"],
                    visit_time=row["Visit_time"],
                    visit_department=row["Visit_department"],
                    chief_complaint=row.get("Chief_complaint", ""),
                    note_id=row.get("Note_ID", ""),
                    note_type=row.get("Note_type", "")
                )

                patients[patient_id].add_visit(visit)

            except KeyError as e:
                print(f"Error: Missing column {e} in the data row. Skipping row.")
                continue
            except ValueError:
                print(f"Error: Invalid Patient_ID value '{row['Patient_ID']}'. Skipping row.")
                continue

    return patients


def save_visit_to_csv(file_name, new_visit):
    with open(file_name, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            new_visit.visit_id,
            new_visit.patient_id,
            new_visit.visit_time,
            new_visit.visit_department,
            new_visit.chief_complaint,
            new_visit.note_id,
            new_visit.note_type,
            new_visit.age
        ])

