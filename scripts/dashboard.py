import streamlit as st
import pandas as pd
import os
from data_loader import load_default_data, prepare_billing_summary
import plotly.express as px

def main():
    st.set_page_config(page_title="Hospital Billing Dashboard", layout="wide")
    st.title("🏥 Hospital Billing & Insurance Demo Dashboard")
    st.markdown("""
    This dashboard displays the billing summary for all patients, doctors, and insurance companies. You can upload new data, add new patients, and visualize billing results.
    """)

    # --- Sidebar: Data Uploaders ---
    st.sidebar.header("Upload Data Files (.docx or .csv)")
    docx_types = [".docx", ".csv"]
    doctor_file = st.sidebar.file_uploader("Doctor Charges", type=["docx", "csv"])
    insurance_file = st.sidebar.file_uploader("Insurance Rates", type=["docx", "csv"])
    patient_file = st.sidebar.file_uploader("Patient Assignments", type=["docx", "csv"])

    # --- Load Data ---
    from data_loader import docx_table_to_df, csv_to_df
    def load_df(uploaded_file, default_path):
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                return csv_to_df(uploaded_file)
            else:
                return docx_table_to_df(uploaded_file)
        else:
            return docx_table_to_df(default_path) if default_path.endswith(".docx") else csv_to_df(default_path)
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    doctor_df = load_df(doctor_file, os.path.join(data_dir, 'Doctor_Charges.docx'))
    insurance_df = load_df(insurance_file, os.path.join(data_dir, 'Medicaid_Insurance_Rates.docx'))
    patient_df = load_df(patient_file, os.path.join(data_dir, 'Patient_Disease_Assignments.docx'))

    # --- Sidebar: Add New Patient Form ---
    st.sidebar.header("Simulate New Patient")
    with st.sidebar.form("add_patient_form"):
        new_patient_name = st.text_input("Patient Name")
        new_patient_id = st.text_input("Patient ID")
        disease_options = doctor_df['Disease Name'].unique().tolist()
        new_disease = st.selectbox("Disease", disease_options)
        icd_code = doctor_df[doctor_df['Disease Name'] == new_disease]['ICD Code'].iloc[0]
        doctor_options = ['A', 'B']
        assigned_doctor = st.selectbox("Assigned Doctor", doctor_options)
        # Insurance companies from insurance_df
        insurance_options = insurance_df['Insurance Company'].unique().tolist() if 'Insurance Company' in insurance_df.columns else ['Medicaid']
        insurance_company = st.selectbox("Insurance Company", insurance_options)
        add_patient = st.form_submit_button("Add Patient")

    # Add new patient if form submitted
    if add_patient and new_patient_name and new_patient_id:
        new_row = {
            'Patient Name': new_patient_name,
            'Patient ID': new_patient_id,
            'Disease': new_disease,
            'ICD Code': icd_code,
            'Assigned Doctor': assigned_doctor,
            'Insurance Company': insurance_company
        }
        patient_df = pd.concat([patient_df, pd.DataFrame([new_row])], ignore_index=True)
        st.sidebar.success(f"Added patient: {new_patient_name}")

    # --- Prepare Billing Summary ---
    summary = prepare_billing_summary(doctor_df, insurance_df, patient_df)

    # --- Sidebar: Filters ---
    st.sidebar.header("Filters")
    # Ensure all filter columns are strings and fillna
    summary["Assigned Doctor"] = summary["Assigned Doctor"].fillna("").astype(str)
    summary["Patient Name"] = summary["Patient Name"].fillna("").astype(str)
    summary["Insurance Company"] = summary["Insurance Company"].fillna("").astype(str)
    doctor_filter = st.sidebar.selectbox("Filter by Assigned Doctor", options=["All"] + sorted(summary["Assigned Doctor"].unique()))
    patient_filter = st.sidebar.selectbox("Filter by Patient", options=["All"] + sorted(summary["Patient Name"].unique()))
    insurance_filter = st.sidebar.selectbox("Filter by Insurance Company", options=["All"] + sorted(summary["Insurance Company"].unique()))

    filtered_summary = summary.copy()
    if doctor_filter != "All":
        filtered_summary = filtered_summary[filtered_summary["Assigned Doctor"] == doctor_filter]
    if patient_filter != "All":
        filtered_summary = filtered_summary[filtered_summary["Patient Name"] == patient_filter]
    if insurance_filter != "All":
        filtered_summary = filtered_summary[filtered_summary["Insurance Company"] == insurance_filter]

    # --- Main Tables ---
    st.subheader("Billing Summary Table")
    st.dataframe(filtered_summary, use_container_width=True)

    st.subheader("Doctor Charges Table")
    st.dataframe(doctor_df, use_container_width=True)

    st.subheader("Insurance Rates Table")
    st.dataframe(insurance_df, use_container_width=True)

    # --- Summary statistics ---
    st.markdown("---")
    st.subheader("Summary Statistics")
    total_billed = filtered_summary["Doctor Charge"].sum()
    total_covered = filtered_summary["Insurance Rate"].sum()
    total_unpaid = filtered_summary["Patient Owes"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Billed", f"${total_billed:,.2f}")
    col2.metric("Total Covered (Insurance)", f"${total_covered:,.2f}")
    col3.metric("Total Unpaid (Patients)", f"${total_unpaid:,.2f}")

    # --- Bar chart: Patient vs. Amount Owed ---
    st.markdown("---")
    st.subheader("Patient Responsibility (Bar Chart)")
    import plotly.express as px
    fig = px.bar(filtered_summary, x="Patient Name", y="Patient Owes", color="Disease",
                 labels={"Patient Owes": "Amount Owed ($)"},
                 title="Patient Out-of-Pocket by Disease")
    st.plotly_chart(fig, use_container_width=True)

    # --- Pie chart: Distribution of Doctor Charges ---
    st.subheader("Doctor Charges Distribution (Pie Chart)")
    fig2 = px.pie(filtered_summary, names="Patient Name", values="Doctor Charge", title="Doctor Charges per Patient")
    st.plotly_chart(fig2, use_container_width=True)

    # --- Download CSV ---
    st.markdown("---")
    st.subheader("Download Billing Summary")
    csv = filtered_summary.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "billing_summary.csv", "text/csv")

if __name__ == "__main__":
    main()
