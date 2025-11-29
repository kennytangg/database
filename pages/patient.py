import streamlit as st
from datetime import datetime
from db_utils import run_query
from collections import defaultdict


def initialize_session_state():
    """Initialize patient view session state"""
    if "patient_view" not in st.session_state:
        st.session_state["patient_view"] = "home"
    if "logged_in_patient_id" not in st.session_state:
        st.session_state["logged_in_patient_id"] = None
    if "logged_in_patient_name" not in st.session_state:
        st.session_state["logged_in_patient_name"] = None
    if "search_results" not in st.session_state:
        st.session_state["search_results"] = None
    if "search_performed" not in st.session_state:
        st.session_state["search_performed"] = False


def logout():
    """Clear patient login session"""
    st.session_state["logged_in_patient_id"] = None
    st.session_state["logged_in_patient_name"] = None
    st.session_state["patient_view"] = "home"
    st.session_state["search_results"] = None
    st.session_state["search_performed"] = False


def back_to_dashboard_button():
    """Navigate back to patient dashboard"""
    if st.button("Back to Dashboard"):
        st.session_state["patient_view"] = "dashboard"
        st.rerun()


def render_home_view():
    """Home view with Register or Login options"""
    st.header("Welcome to the Clinic!")
    st.write("Please choose an option below:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register as a Patient", use_container_width=True):
            st.session_state["patient_view"] = "register"
            st.rerun()
    with col2:
        if st.button("Login as a Patient", use_container_width=True):
            st.session_state["patient_view"] = "login"
            st.rerun()


def render_registration_form():
    """Render patient registration form"""
    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Registration")
    st.write("Please fill in your information below.")

    with st.form("register_form", clear_on_submit=True):
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
        handle_registration_submission(fname, lname, dob, phone, gender, email, address)


def handle_registration_submission(fname, lname, dob, phone, gender, email, address):
    """Handle patient registration form submission"""
    if not fname or not lname or not dob or not phone:
        st.error(
            "Please fill in all required fields: First Name, Last Name, Date of Birth and Phone Number."
        )
        return

    gender_value = None if gender in ["Select gender", "Unknown"] else gender
    email_value = email if email else None
    address_value = address if address else None

    query = """
        INSERT INTO Patient (first_name, last_name, dob, gender, phone_number, email, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (fname, lname, dob, gender_value, phone, email_value, address_value)

    try:
        run_query(query, params)
        st.success("Registration complete! Welcome to our clinic.")
        st.balloons()
        st.info("You can now login using your date of birth.")
    except Exception as e:
        st.error(f"Registration failed: {e}")


def render_login_view():
    """Login view - patient search by DOB"""
    if st.button("Back to Home"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Login")
    st.write("Find your account by entering your date of birth.")

    dob_search = st.date_input(
        "Date of Birth",
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2025, 12, 31),
        value=datetime(2000, 1, 1),
    )

    if st.button("Search", use_container_width=True):
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

    if st.session_state["search_performed"]:
        display_login_results()


def display_login_results():
    """Display patient search results for login"""
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
                        "Login",
                        key=f"login_{p['patient_id']}",
                        use_container_width=True,
                    ):
                        # Set logged in patient
                        st.session_state["logged_in_patient_id"] = p["patient_id"]
                        st.session_state["logged_in_patient_name"] = (
                            f"{p['first_name']} {p['last_name']}"
                        )
                        st.session_state["search_results"] = None
                        st.session_state["search_performed"] = False
                        st.session_state["patient_view"] = "dashboard"
                        st.rerun()
                st.divider()
    else:
        st.warning("No patients found with this date of birth.")


def render_patient_dashboard():
    """Patient dashboard after login"""
    patient_name = st.session_state["logged_in_patient_name"]

    st.header(f"Welcome, {patient_name}!")
    st.write("What would you like to do today?")

    # Logout button in sidebar or top
    if st.button("Logout", type="primary"):
        logout()
        st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Book an Appointment", use_container_width=True):
            st.session_state["patient_view"] = "book"
            st.rerun()
    with col2:
        if st.button("View My Appointments", use_container_width=True):
            st.session_state["patient_view"] = "view"
            st.rerun()
    with col3:
        if st.button("Cancel an Appointment", use_container_width=True):
            st.session_state["patient_view"] = "cancel"
            st.rerun()


def render_booking_view():
    """Render appointment booking - no patient search needed"""
    back_to_dashboard_button()
    st.subheader("Book an Appointment")

    render_appointment_booking()


def render_appointment_booking():
    """Render appointment booking interface for logged-in patient."""
    st.write("Choose a doctor and available time.")

    specs = run_query("SELECT * FROM Specialization", fetch=True)
    if not specs:
        st.error("No specializations found in the system.")
        return

    spec_choices = {
        row["specialization_name"]: row["specialization_id"] for row in specs
    }
    spec_selected = st.selectbox("Choose Specialization", list(spec_choices.keys()))
    spec_id = spec_choices[spec_selected]

    doctors = get_doctors_by_specialization(spec_id)
    if not doctors:
        st.warning("No doctors available for this specialization.")
        return

    selected_doctor = select_doctor(doctors)
    slots = get_available_slots(selected_doctor["doctor_id"])

    if not slots:
        st.info("No available time slots for this doctor.")
        return

    selected_slot = select_time_slot(slots)
    reason = st.text_input("Reason for visit")

    if st.button("Confirm Appointment", use_container_width=True):
        handle_appointment_confirmation(selected_slot, reason)


def render_view_appointments():
    """View all appointments for logged in patient"""
    back_to_dashboard_button()

    patient_id = st.session_state["logged_in_patient_id"]
    patient_name = st.session_state["logged_in_patient_name"]

    st.subheader("My Appointments")
    st.write(f"All appointments for **{patient_name}**")

    # Query all appointments with details
    appointments = run_query(
        """
        SELECT 
            a.appointment_id,
            a.appointment_datetime,
            a.status,
            a.reason_for_visit,
            s.available_day,
            s.start_time,
            s.end_time,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            sp.specialization_name
        FROM Appointment a
        JOIN Schedule s ON a.schedule_id = s.schedule_id
        JOIN Doctor d ON s.doctor_id = d.doctor_id
        JOIN Specialization sp ON d.specialization_id = sp.specialization_id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_datetime DESC
        """,
        (patient_id,),
        fetch=True,
    )

    if not appointments:
        st.info("You don't have any appointments yet.")
        if st.button(" Book Your First Appointment", use_container_width=True):
            st.session_state["patient_view"] = "book"
            st.rerun()
        return

    # Display appointments grouped by status
    display_appointments_by_status(appointments)


def display_appointments_by_status(appointments):
    """Display appointments organized by status with color coding"""

    # Status color mapping
    status_colors = {
        "scheduled": "🟢",
        "completed": "🔵",
        "cancelled": "🔴",
        "missed": "🟠",
    }

    grouped = defaultdict(list)
    for appt in appointments:
        grouped[appt["status"]].append(appt)

    # Show scheduled first, then others
    status_order = ["scheduled", "completed", "cancelled", "missed"]

    for status in status_order:
        if status not in grouped:
            continue

        appts = grouped[status]
        status_icon = status_colors.get(status, "⚪")

        with st.expander(
            f"{status_icon} {status.title()} ({len(appts)})",
            expanded=(status == "scheduled"),
        ):
            for appt in appts:
                render_appointment_card(appt)


def render_appointment_card(appt):
    """Render a single appointment card"""
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"### {appt['available_day']} at {appt['start_time']}–{appt['end_time']}"
            )
            st.write(
                f"**Doctor:** Dr. {appt['doctor_first_name']} {appt['doctor_last_name']}"
            )
            st.write(f"**Specialization:** {appt['specialization_name']}")
            st.write(f"**Reason:** {appt['reason_for_visit'] or 'Not specified'}")
            st.caption(f"Appointment Date: {appt['appointment_datetime']}")

        with col2:
            # Status badge
            status = appt["status"]
            if status == "scheduled":
                st.success("Scheduled")
            elif status == "completed":
                st.info("Completed")
            elif status == "cancelled":
                st.error("Cancelled")
            elif status == "missed":
                st.warning("Missed")

        st.divider()


def get_doctors_by_specialization(spec_id):
    """Fetch doctors for a given specialization."""
    return run_query(
        """
        SELECT doctor_id, first_name, last_name
        FROM Doctor
        WHERE specialization_id = %s
        ORDER BY first_name, last_name
        """,
        (spec_id,),
        fetch=True,
    )


def select_doctor(doctors):
    """Render doctor selection dropdown and return selected doctor."""
    doctor_labels = [f"Dr. {d['first_name']} {d['last_name']}" for d in doctors]
    doctor_selected = st.selectbox("Choose Doctor", doctor_labels, key="doctor_select")
    doc_idx = doctor_labels.index(doctor_selected)
    return doctors[doc_idx]


def get_available_slots(doctor_id):
    """Fetch available time slots for a doctor."""
    return run_query(
        """
        SELECT schedule_id, available_day, start_time, end_time
        FROM Schedule
        WHERE doctor_id = %s AND is_booked = FALSE
        ORDER BY available_day, start_time
        """,
        (doctor_id,),
        fetch=True,
    )


def select_time_slot(slots):
    """Render time slot selection dropdown and return selected slot."""
    slot_labels = [
        f"{row['available_day']} {row['start_time']}–{row['end_time']}" for row in slots
    ]
    slot_selected = st.selectbox(
        "Choose Available Time Slot", slot_labels, key="slot_select"
    )
    s_idx = slot_labels.index(slot_selected)
    return slots[s_idx]


def handle_appointment_confirmation(selected_slot, reason):
    """Handle appointment confirmation and database updates."""
    appointment_datetime = f"2025-12-01 {selected_slot['start_time']}"

    try:
        # Insert appointment
        run_query(
            """
            INSERT INTO Appointment (patient_id, schedule_id, reason_for_visit, appointment_datetime, status)
            VALUES (%s, %s, %s, %s, 'scheduled')
            """,
            (
                st.session_state["logged_in_patient_id"],
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

        display_appointment_summary(selected_slot, reason)

    except Exception as e:
        st.error(f"Appointment booking failed: {e}")


def display_appointment_summary(selected_slot, reason):
    """Display appointment confirmation summary."""
    st.info(
        f"**Appointment Details:**\n\n"
        f"Patient: {st.session_state['logged_in_patient_name']}\n\n"
        f"Date & Time: {selected_slot['available_day']} at {selected_slot['start_time']}\n\n"
        f"Reason: {reason or '-'}\n\n"
        f"Please arrive 15 minutes before your appointment time."
    )


def render_cancel_view():
    """Cancel an existing appointment"""
    back_to_dashboard_button()
    st.subheader("Cancel an Appointment")

    render_patient_appointments_for_cancel()


def render_patient_appointments_for_cancel():
    """Show logged-in patient's upcoming/scheduled appointments and allow cancel."""
    patient_id = st.session_state["logged_in_patient_id"]
    patient_name = st.session_state["logged_in_patient_name"]

    st.markdown(f"### Your Scheduled Appointments")

    appointments = run_query(
        """
        SELECT 
            a.appointment_id,
            a.appointment_datetime,
            a.status,
            a.schedule_id,
            a.reason_for_visit,
            s.available_day,
            s.start_time,
            s.end_time,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name
        FROM Appointment a
        JOIN Schedule s ON a.schedule_id = s.schedule_id
        JOIN Doctor d ON s.doctor_id = d.doctor_id
        WHERE a.patient_id = %s
          AND a.status = 'scheduled'
        ORDER BY a.appointment_datetime
        """,
        (patient_id,),
        fetch=True,
    )

    if not appointments:
        st.info("You have no scheduled appointments to cancel.")
        return

    for appt in appointments:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(
                    f"**{appt['available_day']} at {appt['start_time']}–{appt['end_time']}**"
                )
                st.caption(
                    f"Doctor: Dr. {appt['doctor_first_name']} {appt['doctor_last_name']}"
                )
                st.caption(f"Reason: {appt['reason_for_visit'] or 'Not specified'}")
            with col2:
                if st.button(
                    "Cancel",
                    key=f"cancel_{appt['appointment_id']}",
                    use_container_width=True,
                    type="primary",
                ):
                    handle_cancel_appointment(appt)
            st.divider()


def handle_cancel_appointment(appt_row):
    """Apply cancellation logic and update DB."""
    appt_id = appt_row["appointment_id"]
    schedule_id = appt_row["schedule_id"]

    try:
        # Mark appointment as cancelled
        run_query(
            "UPDATE Appointment SET status = 'cancelled' WHERE appointment_id = %s",
            (appt_id,),
        )

        # Free the schedule slot
        run_query(
            "UPDATE Schedule SET is_booked = FALSE WHERE schedule_id = %s",
            (schedule_id,),
        )

        st.success("Appointment successfully cancelled. The slot is now available.")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to cancel appointment: {e}")


def main():
    """Main routing function"""
    initialize_session_state()

    # If user is logged in, show dashboard-based views
    if st.session_state["logged_in_patient_id"] is not None:
        match st.session_state["patient_view"]:
            case "dashboard":
                render_patient_dashboard()
            case "book":
                render_booking_view()
            case "view":
                render_view_appointments()
            case "cancel":
                render_cancel_view()
            case "update":
                render_cancel_view()
            case _:
                render_patient_dashboard()
    else:
        # Not logged in - show public views
        match st.session_state["patient_view"]:
            case "home":
                render_home_view()
            case "register":
                render_registration_form()
            case "login":
                render_login_view()
            case _:
                render_home_view()


if __name__ == "__main__":
    main()
