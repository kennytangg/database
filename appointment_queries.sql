-- CREATE: Book a new appointment for a patient with a doctor and schedule
INSERT INTO Appointment (appointment_id, patient_id, doctor_id, schedule_id, reason_for_visit, appointment_datetime, status)
VALUES (407, 104, 202, 302, 'Follow-up for dermatitis', '2025-12-08 11:30', 'scheduled');

-- READ: List all appointments
SELECT * FROM Appointment;

-- READ: Get upcoming appointments for a specific patient
SELECT * FROM Appointment
WHERE patient_id = 104 AND appointment_datetime > NOW()
ORDER BY appointment_datetime;

-- READ: Get all completed appointments for a doctor
SELECT * FROM Appointment
WHERE doctor_id = 201 AND status = 'completed';

-- UPDATE: Change appointment status and time (reschedule or mark completed)
UPDATE Appointment
SET appointment_datetime = '2025-12-09 09:00', status = 'completed'
WHERE appointment_id = 402;

-- DELETE: Cancel an appointment by ID
DELETE FROM Appointment WHERE appointment_id = 404;

-- ADVANCED: Count scheduled appointments per doctor (for workload)
SELECT doctor_id, COUNT(*) AS scheduled_appointments
FROM Appointment
WHERE status = 'scheduled'
GROUP BY doctor_id;

-- ADVANCED: Display doctor, patient, and appointment info for today's appointments
SELECT a.appointment_id, a.appointment_datetime, d.first_name AS doctor_name, p.first_name AS patient_name
FROM Appointment a
JOIN Doctor d ON a.doctor_id = d.doctor_id
JOIN Patient p ON a.patient_id = p.patient_id
WHERE DATE(a.appointment_datetime) = CURDATE();

-- ADVANCED: Show all upcoming appointments grouped by patient
SELECT p.patient_id, p.first_name, p.last_name, a.appointment_datetime, a.status
FROM Patient p
JOIN Appointment a ON p.patient_id = a.patient_id
WHERE a.appointment_datetime > NOW()
ORDER BY p.patient_id, a.appointment_datetime;
