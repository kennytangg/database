-- CREATE: Add a new patient
INSERT INTO Patient (patient_id, first_name, last_name, dob, gender, phone_number, email, address)
VALUES (105, 'Erik', 'Pratama', '1995-02-14', 'Male', '081234567894', 'erik.pratama@example.com', 'Jl. Kebon Jeruk 5');

-- READ: Get all patients
SELECT * FROM Patient;

-- READ: Get a patient by ID
SELECT * FROM Patient WHERE patient_id = 101;

-- UPDATE: Update patient’s phone and address
UPDATE Patient
SET phone_number = '081299900123', address = 'Jl. Kemang 10'
WHERE patient_id = 102;

-- DELETE: Remove a patient by ID
DELETE FROM Patient WHERE patient_id = 103;

-- Count total number of patients
SELECT COUNT(*) AS total_patients FROM Patient;

-- Find patients by partial name (showcases searching/filtering with LIKE)
SELECT * FROM Patient WHERE first_name LIKE 'E%' OR last_name LIKE '%Lee%';

-- Show patients who have scheduled appointments (joins for reporting)
SELECT p.patient_id, p.first_name, p.last_name, a.appointment_id, a.appointment_datetime
FROM Patient p
JOIN Appointment a ON p.patient_id = a.patient_id
WHERE a.status = 'scheduled';
