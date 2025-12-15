import streamlit as st
from db_utils import run_query


def init_state():
    """Initialize admin session state"""
    defaults = {
        "admin_view": "home",
        "selected_invoice_id": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_home_view():
    """Admin dashboard home with navigation"""
    st.header("Clinic Admin Portal")
    st.write("Manage clinic operations and view analytics")
    st.divider()

    # Navigation cards
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Dashboard & Analytics", use_container_width=True, type="primary"):
            st.session_state["admin_view"] = "dashboard"
            st.rerun()

        if st.button("View All Schedules", use_container_width=True):
            st.session_state["admin_view"] = "schedules"
            st.rerun()

        if st.button("View Database Tables", use_container_width=True):
            st.session_state["admin_view"] = "database"
            st.rerun()

    with col2:
        if st.button("View All Appointments", use_container_width=True):
            st.session_state["admin_view"] = "appointments"
            st.rerun()

        if st.button("Manage Invoices", use_container_width=True):
            st.session_state["admin_view"] = "invoices"
            st.rerun()


def render_dashboard():
    """Analytics dashboard with appointment and revenue summary"""
    if st.button("← Back to Home"):
        st.session_state["admin_view"] = "home"
        st.rerun()

    st.header("Clinic Dashboard")
    st.divider()

    # Appointment Summary
    st.subheader("Appointment Summary")
    appointment_summary = run_query(
        """
        SELECT status, COUNT(*) as count
        FROM Appointment
        GROUP BY status
        """,
        fetch=True,
    )

    if appointment_summary:
        cols = st.columns(len(appointment_summary))
        for idx, stat in enumerate(appointment_summary):
            with cols[idx]:
                st.metric(stat["status"].capitalize(), stat["count"])
    else:
        st.info("No appointment data available")

    st.divider()

    # Revenue Summary
    st.subheader("Revenue Summary")

    revenue_data = run_query(
        """
        SELECT 
            SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as total_paid,
            SUM(CASE WHEN status = 'unpaid' THEN amount ELSE 0 END) as total_unpaid,
            SUM(amount) as total_revenue
        FROM Invoice
        """,
        fetch=True,
    )

    if revenue_data and revenue_data[0]["total_revenue"]:
        rev = revenue_data[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"Rp {rev['total_revenue']:,.0f}")
        with col2:
            st.metric("Paid", f"Rp {rev['total_paid']:,.0f}")
        with col3:
            st.metric("Outstanding", f"Rp {rev['total_unpaid']:,.0f}")
    else:
        st.info("No revenue data available")

    st.divider()

    # Recent Activity
    st.subheader("Recent Completed Appointments")

    recent_appointments = run_query(
        """
        SELECT 
            a.appointment_datetime,
            p.first_name as patient_first,
            p.last_name as patient_last,
            d.first_name as doctor_first,
            d.last_name as doctor_last,
            a.reason_for_visit,
            r.diagnosis
        FROM Appointment a
        JOIN Patient p ON a.patient_id = p.patient_id
        JOIN Schedule sch ON a.schedule_id = sch.schedule_id
        JOIN Doctor d ON sch.doctor_id = d.doctor_id
        LEFT JOIN Record r ON a.appointment_id = r.appointment_id
        WHERE a.status = 'completed'
        ORDER BY a.appointment_datetime DESC
        LIMIT 10
        """,
        fetch=True,
    )

    if recent_appointments:
        for appt in recent_appointments:
            with st.expander(
                f"{appt['appointment_datetime'].strftime('%Y-%m-%d %H:%M')} - "
                f"{appt['patient_first']} {appt['patient_last']} → "
                f"Dr. {appt['doctor_first']} {appt['doctor_last']}"
            ):
                st.write(
                    f"**Reason:** {appt['reason_for_visit'] or 'General consultation'}"
                )
                st.write(f"**Diagnosis:** {appt['diagnosis'] or 'N/A'}")
    else:
        st.info("No recent completed appointments")


def render_schedules():
    """View all doctor schedules"""
    if st.button("← Back to Home"):
        st.session_state["admin_view"] = "home"
        st.rerun()

    st.header("Doctor Schedules")
    st.divider()

    schedules = run_query(
        """
        SELECT 
            d.first_name as doctor_first,
            d.last_name as doctor_last,
            s.specialization_name,
            sch.available_day,
            sch.start_time,
            sch.end_time,
            sch.is_booked
        FROM Schedule sch
        JOIN Doctor d ON sch.doctor_id = d.doctor_id
        JOIN Specialization s ON d.specialization_id = s.specialization_id
        ORDER BY d.doctor_id, sch.available_day, sch.start_time
        """,
        fetch=True,
    )

    if schedules:
        # Group by doctor
        current_doctor = None
        for schedule in schedules:
            doctor_name = f"Dr. {schedule['doctor_first']} {schedule['doctor_last']}"

            if current_doctor != doctor_name:
                if current_doctor is not None:
                    st.divider()
                st.subheader(f"{doctor_name} - {schedule['specialization_name']}")
                current_doctor = doctor_name

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{schedule['available_day']}**")
            with col2:
                st.write(f"{schedule['start_time']} - {schedule['end_time']}")
            with col3:
                if schedule["is_booked"]:
                    st.markdown(":red[**Booked**]")
                else:
                    st.markdown(":green[**Free**]")
    else:
        st.info("No schedules available")


def render_appointments():
    """View all appointments with filtering"""
    if st.button("← Back to Home"):
        st.session_state["admin_view"] = "home"
        st.rerun()

    st.header("All Appointments")

    # Status filter
    status_filter = st.selectbox(
        "Filter by Status", ["All", "scheduled", "completed", "cancelled"]
    )

    st.divider()

    # Build query based on filter
    if status_filter == "All":
        where_clause = ""
        params = ()
    else:
        where_clause = "WHERE a.status = %s"
        params = (status_filter,)

    appointments = run_query(
        f"""
        SELECT 
            a.appointment_id,
            a.appointment_datetime,
            a.status,
            a.reason_for_visit,
            p.first_name as patient_first,
            p.last_name as patient_last,
            p.phone_number,
            d.first_name as doctor_first,
            d.last_name as doctor_last,
            s.specialization_name
        FROM Appointment a
        JOIN Patient p ON a.patient_id = p.patient_id
        JOIN Schedule sch ON a.schedule_id = sch.schedule_id
        JOIN Doctor d ON sch.doctor_id = d.doctor_id
        JOIN Specialization s ON d.specialization_id = s.specialization_id
        {where_clause}
        ORDER BY a.appointment_datetime DESC
        """,
        params,
        fetch=True,
    )

    if appointments:
        st.write(f"**Total: {len(appointments)} appointment(s)**")
        st.divider()

        for appt in appointments:
            # Status badge color
            if appt["status"] == "completed":
                status_badge = ":green[COMPLETED]"
            elif appt["status"] == "scheduled":
                status_badge = ":orange[SCHEDULED]"
            else:  # cancelled
                status_badge = ":red[CANCELLED]"

            with st.expander(
                f"{appt['appointment_datetime'].strftime('%Y-%m-%d %H:%M')} - "
                f"{appt['patient_first']} {appt['patient_last']} → "
                f"Dr. {appt['doctor_first']} {appt['doctor_last']}"
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Appointment ID:** {appt['appointment_id']}")
                    st.write(
                        f"**Patient:** {appt['patient_first']} {appt['patient_last']}"
                    )
                    st.write(f"**Phone:** {appt['phone_number']}")
                with col2:
                    st.write(
                        f"**Doctor:** Dr. {appt['doctor_first']} {appt['doctor_last']}"
                    )
                    st.write(f"**Specialization:** {appt['specialization_name']}")
                    st.markdown(f"**Status:** {status_badge}")

                st.write(
                    f"**Reason:** {appt['reason_for_visit'] or 'General consultation'}"
                )
    else:
        st.info("No appointments found")


def render_invoices():
    """Manage invoices: view, create, update payment status"""
    if st.button("← Back to Home"):
        st.session_state["admin_view"] = "home"
        st.rerun()

    st.header("Invoice Management")

    # Tabs for different invoice operations
    tab1, tab2, tab3 = st.tabs(
        ["View All Invoices", "Create Invoice", "Update Payment"]
    )

    # Tab 1: View All Invoices
    with tab1:
        st.subheader("All Invoices")

        invoices = run_query(
            """
            SELECT 
                i.appointment_id,
                i.amount,
                i.issue_date,
                i.status,
                p.first_name as patient_first,
                p.last_name as patient_last,
                a.appointment_datetime,
                a.reason_for_visit
            FROM Invoice i
            JOIN Appointment a ON i.appointment_id = a.appointment_id
            JOIN Patient p ON a.patient_id = p.patient_id
            ORDER BY i.issue_date DESC
            """,
            fetch=True,
        )

        if invoices:
            st.write(f"**Total: {len(invoices)} invoice(s)**")
            st.divider()

            for inv in invoices:
                status_badge = (
                    ":green[PAID]" if inv["status"] == "paid" else ":orange[UNPAID]"
                )

                with st.expander(
                    f"Invoice #{inv['appointment_id']} - "
                    f"{inv['patient_first']} {inv['patient_last']} - "
                    f"Rp {inv['amount']:,.0f} - {status_badge}"
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(
                            f"**Patient:** {inv['patient_first']} {inv['patient_last']}"
                        )
                        st.write(
                            f"**Appointment Date:** {inv['appointment_datetime'].strftime('%Y-%m-%d')}"
                        )
                        st.write(f"**Reason:** {inv['reason_for_visit'] or 'General'}")
                    with col2:
                        st.write(f"**Amount:** Rp {inv['amount']:,.0f}")
                        st.write(f"**Issue Date:** {inv['issue_date']}")
                        st.markdown(f"**Status:** {status_badge}")
        else:
            st.info("No invoices found")

    # Tab 2: Create Invoice
    with tab2:
        st.subheader("Create New Invoice")
        st.write("Create invoices for completed appointments without invoices")

        # Get completed appointments without invoices
        eligible_appointments = run_query(
            """
            SELECT 
                a.appointment_id,
                a.appointment_datetime,
                a.reason_for_visit,
                p.first_name as patient_first,
                p.last_name as patient_last,
                d.first_name as doctor_first,
                d.last_name as doctor_last
            FROM Appointment a
            JOIN Patient p ON a.patient_id = p.patient_id
            JOIN Schedule sch ON a.schedule_id = sch.schedule_id
            JOIN Doctor d ON sch.doctor_id = d.doctor_id
            LEFT JOIN Invoice i ON a.appointment_id = i.appointment_id
            WHERE a.status = 'completed' AND i.appointment_id IS NULL
            ORDER BY a.appointment_datetime DESC
            """,
            fetch=True,
        )

        if eligible_appointments:
            st.write(f"**{len(eligible_appointments)} appointment(s) need invoices**")
            st.divider()

            with st.form("create_invoice_form"):
                # Select appointment
                appointment_options = {
                    f"#{appt['appointment_id']} - {appt['patient_first']} {appt['patient_last']} → "
                    f"Dr. {appt['doctor_first']} {appt['doctor_last']} "
                    f"({appt['appointment_datetime'].strftime('%Y-%m-%d')})": appt[
                        "appointment_id"
                    ]
                    for appt in eligible_appointments
                }

                selected_appt = st.selectbox(
                    "Select Appointment", options=list(appointment_options.keys())
                )

                amount = st.number_input(
                    "Invoice Amount (Rp)",
                    min_value=0.0,
                    step=10000.0,
                    value=150000.0,
                    format="%.2f",
                )

                submitted = st.form_submit_button(
                    "Create Invoice", use_container_width=True, type="primary"
                )

            if submitted:
                try:
                    appointment_id = appointment_options[selected_appt]
                    run_query(
                        """
                        INSERT INTO Invoice (appointment_id, amount, issue_date, status)
                        VALUES (%s, %s, CURDATE(), 'unpaid')
                        """,
                        (appointment_id, amount),
                    )
                    st.success(
                        f"Invoice created successfully for Appointment #{appointment_id}!"
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to create invoice: {e}")
        else:
            st.info("No completed appointments need invoices")

    # Tab 3: Update Payment Status
    with tab3:
        st.subheader("Update Payment Status")
        st.write("Mark invoices as paid")

        # Get unpaid invoices
        unpaid_invoices = run_query(
            """
            SELECT 
                i.appointment_id,
                i.amount,
                i.issue_date,
                p.first_name as patient_first,
                p.last_name as patient_last,
                a.appointment_datetime
            FROM Invoice i
            JOIN Appointment a ON i.appointment_id = a.appointment_id
            JOIN Patient p ON a.patient_id = p.patient_id
            WHERE i.status = 'unpaid'
            ORDER BY i.issue_date
            """,
            fetch=True,
        )

        if unpaid_invoices:
            st.write(f"**{len(unpaid_invoices)} unpaid invoice(s)**")
            st.divider()

            for inv in unpaid_invoices:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Invoice #{inv['appointment_id']}**")
                    st.write(
                        f"{inv['patient_first']} {inv['patient_last']} - Rp {inv['amount']:,.0f}"
                    )
                    st.caption(
                        f"Issued: {inv['issue_date']} | Appointment: {inv['appointment_datetime'].strftime('%Y-%m-%d')}"
                    )
                with col2:
                    if st.button(
                        "Mark Paid",
                        key=f"pay_{inv['appointment_id']}",
                        use_container_width=True,
                    ):
                        try:
                            run_query(
                                "UPDATE Invoice SET status = 'paid' WHERE appointment_id = %s",
                                (inv["appointment_id"],),
                            )
                            st.success(
                                f"Invoice #{inv['appointment_id']} marked as paid!"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to update: {e}")
                st.divider()
        else:
            st.success("All invoices are paid!")

def render_database():
    """View database tables"""
    if st.button("← Back to Home"):
        st.session_state["admin_view"] = "home"
        st.rerun()

    st.header("Database Tables")
    st.write("View all data in each table")
    st.divider()

    # List of tables to display
    tables = [
        "Specialization",
        "Patient", 
        "Doctor",
        "Schedule",
        "Appointment",
        "Record",
        "Invoice"
    ]

    # Table selector
    selected_table = st.selectbox("Select Table", tables)
    
    st.subheader(f"Table: {selected_table}")
    
    # Query and display the selected table
    data = run_query(f"SELECT * FROM {selected_table}", fetch=True)
    
    if data:
        st.write(f"**Total rows: {len(data)}**")
        st.dataframe(data, use_container_width=True)
    else:
        st.info(f"No data in {selected_table}")


def main():
    init_state()

    match st.session_state["admin_view"]:
        case "dashboard":
            render_dashboard()
        case "schedules":
            render_schedules()
        case "appointments":
            render_appointments()
        case "invoices":
            render_invoices()
        case "database":
            render_database()
        case _:
            render_home_view()


if __name__ == "__main__":
    main()
