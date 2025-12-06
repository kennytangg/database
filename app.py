import streamlit as st

st.set_page_config(page_title="Clinic Appointment System", layout="wide")

st.title("Clinic Appointment System")

st.markdown("""
### Business Process Demo

Select a role from the sidebar to begin:
- **Patient** - Register, book, view, and cancel appointments
- **Doctor** - View today's schedule and complete appointments  
- **Admin** - Manage invoices, view schedules, and analytics
""")

st.divider()

st.info("Use the sidebar navigation to switch between roles")
