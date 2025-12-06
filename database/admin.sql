-- 1. Appointment summary by status
SELECT status, COUNT(*) as count
FROM Appointment
GROUP BY status;


-- 2. Revenue summary (paid, unpaid, total)
SELECT 
    SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as total_paid,
    SUM(CASE WHEN status = 'unpaid' THEN amount ELSE 0 END) as total_unpaid,
    SUM(amount) as total_revenue
FROM Invoice;


-- 3. Recent completed appointments (last 10)
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
LIMIT 10;


-- 4. All doctor schedules with availability
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
ORDER BY d.doctor_id, sch.available_day, sch.start_time;


-- 5. All appointments (no filter)
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
ORDER BY a.appointment_datetime DESC;


-- 6. Filter by status
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
WHERE a.status = %s
ORDER BY a.appointment_datetime DESC;


-- 7. All invoices with patient and appointment details
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
ORDER BY i.issue_date DESC;


-- 8. Get completed appointments without invoices
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
ORDER BY a.appointment_datetime DESC;


-- 9. Insert new invoice for completed appointment
INSERT INTO Invoice (appointment_id, amount, issue_date, status)
VALUES (%s, %s, CURDATE(), 'unpaid');


-- 10. Get all unpaid invoices
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
ORDER BY i.issue_date;


-- 11. Mark invoice as paid
UPDATE Invoice 
SET status = 'paid' 
WHERE appointment_id = %s;
