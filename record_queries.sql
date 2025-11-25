-- CREATE: Add a new medical record for an appointment
INSERT INTO Record (appointment_id, diagnosis, prescription, notes)
VALUES (406, 'Dermatitis', 'Topical ointment', 'Initial diagnosis, prescribed medicine.');

-- CREATE: Only add a record if appointment is completed
INSERT INTO Record (patient_id, appointment_id, diagnosis, prescription, notes)
SELECT a.patient_id, a.appointment_id, 'Diagnosis', 'Prescription', 'Notes'
FROM Appointment a
WHERE a.appointment_id = 407 AND a.status = 'completed';

-- READ: Get all records (view all diagnoses and prescriptions)
SELECT * FROM Record;

-- READ: Get record for a specific appointment
SELECT * FROM Record WHERE appointment_id = 401;

-- UPDATE: Update diagnosis and notes for a record
UPDATE Record
SET diagnosis = 'Resolved', notes = 'Condition cleared, no prescription needed.'
WHERE appointment_id = 406;

-- DELETE: Remove a record for a specific appointment
DELETE FROM Record WHERE appointment_id = 401;

-- Show patient and record info by joining appointments and patients
SELECT r.*, p.patient_id, p.first_name, p.last_name
FROM Record r
JOIN Appointment a ON r.appointment_id = a.appointment_id
JOIN Patient p ON a.patient_id = p.patient_id
ORDER BY p.patient_id;

-- Count total records per patient
SELECT a.patient_id, COUNT(*) AS total_records
FROM Record r
JOIN Appointment a ON r.appointment_id = a.appointment_id
GROUP BY a.patient_id;

-- List all diagnoses made in clinic
SELECT DISTINCT diagnosis FROM Record WHERE diagnosis IS NOT NULL;

-- Recent records for review (last 7 days)
SELECT r.*, a.appointment_datetime
FROM Record r
JOIN Appointment a ON r.appointment_id = a.appointment_id
WHERE a.appointment_datetime > DATE_SUB(NOW(), INTERVAL 7 DAY);
