import streamlit as st

st.set_page_config(page_title="Clinic Appointment System", layout="wide")

st.title("Clinic Appointment System")

st.markdown(""" ## Demo
Select a role from the sidebar to begin:
- **Patient**: Register, book, view, and cancel appointments
- **Doctor**: View today schedule and complete appointments  
- **Admin**: Manage invoices, view schedules and analytics
""")
