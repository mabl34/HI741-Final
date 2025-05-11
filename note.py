#!/usr/bin/env python
# coding: utf-8

# Defining note class using OOP design
# Multiple notes can be created by a single patient, there is one note per visit per patient


class Note:
    def __init__(self, note_id, patient_id, visit_id, note_type, content):
        self.note_id = note_id
        self.patient_id = patient_id
        self.visit_id = visit_id
        self.note_type = note_type
        self.content = content

