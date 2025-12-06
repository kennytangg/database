-- 1. Register new patient
INSERT INTO Patient (first_name, last_name, dob, gender, phone_number, email, address) 
VALUES (%s, %s, %s, %s, %s, %s, %s);

-- 2. Search patient by date of birth (login)
SELECT patient_id, first_name, last_name, phone_number, email 
FROM Patient 
WHERE dob = %s;

-- 3. View all appointments (with doctor and specialization details)
SELECT 
    a.appointment_id, 
    a.appointment_datetime, 
    a.status, 
    a.reason_for_visit, 
    a.schedule_id,
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
ORDER BY a.appointment_datetime DESC;


-- 4. View appointments by status (for filtered views)
SELECT 
    a.appointment_id, 
    a.appointment_datetime, 
    a.status, 
    a.reason_for_visit, 
    a.schedule_id,
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
WHERE a.patient_id = %s AND a.status = %s
ORDER BY a.appointment_datetime DESC;


-- 5. Update appointment status (cancel appointment)
UPDATE Appointment 
SET status = 'cancelled' 
WHERE appointment_id = %s;


-- 6. Free up the schedule slot 
UPDATE Schedule 
SET is_booked = FALSE 
WHERE schedule_id = %s;


-- 7. Get all specializations
SELECT * FROM Specialization;


-- 8. Get doctors by specialization
SELECT doctor_id, first_name, last_name 
FROM Doctor 
WHERE specialization_id = %s;


-- 9. Get available time slots for selected doctor
SELECT * 
FROM Schedule 
WHERE doctor_id = %s AND is_booked = FALSE;


-- 10. Create new appointment
INSERT INTO Appointment (patient_id, schedule_id, reason_for_visit, appointment_datetime, status) 
VALUES (%s, %s, %s, %s, 'scheduled');


-- 11. Mark schedule slot as booked
UPDATE Schedule 
SET is_booked = TRUE 
WHERE schedule_id = %s;


-- 12. Get current patient information
SELECT * 
FROM Patient 
WHERE patient_id = %s;


-- 13. Update patient contact information
UPDATE Patient 
SET phone_number = %s, email = %s, address = %s 
WHERE patient_id = %s;