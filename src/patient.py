#!/usr/bin/env python
# coding: utf-8


# Building upon previous coding: class design

# Defining patient class using OOP design
# Individual patients can have unique id, demographic information, zip code and insurance
# Much of this information is retained across visits by patient 
# (sometimes age, zip code, or insurance could change between visits)
# Patient visits can be added to patient's record and patient information can be stored by visit
# Defined two functions to add visit and return visit

class Patient:
    def __init__(self, patient_id, race, gender, ethnicity, zip_code, insurance):
        self.patient_id = patient_id
        self.race = race
        self.gender = gender
        self.ethnicity = ethnicity
        self.zip_code = zip_code
        self.insurance = insurance
        self.visits = []
        
    def __str__(self):
        visit_details = "\n  ".join([str(visit) for visit in self.visits])
        return (f"Patient ID: {self.patient_id}\n"
                f"Race: {self.race}, Gender: {self.gender}, Ethnicity: {self.ethnicity}\n"
                f"Zip Code: {self.zip_code}, Insurance: {self.insurance}\n"
                f"Visits:\n  {visit_details if visit_details else 'No visits recorded'}")
                

    def __repr__(self):  # Ensures that lists of patients display properly
        return self.__str__()

    def add_visit(self, visit):
        # Adds a visit to the patient's record
        self.visits.append(visit)

    def get_visits(self):
        # Returns all visits for this patient
        return self.visits

