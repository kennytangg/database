-- CREATE: Add a new specialization
INSERT INTO Specialization (specialization_id, specialization_name)
VALUES (5, 'Neurology');

-- READ: Get all specializations
SELECT * FROM Specialization;

-- READ: Get a specialization by ID
SELECT * FROM Specialization WHERE specialization_id = 2;

-- UPDATE: Update a specialization's name (renaming for clarity)
UPDATE Specialization
SET specialization_name = 'Skin Care'
WHERE specialization_id = 2;

-- DELETE: Remove a specialization by ID
-- Note: We must update any doctors referencing this specialization before deletion
-- Example: Set their specialization_id to another valid value or delete those doctors.
UPDATE Doctor SET specialization_id = 1 WHERE specialization_id = 2;
DELETE FROM Specialization WHERE specialization_id = 2;

-- ADVANCED: Count total number of specializations offered
SELECT COUNT(*) AS total_specializations FROM Specialization;

-- ADVANCED: List all doctors by specialization
SELECT s.specialization_name, d.first_name, d.last_name
FROM Specialization s
JOIN Doctor d ON s.specialization_id = d.specialization_id
ORDER BY s.specialization_name;

-- ADVANCED: Find all specializations with more than one doctor
SELECT s.specialization_name, COUNT(d.doctor_id) AS doctor_count
FROM Specialization s
JOIN Doctor d ON s.specialization_id = d.specialization_id
GROUP BY s.specialization_id
HAVING doctor_count > 1;
