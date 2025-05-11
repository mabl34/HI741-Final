#!/usr/bin/env python
# coding: utf-8

# Defining department class using OOP design
# Patients can visit multiple departments
# Defined two functions to add patient and return patient values


class Department:
    def __init__(self, name):
        self.name = name
        self.patients = {}

    def add_patient(self, patient):
        # Adds a patient to the department
        self.patients[patient.patient_id] = patient

    def get_patients(self):
        # Returns all patients in the department
        return self.patients.values()

