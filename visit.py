#!/usr/bin/env python
# coding: utf-8

# Define visit class
# There can be several visits per patients with unique times, notes, and departments
# Define how visit information will be printed


class Visit:
    def __init__(self, visit_id, patient_id, visit_time, visit_department, chief_complaint, note_id, note_type, age):
        self.visit_id = visit_id
        self.patient_id = patient_id
        self.visit_time = visit_time
        self.visit_department = visit_department
        self.chief_complaint = chief_complaint
        self.note_id = note_id
        self.note_type = note_type
        self.age = age  # Store the age for this specific visit

    def __str__(self):
        return (f"Visit ID: {self.visit_id}, Time: {self.visit_time}, Age: {self.age}, "
                    f" Department: {self.visit_department}, Chief Complaint: {self.chief_complaint}, "
                    f"Note ID: {self.note_id}, Note Type: {self.note_type}")
    def __repr__(self):  # Ensures that lists of visits are also displayed properly
        return self.__str__()