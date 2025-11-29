import streamlit as st
from datetime import datetime
from db_utils import run_query
from collections import defaultdict


# Session state helpers
def init_state():
    """Initialize all session state variables"""
    defaults = {
        "patient_view": "home",
        "logged_in_patient_id": None,
        "logged_in_patient_name": None,
        "search_results": None,
        "search_performed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    """Clear patient session"""
    st.session_state.update(
        {
            "logged_in_patient_id": None,
            "logged_in_patient_name": None,
            "patient_view": "home",
            "search_results": None,
            "search_performed": False,
        }
    )


def nav_button(label, view):
    """Reusable navigation button"""
    if st.button(label, use_container_width=True):
        st.session_state["patient_view"] = view
        st.rerun()


# Public views
def render_home_view():
    st.header("Welcome to the Clinic!")
    col1, col2 = st.columns(2)
    with col1:
        nav_button("Register as a Patient", "register")
    with col2:
        nav_button("Login as a Patient", "login")


def render_registration_form():
    if st.button("← Back"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Registration")

    with st.form("register_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name *")
            dob = st.date_input("Date of Birth *", datetime(2000, 1, 1))
            phone = st.text_input("Phone Number *")
            address = st.text_area("Address")
        with col2:
            lname = st.text_input("Last Name *")
            gender = st.selectbox("Gender *", ["Select", "Male", "Female"])
            email = st.text_input("Email")

        if st.form_submit_button("Submit", use_container_width=True):
            if not all([fname, lname, phone]) or gender == "Select":
                st.error("Please fill all required fields")
            else:
                try:
                    run_query(
                        "INSERT INTO Patient (first_name, last_name, dob, gender, phone_number, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            fname,
                            lname,
                            dob,
                            gender,
                            phone,
                            email or None,
                            address or None,
                        ),
                    )
                    st.success("Registration complete!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Registration failed: {e}")


def render_login_view():
    if st.button("← Back"):
        st.session_state["patient_view"] = "home"
        st.rerun()

    st.subheader("Patient Login")
    dob = st.date_input("Date of Birth", datetime(2000, 1, 1))

    if st.button("Search", use_container_width=True):
        patients = run_query(
            "SELECT patient_id, first_name, last_name, phone_number, email FROM Patient WHERE dob = %s",
            (dob,),
            fetch=True,
        )
        st.session_state["search_results"] = patients
        st.session_state["search_performed"] = True
        st.rerun()

    if st.session_state["search_performed"]:
        patients = st.session_state["search_results"]
        if patients:
            st.success(f"Found {len(patients)} patient(s)")
            for p in patients:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{p['first_name']} {p['last_name']}**")
                    st.caption(f"Phone: {p['phone_number']}")
                with col2:
                    if st.button(
                        "Login",
                        key=f"login_{p['patient_id']}",
                        use_container_width=True,
                    ):
                        st.session_state.update(
                            {
                                "logged_in_patient_id": p["patient_id"],
                                "logged_in_patient_name": f"{p['first_name']} {p['last_name']}",
                                "patient_view": "dashboard",
                                "search_results": None,
                                "search_performed": False,
                            }
                        )
                        st.rerun()
                st.divider()
        else:
            st.warning("No patients found")


# Dashboard views
def render_patient_dashboard():
    st.header(f"Welcome, {st.session_state['logged_in_patient_name']}!")

    if st.button("Logout", type="primary"):
        logout()
        st.rerun()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        nav_button("Book Appointment", "book")
        nav_button("Cancel Appointment", "cancel")
    with col2:
        nav_button("View Appointments", "view")
        nav_button("Update Profile", "update_profile")


def back_to_dash():
    if st.button("← Dashboard"):
        st.session_state["patient_view"] = "dashboard"
        st.rerun()


def get_appointments(patient_id, status_filter=None):
    """Unified appointment query"""
    query = """
        SELECT a.appointment_id, a.appointment_datetime, a.status, a.reason_for_visit, a.schedule_id,
               s.available_day, s.start_time, s.end_time,
               d.first_name AS doctor_first_name, d.last_name AS doctor_last_name,
               sp.specialization_name
        FROM Appointment a
        JOIN Schedule s ON a.schedule_id = s.schedule_id
        JOIN Doctor d ON s.doctor_id = d.doctor_id
        JOIN Specialization sp ON d.specialization_id = sp.specialization_id
        WHERE a.patient_id = %s
    """
    params = [patient_id]
    if status_filter:
        query += " AND a.status = %s"
        params.append(status_filter)
    query += " ORDER BY a.appointment_datetime DESC"
    return run_query(query, tuple(params), fetch=True)


def render_appointment_item(appt, show_cancel=False):
    """Reusable appointment display"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(
            f"**{appt['available_day']} at {appt['start_time']}–{appt['end_time']}**"
        )
        st.caption(f"Dr. {appt['doctor_first_name']} {appt['doctor_last_name']}")
        st.caption(f"Reason: {appt.get('reason_for_visit') or 'Not specified'}")
        if not show_cancel:
            st.caption(f"Status: {appt['status']}")
    with col2:
        if show_cancel:
            if st.button(
                "Cancel",
                key=f"cancel_{appt['appointment_id']}",
                use_container_width=True,
            ):
                try:
                    run_query(
                        "UPDATE Appointment SET status = 'cancelled' WHERE appointment_id = %s",
                        (appt["appointment_id"],),
                    )
                    run_query(
                        "UPDATE Schedule SET is_booked = FALSE WHERE schedule_id = %s",
                        (appt["schedule_id"],),
                    )
                    st.success("Cancelled")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            status_map = {
                "scheduled": st.success,
                "completed": st.info,
                "cancelled": st.error,
            }
            status_map.get(appt["status"], st.info)(appt["status"].title())
    st.divider()


def render_view_appointments():
    back_to_dash()
    st.subheader("My Appointments")

    appointments = get_appointments(st.session_state["logged_in_patient_id"])

    if not appointments:
        st.info("No appointments yet")
        nav_button("Book First Appointment", "book")
        return

    grouped = defaultdict(list)
    for appt in appointments:
        grouped[appt["status"]].append(appt)

    status_icons = {
        "scheduled": "🟢",
        "completed": "🔵",
        "cancelled": "🔴",
    }

    for status in ["scheduled", "completed", "cancelled"]:
        if status in grouped:
            with st.expander(
                f"{status_icons[status]} {status.title()} ({len(grouped[status])})",
                expanded=(status == "scheduled"),
            ):
                for appt in grouped[status]:
                    render_appointment_item(appt)


def render_cancel_view():
    back_to_dash()
    st.subheader("Cancel an Appointment")

    appointments = get_appointments(
        st.session_state["logged_in_patient_id"], "scheduled"
    )

    if not appointments:
        st.info("No scheduled appointments")
    else:
        for appt in appointments:
            render_appointment_item(appt, show_cancel=True)


def render_booking_view():
    back_to_dash()
    st.subheader("Book an Appointment")

    specs = run_query("SELECT * FROM Specialization", fetch=True)
    if not specs:
        st.error("No specializations available")
        return

    spec_choice = st.selectbox(
        "Specialization", [s["specialization_name"] for s in specs]
    )
    spec_id = next(
        s["specialization_id"] for s in specs if s["specialization_name"] == spec_choice
    )

    doctors = run_query(
        "SELECT doctor_id, first_name, last_name FROM Doctor WHERE specialization_id = %s",
        (spec_id,),
        fetch=True,
    )
    if not doctors:
        st.warning("No doctors available")
        return

    doctor_choice = st.selectbox(
        "Doctor", [f"Dr. {d['first_name']} {d['last_name']}" for d in doctors]
    )
    doctor_id = next(
        d["doctor_id"]
        for d in doctors
        if f"Dr. {d['first_name']} {d['last_name']}" == doctor_choice
    )

    slots = run_query(
        "SELECT * FROM Schedule WHERE doctor_id = %s AND is_booked = FALSE",
        (doctor_id,),
        fetch=True,
    )
    if not slots:
        st.info("No slots available")
        return

    slot_choice = st.selectbox(
        "Time Slot",
        [f"{s['available_day']} {s['start_time']}–{s['end_time']}" for s in slots],
    )
    slot = next(
        s
        for s in slots
        if f"{s['available_day']} {s['start_time']}–{s['end_time']}" == slot_choice
    )

    reason = st.text_input("Reason for visit")

    if st.button("Confirm", use_container_width=True):
        try:
            run_query(
                "INSERT INTO Appointment (patient_id, schedule_id, reason_for_visit, appointment_datetime, status) VALUES (%s, %s, %s, %s, 'scheduled')",
                (
                    st.session_state["logged_in_patient_id"],
                    slot["schedule_id"],
                    reason,
                    f"2025-12-01 {slot['start_time']}",
                ),
            )
            run_query(
                "UPDATE Schedule SET is_booked = TRUE WHERE schedule_id = %s",
                (slot["schedule_id"],),
            )
            st.success("Appointment booked!")
            st.balloons()
        except Exception as e:
            st.error(f"Booking failed: {e}")


def render_update_profile():
    back_to_dash()
    st.subheader("Update My Profile")
    st.info("Name, DOB, and gender are locked")

    patient = run_query(
        "SELECT * FROM Patient WHERE patient_id = %s",
        (st.session_state["logged_in_patient_id"],),
        fetch=True,
    )[0]

    with st.form("update_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("First Name", patient["first_name"], disabled=True)
            st.text_input("Last Name", patient["last_name"], disabled=True)
            st.date_input("DOB", patient["dob"], disabled=True)
        with col2:
            st.text_input("Gender", patient["gender"] or "Not set", disabled=True)
            phone = st.text_input("Phone *", patient["phone_number"])
            email = st.text_input("Email", patient["email"] or "")

        address = st.text_area("Address", patient["address"] or "")

        if st.form_submit_button("Save", use_container_width=True):
            if not phone:
                st.error("Phone required")
            else:
                try:
                    run_query(
                        "UPDATE Patient SET phone_number = %s, email = %s, address = %s WHERE patient_id = %s",
                        (phone, email or None, address or None, patient["patient_id"]),
                    )
                    st.success("Profile updated!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Update failed: {e}")


# Main router
def main():
    init_state()

    if st.session_state["logged_in_patient_id"]:
        match st.session_state["patient_view"]:
            case "dashboard":
                render_patient_dashboard()
            case "book":
                render_booking_view()
            case "view":
                render_view_appointments()
            case "cancel":
                render_cancel_view()
            case "update_profile":
                render_update_profile()
            case _:
                render_patient_dashboard()
    else:
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
