-- CREATE: Add a new schedule slot for a doctor
INSERT INTO Schedule (schedule_id, doctor_id, available_day, start_time, end_time, is_booked)
VALUES (305, 202, 'Thursday', '09:00', '12:00', FALSE);

-- READ: Get all schedules
SELECT * FROM Schedule;

-- READ: Get all schedules for a specific doctor
SELECT * FROM Schedule WHERE doctor_id = 201;

-- READ: Get a schedule by ID
SELECT * FROM Schedule WHERE schedule_id = 301;

-- UPDATE: Update a schedule’s availability (mark it booked, change time, etc.)
UPDATE Schedule
SET is_booked = TRUE, start_time = '10:00', end_time = '13:00'
WHERE schedule_id = 302;

-- DELETE: Remove a schedule by ID
-- Note: Delete any appointments referencing this schedule before deleting, OR update their schedule_id.
DELETE FROM Appointment WHERE schedule_id = 303;
DELETE FROM Schedule WHERE schedule_id = 303;

-- ADVANCED: Count available schedules per doctor
SELECT doctor_id, COUNT(*) AS available_slots
FROM Schedule
WHERE is_booked = FALSE
GROUP BY doctor_id;

-- ADVANCED: Show doctors and their next available schedule slot
SELECT d.doctor_id, d.first_name, d.last_name, s.available_day, s.start_time
FROM Doctor d
JOIN Schedule s ON d.doctor_id = s.doctor_id
WHERE s.is_booked = FALSE
ORDER BY s.start_time
LIMIT 1;

-- ADVANCED: Show all booked schedules
SELECT * FROM Schedule WHERE is_booked = TRUE;
