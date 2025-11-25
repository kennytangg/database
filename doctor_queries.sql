-- CREATE: Add a new doctor
INSERT INTO Doctor (doctor_id, specialization_id, first_name, last_name, phone_number, email)
VALUES (205, 2, 'Dr. Nadia', 'Ramli', '081201234504', 'nadia.ramli@clinic.com');

-- READ: Get all doctors (for listing or directory)
SELECT * FROM Doctor;

-- READ: Get a specific doctor by their ID
SELECT * FROM Doctor WHERE doctor_id = 201;

-- UPDATE: Update a doctor's phone and email information
UPDATE Doctor
SET phone_number = '081288877700', email = 'agung.putra@clinicmail.com'
WHERE doctor_id = 201;

-- DELETE: Remove a doctor by ID
-- Delete related referencing this doctor
DELETE FROM Appointment WHERE doctor_id = 203;
DELETE FROM Schedule WHERE doctor_id = 203;
DELETE FROM Doctor WHERE doctor_id = 203;


-- Count total number of doctors in clinic
SELECT COUNT(*) AS total_doctors FROM Doctor;

-- List all doctors with their specialization
SELECT d.doctor_id, d.first_name, d.last_name, s.specialization_name
FROM Doctor d
JOIN Specialization s ON d.specialization_id = s.specialization_id;

-- Find all doctors who have an active schedule
SELECT d.doctor_id, d.first_name, d.last_name, sch.available_day
FROM Doctor d
JOIN Schedule sch ON d.doctor_id = sch.doctor_id
WHERE sch.is_booked = FALSE;

-- Find doctors who have scheduled appointments
SELECT DISTINCT d.doctor_id, d.first_name, d.last_name
FROM Doctor d
JOIN Appointment a ON d.doctor_id = a.doctor_id
WHERE a.status = 'scheduled';
