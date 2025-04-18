import os
import pandas as pd
from docx import Document

def docx_table_to_df(docx_path):
    doc = Document(docx_path)
    table = doc.tables[0]
    data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def load_all_data():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    doctor_df = docx_table_to_df(os.path.join(data_dir, 'Doctor_Charges.docx'))
    insurance_df = docx_table_to_df(os.path.join(data_dir, 'Medicaid_Insurance_Rates.docx'))
    patient_df = docx_table_to_df(os.path.join(data_dir, 'Patient_Disease_Assignments.docx'))
    return doctor_df, insurance_df, patient_df

def prepare_billing_summary(doctor_df, insurance_df, patient_df):
    # Assign doctors to patients (alternating: A, B, ...)
    doctors = ['A', 'B'] * 3
    patient_df['Assigned Doctor'] = [doctors[i] for i in range(len(patient_df))]

    # Merge patient with disease info
    merged = pd.merge(patient_df, doctor_df, left_on=['Disease', 'ICD Code'], right_on=['Disease Name', 'ICD Code'])
    merged = pd.merge(merged, insurance_df, on=['Disease Name', 'ICD Code'])

    # Calculate charges and patient responsibility
    def get_doctor_charge(row):
        return float(row['Doctor A Rate ($)']) if row['Assigned Doctor'] == 'A' else float(row['Doctor B Rate ($)'])
    merged['Doctor Charge'] = merged.apply(get_doctor_charge, axis=1)
    merged['Medicaid Rate'] = merged['Medicaid Rate ($)'].astype(float)
    merged['Patient Owes'] = merged['Doctor Charge'] - merged['Medicaid Rate']

    summary_cols = [
        'Patient Name', 'Patient ID', 'Disease', 'ICD Code', 'Assigned Doctor',
        'Doctor Charge', 'Medicaid Rate', 'Patient Owes'
    ]
    summary = merged[summary_cols]
    return summary

if __name__ == "__main__":
    # For quick testing
    doctor_df, insurance_df, patient_df = load_all_data()
    summary = prepare_billing_summary(doctor_df, insurance_df, patient_df)
    print(summary)
