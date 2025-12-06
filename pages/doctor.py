import streamlit as st
from db_utils import run_query
from datetime import date


def init_state():
    """Initialize doctor session state"""
    defaults = {
        "doctor_view": "home",
        "logged_in_doctor_id": None,
        "logged_in_doctor_name": None,
        "selected_appointment_id": None,
        "selected_patient_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def logout():
    """Clear doctor session"""
    st.session_state.update(
        {
            "logged_in_doctor_id": None,
            "logged_in_doctor_name": None,
            "doctor_view": "home",
            "selected_appointment_id": None,
            "selected_patient_id": None,
        }
    )


def render_home_view():
    """Doctor login page"""
    st.header("Doctor Portal")
    st.write("Select your profile to login")

    doctors = run_query(
        "SELECT d.doctor_id, d.first_name, d.last_name, s.specialization_name "
        "FROM Doctor d JOIN Specialization s ON d.specialization_id = s.specialization_id",
        fetch=True,
    )

    for doc in doctors:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Dr. {doc['first_name']} {doc['last_name']}**")
            st.caption(f"Specialization: {doc['specialization_name']}")
        with col2:
            if st.button(
                "Login", key=f"doc_{doc['doctor_id']}", use_container_width=True
            ):
                st.session_state.update(
                    {
                        "logged_in_doctor_id": doc["doctor_id"],
                        "logged_in_doctor_name": f"Dr. {doc['first_name']} {doc['last_name']}",
                        "doctor_view": "dashboard",
                    }
                )
                st.rerun()
        st.divider()


def render_dashboard():
    """Doctor dashboard - Today appointments list"""
    st.header(f"Welcome, {st.session_state['logged_in_doctor_name']}!")

    if st.button("Logout", type="primary"):
        logout()
        st.rerun()

    st.divider()
    st.subheader("Today's Appointments")

    # Get today scheduled appointments
    appointments = run_query(
    """
        SELECT 
            a.appointment_id,
            a.reason_for_visit,
            a.appointment_datetime,
            sch.start_time,
            sch.end_time,
            p.patient_id,
            p.first_name AS patient_first_name,
            p.last_name AS patient_last_name,
            p.gender,
            p.dob
        FROM Appointment a
        JOIN Schedule sch ON a.schedule_id = sch.schedule_id
        JOIN Patient p ON a.patient_id = p.patient_id
        WHERE sch.doctor_id = %s 
          AND a.status = 'scheduled'
          AND DATE(a.appointment_datetime) = CURDATE()
        ORDER BY a.appointment_datetime
    """,
        (st.session_state["logged_in_doctor_id"],),
        fetch=True,
    )

    if not appointments:
        st.info("No scheduled appointments for today")
        return

    st.write(f"**{len(appointments)} patient(s) scheduled**")
    st.divider()

    for appt in appointments:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{appt['start_time']} - {appt['end_time']}**")
            st.write(f"{appt['patient_first_name']} {appt['patient_last_name']}")
            st.caption(f"Reason: {appt['reason_for_visit'] or 'General consultation'}")
        with col2:
            if st.button(
                "Open", key=f"open_{appt['appointment_id']}", use_container_width=True
            ):
                st.session_state["selected_appointment_id"] = appt["appointment_id"]
                st.session_state["selected_patient_id"] = appt["patient_id"]
                st.session_state["doctor_view"] = "patient_context"
                st.rerun()
        st.divider()


def render_patient_context():
    """Review patient context - basic info + previous visits"""
    if st.button("← Back to Dashboard"):
        st.session_state["doctor_view"] = "dashboard"
        st.session_state["selected_appointment_id"] = None
        st.session_state["selected_patient_id"] = None
        st.rerun()

    patient_id = st.session_state["selected_patient_id"]

    # Get patient basic info
    patient = run_query(
        """
        SELECT first_name, last_name, dob, gender, phone_number, email, address
        FROM Patient
        WHERE patient_id = %s
    """,
        (patient_id,),
        fetch=True,
    )[0]

    # Calculate age
    today = date.today()
    age = (
        today.year
        - patient["dob"].year
        - ((today.month, today.day) < (patient["dob"].month, patient["dob"].day))
    )

    st.subheader(f"Patient: {patient['first_name']} {patient['last_name']}")

    # Patient info card
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Age", f"{age} years")
        st.metric("Gender", patient["gender"])
    with col2:
        st.write(f"**DOB:** {patient['dob']}")
        st.write(f"**Phone:** {patient['phone_number']}")

    st.divider()

    # Previous visits
    st.markdown("### Previous Visits")

    previous_visits = run_query(
        """
        SELECT 
            a.appointment_datetime,
            a.reason_for_visit,
            r.diagnosis,
            r.prescription,
            r.notes
        FROM Appointment a
        LEFT JOIN Record r ON a.appointment_id = r.appointment_id
        WHERE a.patient_id = %s 
          AND a.status = 'completed'
          AND a.appointment_id != %s
        ORDER BY a.appointment_datetime DESC
        LIMIT 5
    """,
        (patient_id, st.session_state["selected_appointment_id"]),
        fetch=True,
    )

    if previous_visits:
        for visit in previous_visits:
            with st.expander(
                f"{visit['appointment_datetime'].strftime('%Y-%m-%d')} - {visit['reason_for_visit'] or 'General'}"
            ):
                st.write(f"**Diagnosis:** {visit['diagnosis'] or 'N/A'}")
                st.write(f"**Prescription:** {visit['prescription'] or 'N/A'}")
                if visit["notes"]:
                    st.write(f"**Notes:** {visit['notes']}")
    else:
        st.info("No previous visits found (First time patient)")

    st.divider()

    # Button to proceed to appointment
    if st.button("️Start Appointment", use_container_width=True, type="primary"):
        st.session_state["doctor_view"] = "conduct_appointment"
        st.rerun()


def render_conduct_appointment():
    """Conduct appointment and input diagnosis/prescription"""
    if st.button("← Back to Patient Info"):
        st.session_state["doctor_view"] = "patient_context"
        st.rerun()

    appointment_id = st.session_state["selected_appointment_id"]

    # Get current appointment details
    appt = run_query(
        """
        SELECT 
            p.first_name,
            p.last_name,
            a.reason_for_visit
        FROM Appointment a
        JOIN Patient p ON a.patient_id = p.patient_id
        WHERE a.appointment_id = %s
    """,
        (appointment_id,),
        fetch=True,
    )[0]

    st.subheader(f"Appointment: {appt['first_name']} {appt['last_name']}")
    st.write(
        f"**Reason for visit:** {appt['reason_for_visit'] or 'General consultation'}"
    )

    st.divider()

    # Input form
    with st.form("appointment_form"):
        st.markdown("### Medical Record")

        diagnosis = st.text_input("Diagnosis *", placeholder="Enter diagnosis")
        prescription = st.text_input(
            "Prescription/Treatment", placeholder="Enter prescription or treatment plan"
        )
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any additional observations or instructions",
            height=100,
        )

        submitted = st.form_submit_button(
            "Save & Complete Visit", use_container_width=True, type="primary"
        )

    if submitted:
        if not diagnosis:
            st.error("Diagnosis is required")
        else:
            try:
                # Update appointment status
                run_query(
                    "UPDATE Appointment SET status = 'completed' WHERE appointment_id = %s",
                    (appointment_id,),
                )

                # Add medical record
                run_query(
                    "INSERT INTO Record (appointment_id, diagnosis, prescription, notes) VALUES (%s, %s, %s, %s)",
                    (appointment_id, diagnosis, prescription or None, notes or None),
                )

                st.success("Appointment completed successfully!")
                st.balloons()

                # Reset and return to dashboard
                st.session_state["selected_appointment_id"] = None
                st.session_state["selected_patient_id"] = None
                st.session_state["doctor_view"] = "dashboard"

                st.info("Returning to dashboard...")
                st.rerun()

            except Exception as e:
                st.error(f"Failed to complete appointment: {e}")


def main():
    init_state()

    if st.session_state["logged_in_doctor_id"]:
        match st.session_state["doctor_view"]:
            case "dashboard":
                render_dashboard()
            case "patient_context":
                render_patient_context()
            case "conduct_appointment":
                render_conduct_appointment()
            case _:
                render_dashboard()
    else:
        render_home_view()


if __name__ == "__main__":
    main()
