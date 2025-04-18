import streamlit as st
import pandas as pd
import os
from data_loader import load_all_data, prepare_billing_summary
import plotly.express as px

def main():
    st.set_page_config(page_title="Hospital Billing Dashboard", layout="wide")
    st.title("🏥 Hospital Billing & Insurance Demo Dashboard")
    st.markdown("""
    This dashboard displays the billing summary for five patients, two doctors, and Medicaid insurance coverage.
    """)

    # Load data
    doctor_df, insurance_df, patient_df = load_all_data()
    summary = prepare_billing_summary(doctor_df, insurance_df, patient_df)

    # Sidebar filters
    st.sidebar.header("Filters")
    doctor_filter = st.sidebar.selectbox("Filter by Assigned Doctor", options=["All"] + list(summary["Assigned Doctor"].unique()))
    patient_filter = st.sidebar.selectbox("Filter by Patient", options=["All"] + list(summary["Patient Name"].unique()))

    filtered_summary = summary.copy()
    if doctor_filter != "All":
        filtered_summary = filtered_summary[filtered_summary["Assigned Doctor"] == doctor_filter]
    if patient_filter != "All":
        filtered_summary = filtered_summary[filtered_summary["Patient Name"] == patient_filter]

    # Show main summary table
    st.subheader("Billing Summary Table")
    st.dataframe(filtered_summary, use_container_width=True)

    # Show doctor charges table
    st.subheader("Doctor Charges Table")
    st.dataframe(doctor_df, use_container_width=True)

    # Show insurance rates table
    st.subheader("Insurance Rates Table (Medicaid)")
    st.dataframe(insurance_df, use_container_width=True)

    # Summary statistics
    st.markdown("---")
    st.subheader("Summary Statistics")
    total_billed = filtered_summary["Doctor Charge"].sum()
    total_covered = filtered_summary["Medicaid Rate"].sum()
    total_unpaid = filtered_summary["Patient Owes"].sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Billed", f"${total_billed:,.2f}")
    col2.metric("Total Covered (Insurance)", f"${total_covered:,.2f}")
    col3.metric("Total Unpaid (Patients)", f"${total_unpaid:,.2f}")

    # Bar chart: Patient vs. Amount Owed
    st.markdown("---")
    st.subheader("Patient Responsibility (Bar Chart)")
    fig = px.bar(filtered_summary, x="Patient Name", y="Patient Owes", color="Disease",
                 labels={"Patient Owes": "Amount Owed ($)"},
                 title="Patient Out-of-Pocket by Disease")
    st.plotly_chart(fig, use_container_width=True)

    # Pie chart: Distribution of Doctor Charges
    st.subheader("Doctor Charges Distribution (Pie Chart)")
    fig2 = px.pie(filtered_summary, names="Patient Name", values="Doctor Charge", title="Doctor Charges per Patient")
    st.plotly_chart(fig2, use_container_width=True)

    # Download CSV
    st.markdown("---")
    st.subheader("Download Billing Summary")
    csv = filtered_summary.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "billing_summary.csv", "text/csv")

if __name__ == "__main__":
    main()
