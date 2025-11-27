import streamlit as st
from datetime import datetime
from db_utils import run_query

# st.title("Patient Portal – Clinic Demo")

if "patient_view" not in st.session_state:
    st.session_state["patient_view"] = "home"

# --- HOME VIEW ---
if st.session_state["patient_view"] == "home":
    st.header("Welcome!")
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
    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Registration")
    st.write("Please fill in your information below.")

    with st.form(
        "register_form", clear_on_submit=True
    ):  
        col1, col2 = st.columns(2)

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
            gender = st.selectbox(
                "Gender", ["Select gender", "Male", "Female", "Unknown"]
            )
            email = st.text_input("Email", placeholder="example@email.com")

        submitted = st.form_submit_button(
            "Submit Registration", use_container_width=True
        )

    if submitted:
        if not fname or not lname or not dob or not phone:
            st.error(
                "Please fill in all required fields: First Name, Last Name, Date of Birth and Phone Number."
            )
        else:
            gender_value = None if gender in ["Select gender", "Unknown"] else gender
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
                st.balloons()
            except Exception as e:
                st.error(f"Registration failed: {e}")

# --- BOOK APPOINTMENT VIEW ---
elif st.session_state["patient_view"] == "book":
    # Initialize sub-state for booking flow
    if "selected_patient_id" not in st.session_state:
        st.session_state["selected_patient_id"] = None
    if "search_results" not in st.session_state:
        st.session_state["search_results"] = None
    if "search_performed" not in st.session_state:
        st.session_state["search_performed"] = False

    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.session_state["selected_patient_id"] = None
        st.session_state["search_results"] = None
        st.session_state["search_performed"] = False
        st.rerun()

    st.subheader("Book an Appointment")

    if st.session_state["selected_patient_id"] is None:
        st.write("Find your record by date of birth.")

        dob_search = st.date_input(
            "Date of Birth",
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2025, 12, 31),
            value=datetime(2000, 1, 1),
        )

        if st.button("Search Patients", use_container_width=True):
            patients = run_query(
                """
                SELECT patient_id, first_name, last_name, phone_number, email
                FROM Patient
                WHERE dob = %s
                ORDER BY first_name, last_name
                """,
                (dob_search,),
                fetch=True,
            )
            st.session_state["search_results"] = patients
            st.session_state["search_performed"] = True
            st.rerun()

        # Show results only if search was performed
        if st.session_state["search_performed"]:
            patients = st.session_state["search_results"]
            if patients:
                st.success(f"Found {len(patients)} patient(s).")
                for p in patients:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{p['first_name']} {p['last_name']}**")
                            st.caption(
                                f"Phone: {p['phone_number']} | Email: {p['email'] or 'Not provided'}"
                            )
                        with col2:
                            if st.button(
                                "Select",
                                key=f"select_{p['patient_id']}",
                                use_container_width=True,
                            ):
                                st.session_state["selected_patient_id"] = p["patient_id"]
                                st.session_state["selected_patient_name"] = (
                                    f"{p['first_name']} {p['last_name']}"
                                )
                                # Clear search state
                                st.session_state["search_results"] = None
                                st.session_state["search_performed"] = False
                                st.rerun()
                        st.divider()
            else:
                st.warning("No patients found with this date of birth.")


    else:
        st.write("Choose a doctor and available time.")

        specs = run_query("SELECT * FROM Specialization", fetch=True)
        if not specs:
            st.error("No specializations found in the system.")
        else:
            spec_choices = {
                row["specialization_name"]: row["specialization_id"] for row in specs
            }
            spec_selected = st.selectbox(
                "Choose Specialization", list(spec_choices.keys())
            )
            spec_id = spec_choices[spec_selected]

            # Choose doctor
            doctors = run_query(
                """
                SELECT doctor_id, first_name, last_name
                FROM Doctor
                WHERE specialization_id = %s
                ORDER BY first_name, last_name
                """,
                (spec_id,),
                fetch=True,
            )

            if not doctors:
                st.warning("No doctors available for this specialization.")
            else:
                doctor_labels = [
                    f"Dr. {d['first_name']} {d['last_name']}" for d in doctors
                ]
                doctor_selected = st.selectbox(
                    "Choose Doctor", doctor_labels, key="doctor_select"
                )
                doc_idx = doctor_labels.index(doctor_selected)
                selected_doctor = doctors[doc_idx]

                # Available slots for this doctor
                slots = run_query(
                    """
                    SELECT schedule_id, available_day, start_time, end_time
                    FROM Schedule
                    WHERE doctor_id = %s AND is_booked = FALSE
                    ORDER BY available_day, start_time
                    """,
                    (selected_doctor["doctor_id"],),
                    fetch=True,
                )

                if not slots:
                    st.info("No available time slots for this doctor.")
                else:
                    slot_labels = [
                        f"{row['available_day']} {row['start_time']}–{row['end_time']}"
                        for row in slots
                    ]
                    slot_selected = st.selectbox(
                        "Choose Available Time Slot", slot_labels, key="slot_select"
                    )
                    s_idx = slot_labels.index(slot_selected)
                    selected_slot = slots[s_idx]

                    reason = st.text_input("Reason for visit")

                    if st.button("Confirm Appointment", use_container_width=True):
                        appointment_datetime = (
                            f"2025-12-01 {selected_slot['start_time']}"
                        )
                        
                        try:
                            # Insert appointment
                            run_query(
                                """
                                INSERT INTO Appointment (patient_id, schedule_id, reason_for_visit, appointment_datetime, status)
                                VALUES (%s, %s, %s, %s, 'scheduled')
                                """,
                                (
                                    st.session_state["selected_patient_id"],
                                    selected_slot["schedule_id"],
                                    reason,
                                    appointment_datetime,
                                ),
                            )
                            # Mark schedule as booked
                            run_query(
                                "UPDATE Schedule SET is_booked = TRUE WHERE schedule_id = %s",
                                (selected_slot["schedule_id"],),
                            )
                            
                            st.success("Appointment Successfully Booked!")
                            st.balloons()
                            
                            # Show appointment summary
                            st.info(
                                f"**Appointment Details:**\n\n"
                                f"Patient: {st.session_state['selected_patient_name']}\n\n"
                                f"️Doctor: {doctor_selected}\n\n"
                                f"Date & Time: {selected_slot['available_day']} at {selected_slot['start_time']}\n\n"
                                f"Reason: {reason or '-'}\n\n"
                                f"Please arrive 15 minutes before your appointment time."
                            )
                            
                            st.session_state["selected_patient_id"] = None
                            st.session_state["search_results"] = []
                            
                        except Exception as e:
                            st.error(f"Appointment booking failed: {e}")
