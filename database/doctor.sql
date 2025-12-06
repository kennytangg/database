-- 1. Get all doctors with their specializations (login)
SELECT d.doctor_id, d.first_name, d.last_name, s.specialization_name
FROM Doctor d 
JOIN Specialization s ON d.specialization_id = s.specialization_id;


-- 2. View today scheduled appointments
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
ORDER BY a.appointment_datetime;


-- 3. Get patient basic information
SELECT first_name, last_name, dob, gender, phone_number, email, address
FROM Patient
WHERE patient_id = %s;


-- 4. Get patient previous visit history with medical records
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
LIMIT 5;


-- 5. Get current appointment details
SELECT p.first_name, p.last_name, a.reason_for_visit
FROM Appointment a
JOIN Patient p ON a.patient_id = p.patient_id
WHERE a.appointment_id = %s;


-- 6. Update appointment status to completed
UPDATE Appointment 
SET status = 'completed' 
WHERE appointment_id = %s;


-- 7. Create medical record
INSERT INTO Record (appointment_id, diagnosis, prescription, notes) 
VALUES (%s, %s, %s, %s);
