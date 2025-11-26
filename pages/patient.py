import streamlit as st
from datetime import datetime
from db_utils import run_query

# st.title("Patient Portal – Clinic Demo")

# Initialize session state for workflow navigation
if "patient_view" not in st.session_state:
    st.session_state["patient_view"] = "home"

# --- HOME VIEW (Two Buttons) ---
if st.session_state["patient_view"] == "home":
    st.header("Welcome, Patient!")
    st.write("What would you like to do?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register as a Patient", use_container_width=True):
            st.session_state["patient_view"] = "register"
            st.rerun()
    with col2:
        if st.button("Create an Appointment", use_container_width=True):
            st.session_state["patient_view"] = "book"
            st.rerun()

# --- REGISTER VIEW ---
elif st.session_state["patient_view"] == "register":
    # Back button at the top
    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Registration")
    st.write("Please fill in your information below.")

    with st.form("register_form"):
        col1, col2 = st.columns(2)  # Equal 1:1 split

        with col1:
            fname = st.text_input("First Name *", placeholder="Enter your first name")
            dob = st.date_input(
                "Date of Birth*",
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2025, 12, 31),
                value=datetime(2000, 1, 1),
            )
            phone = st.text_input("Phone Number *", placeholder="e.g., 081234567890")
            address = st.text_area(
                "Address", height=100, placeholder="Your full address"
            )

        with col2:
            lname = st.text_input("Last Name *", placeholder="Enter your last name")
            gender = st.selectbox("Gender", ["Male", "Female", "Unknown"])
            email = st.text_input("Email", placeholder="example@email.com")

        submitted = st.form_submit_button(
            "Submit Registration", use_container_width=True
        )

    if submitted:
        if not fname or not lname or not dob or not phone:
            st.error(
                "❌ Please fill in all required fields: First Name, Last Name, Date of Birth and Phone Number."
            )
        else:
            gender_value = None if gender == "Unknown" else gender
            email_value = email if email else None
            address_value = address if address else None

            query = """
                INSERT INTO Patient (first_name, last_name, dob, gender, phone_number, email, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                fname,
                lname,
                dob,
                gender_value,
                phone,
                email_value,
                address_value,
            )

            try:
                run_query(query, params)
                st.success("Registration complete! Welcome to our clinic.")
                st.info("You can now book an appointment using your contact information.")
            except Exception as e:
                st.error(f"Registration failed: {e}")


# --- BOOK APPOINTMENT VIEW ---
elif st.session_state["patient_view"] == "book":
    # Back button at the top
    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Book an Appointment")

    patient_id = st.number_input("Enter your Patient ID", min_value=1, step=1)

    # Filter by specialization
    specs = run_query("SELECT * FROM Specialization", fetch=True)
    if specs:
        spec_choices = {
            row["specialization_name"]: row["specialization_id"] for row in specs
        }
        spec_selected = st.selectbox("Choose Specialization", list(spec_choices.keys()))
        spec_id = spec_choices[spec_selected]

        # Show available slots
        slots = run_query(
            """
            SELECT s.schedule_id, s.available_day, s.start_time, s.end_time, 
                   d.first_name, d.last_name
            FROM Schedule s
            JOIN Doctor d ON s.doctor_id = d.doctor_id
            WHERE s.is_booked = FALSE AND d.specialization_id = %s
            ORDER BY s.available_day, s.start_time
            """,
            (spec_id,),
            fetch=True,
        )

        if slots:
            slot_strs = [
                f"{row['available_day']} {row['start_time']}–{row['end_time']} (Dr. {row['first_name']} {row['last_name']})"
                for row in slots
            ]
            selected = st.selectbox("Pick an available slot", slot_strs)
            idx = slot_strs.index(selected)
            slot_row = slots[idx]

            reason = st.text_input("Reason for visit")

            if st.button("Book This Appointment"):
                # Create appointment (use real date calculation if needed)
                appointment_datetime = f"2025-12-01 {slot_row['start_time']}"
                run_query(
                    """
                    INSERT INTO Appointment (patient_id, schedule_id, reason_for_visit, appointment_datetime, status)
                    VALUES (%s, %s, %s, %s, 'scheduled')
                    """,
                    (patient_id, slot_row["schedule_id"], reason, appointment_datetime),
                )
                run_query(
                    "UPDATE Schedule SET is_booked = TRUE WHERE schedule_id = %s",
                    (slot_row["schedule_id"],),
                )
                st.success("✅ Your appointment is booked!")
        else:
            st.info("No available slots for this specialization.")
