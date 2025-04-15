# 🏥 Hospital Insurance Billing System

## Overview

This project is a Python-based application designed by a team of 5 developers to automate billing in hospitals. It takes patient details, services received, and insurance information to calculate the final balance the patient owes after insurance deductions.

The system supports major insurance companies like **Medicaid** and **United Healthcare** and generates a final billing summary that includes a detailed breakdown of services, insurance coverage, and patient responsibilities.

---

## 🚀 Features

- Accepts patient info and service details (via CPT codes)
- Calculates total billed amount for hospital services
- Determines insurance-covered costs vs. patient responsibility
- Supports multiple insurance companies (Medicaid, UHC, etc.)
- Handles reason codes like `PR1` (Deductible) and `CO45` (Denied)
- Automatically generates a billing summary for the patient
- Option to email billing statements

---

## 📂 Project Structure

```
Insurance_project/
│
├── data/         # Input/output data files (Excel, CSV, DB, PDFs, etc.)
│├── diagnosis_codes.xlsx
│├── diagnosis_codes.db
│├── uhc_eob_data.csv
│├── uhc_eob_data.json
│├── diagnosistable.pdf
│└── uhc eob.pdf
│
├── scripts/      # Python scripts for extraction and processing
│├── extract_diagnosis_table.py
│└── extract_eob_data.py
│
├── .gitignore    # Ignores all data outputs and temp files
└── README.md     # Project instructions
```

---

## ⚙️ Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Insurance_project
   ```
2. **Install dependencies:**
   ```bash
   pip install pdfplumber pandas openpyxl
   # For scanned EOBs, also: pip install pytesseract Pillow
   ```

---

## 🛠️ Usage

1. **Extract Diagnosis Codes:**
   - Place your `diagnosistable.pdf` in `data/`.
   - Run:
     ```bash
     python scripts/extract_diagnosis_table.py
     ```
   - Outputs: `diagnosis_codes.xlsx` and `diagnosis_codes.db` in `data/`.

2. **Extract EOB Data:**
   - Place EOB PDFs (e.g., `uhc eob.pdf`) in `data/`.
   - Run:
     ```bash
     python scripts/extract_eob_data.py
     ```
   - Outputs: `uhc_eob_data.csv` and `uhc_eob_data.json` in `data/`.

---

## 🔄 Workflow Summary

1. Diagnosis codes organized → Search tool (Person 1)
2. EOB PDFs processed → Clean CSV/JSON (Person 2)
3. Payment vs. billed compared → Issues flagged (Person 3)
4. Multi-insurance claims managed → Coordinated results (Person 4)
5. Final insights → Dashboard + Reports (Person 5)

---

## 📦 Requirements
- Python 3.8+
- pdfplumber
- pandas
- openpyxl
- (Optional) pytesseract, Pillow (for scanned PDFs)

---

## 🤝 Contributing
- Scripts go in `scripts/`
- Data files go in `data/` (ignored by Git)
- Update `.gitignore` as needed for new temp/output files

---

## 📝 Notes
- Sensitive or large data files are kept out of version control via `.gitignore`.
- For automated billing emails, see future scripts or modules.
- For dashboard/reporting, see next development steps.

---

## 📧 Contact
For questions or contributions, please contact the project maintainers or open an issue.
