# HI741-Final

## Project Overview

This project is a secure, role-based healthcare data system built with Python and Tkinter. It allows users such as nurses, clinicians, administrators, and management to:

- Add, retrieve, and remove patient records
- View and search patient notes
- Count patient visits by date
- Generate temporal and demographic statistics
- Log all usage activity (for audit and analysis)

The program features a **user-friendly graphical interface (GUI)** and tracks user actions to ensure transparency and accountability.

---

## How to Run the Program

### 1. Clone the GitHub Repository

```bash
git clone https://github.com/mabl34/HI741-Final.git
cd HI741-Final
```

### 2. Set Up the Environment

If you're using `pip`:

```bash
pip install -r requirements.txt
```

If you're using Anaconda:

```bash
conda create --name healthcare_env --file=requirements.txt
conda activate healthcare_env
```

### 3. Run the Program

```bash
python main.py
```

The GUI will launch and prompt you to log in using your credentials from `Credentials.csv`.

---

## Repository Structure

```
HI741-Final/
├── data/                     # Folder for input and output files
│   ├── Credentials.csv
│   ├── Patient_data.csv
│   ├── Notes.csv
│   ├── usage_log.csv         # Automatically created
├── src/                      # Python source code
│   ├── main.py
│   ├── ui.py
│   ├── user.py
│   ├── visit.py
│   ├── patient.py
│   ├── logger.py
│   ├── data_handler.py
│   └── ...
├── UML.pdf                   # UML diagram
├── requirements.txt
└── README.md
```

---

## Features by User Role

| Role        | Features                                                                 |
|-------------|--------------------------------------------------------------------------|
| Nurse       | Add/Remove/Retrieve patients, Count visits, View notes                  |
| Clinician   | Same as Nurse                                                            |
| Admin       | Count visits by date                                                     |
| Management  | Generate statistical plots and trends                                    |

---

## Output Files

- `Patient_data.csv`: Automatically updated with patient visit additions or deletions.
- `usage_log.csv`: Tracks all user logins, actions, timestamps, and login outcomes.

---

## Requirements

The main packages are:

```
matplotlib
pandas
```

Standard Python libraries used:
- `tkinter`
- `csv`
- `datetime`
- `os`

---

## Version Control & Collaboration

- GitHub repo: [Your Repo URL Here](https://github.com/yourusername/HI741-Final)
- Includes commit history, project structure, and source code.
- Shows active development and usage of version control tools.

---

## Notes

- Make sure your credential and patient data CSVs are in the correct format.
- All login attempts (successful and failed) are logged.
- You can extend the program by adding additional roles or features.

---

## UML Diagram

See `UML.pdf` in the project root for a visual representation of the class structure.

---

## Developed By

Michaela Braun  
HI 741 – Spring 2025 Final Project
