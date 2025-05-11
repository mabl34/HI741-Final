#!/usr/bin/env python
# coding: utf-8

# auth.py

def load_users(filepath):
    user_data = {}
    with open(filepath, 'r') as f:
        next(f)  # skip header
        for line in f:
            username, password, role = line.strip().split(',')
            user_data[username] = (password, role)
    return user_data

def create_user(username, password, user_data):
    if username in user_data and user_data[username][0] == password:
        role = user_data[username][1]
        if role == "nurse":
            return Nurse(username, role)
        elif role == "clinician":
            return Clinician(username, role)
        elif role == "admin":
            return Admin(username, role)
        elif role == "management":
            return Management(username, role)
    return None
